#! /Users/asundar/.local/bin/python3

"""
FFT addition - read stdtime as input and output stdtime and stdspace of mixed traffic
"""

import random, sys, math, copy
import numpy as np
import scipy as sp
import scipy.signal
from scipy.optimize import brentq
import numpy.fft as fft
sys.path.append('Utils')
import StackDistance
import cmath
import os

# Floor for st and ss
def floor(t_set, t):
	# Error 
	if len(t_set) < 1:
		return -1
	# Only one element in t_set 
	if len(t_set) == 1:
		return t_set[0]
	# Match found
	if t in t_set:
		return t
	# t < min
	if t < t_set[0]:
		return t_set[0]
	# t > max
	if t > t_set[len(t_set) - 1]:
		return t_set[len(t_set) - 1]
	# Floor
	start = 0
	end = len(t_set) - 1
	while start < end:
		middle = (start + end) // 2
		if t_set[middle] > t:
			end = middle
		else:
			start = middle
		if (end - start + 1 == 2):
			return t_set[start]

# st->iat
def st_2_iat(st):
	pass
	#return dict((t, sum(st[t].values())) for t in st.keys())

# st->sd
def st_2_sd(st, sd):
	for t in st.keys():
		for s in st[t].keys():
			if s <= (sys.maxsize / 100): # HACK
				if s not in sd: 
					sd[s] = [0, 0]
				sd[s][0] += st[t][s][0] # HRC for requests
				sd[s][1] += st[t][s][1] # HRC for bytes

def pdf_2_cdf_sd(ss):
	s_set = sorted(ss.keys())
	i = 2
	l = len(ss)
	while i < (l + 1):
		ss[s_set[i - 1]][0] += ss[s_set[i - 2]][0]
		ss[s_set[i - 1]][1] += ss[s_set[i - 2]][1]
		i += 1

# Print key value from dict (for stdspace)
def f_print_out_sd(f_out, sd, rb_total):
	with open(f_out, 'w') as f:
		f.write("# r " + str(rb_total[0]) + ' b ' + str(rb_total[1]) + "\n")
		#f.write("#" + ' ' + str(rb_total[0]) + ' ' + str(rb_total[1]) + "\n")
		for k in sorted(list(sd.keys())):
			f.write(str(k) + ' ' + str(sd[k][0]) + ' ' + str(sd[k][0]) + "\n")

# Print stdtime
def f_print_out_st(f_out, st, rb_total):
        pass
	#with open(f_out, 'w') as f:
		#f.write("# r " + str(rb_total[0]) + ' b ' + str(rb_total[1]) + "\n")		
		#f.write("#" + ' ' + str(rb_total[0]) + ' ' + str(rb_total[1]) + "\n")
		#for t in sorted(st.keys()):
			#for s in sorted(st[t].keys()):
				#f.write(str(t) + ' ' + str(s) + ' ' + str(st[t][s][0]) + ' ' + str(st[t][s][1]) + "\n")

# Determine conditional distribution, conditioned on t
def cond_prob(st):
	for t in st.keys():
		prob_sum_st = sum([v[0] for v in st[t].values()])
		for s in st[t].keys():
			st[t][s] = [st[t][s][0] / prob_sum_st, st[t][s][0] / prob_sum_st] if prob_sum_st else [0, 0]

# 2D convolution
def convolve_2d(st1, st2, st12, rate1, rate2, sd_gran):
	# Determine conditional probabilties of st1 and st2
	st1_cond = copy.deepcopy(st1)
	cond_prob(st1_cond)
	st2_cond = copy.deepcopy(st2)
	cond_prob(st2_cond)
	t1_set = sorted(set(list(st1.keys())))
	t2_set = sorted(set(list(st2.keys())))
	t12_set = sorted(set(t1_set + t2_set))
	#print(len(t12_set))
	for t in t12_set:
		if (t in st1) and (t in st2):
			prob_t1 = sum([v[0] for v in st1[t].values()]) if t in st1 else 0
			prob_t2 = sum([v[0] for v in st2[t].values()]) if t in st2 else 0
			prob_t12 = (((rate1 / (rate1 + rate2)) * prob_t1) + ((rate2 / (rate1 + rate2)) * prob_t2), 0)
			st12[t] = {}
			# Get floor_t for st*_cond
			#st1_cond = copy.deepcopy(st1[t])
			st1_c = st1_cond[floor(sorted(set(st1_cond.keys())), t)]
			#st2_cond = copy.deepcopy(st2[t])
			st2_c = st2_cond[floor(sorted(set(st2_cond.keys())), t)]
			# Convolution
			out_k = set([])
			ct = 0
			for i in st1_c.keys():
				for j in st2_c.keys():
					out_k.add(i + j)
			out_k = sorted(out_k)
			for s in out_k:
				prob = 0
				for k in range(1, s + 1, sd_gran):
					prob += st1_c[k][0] * st2_c[s - k][0] if (k in st1_c and (s - k) in st2_c) else 0
				if prob:
					st12[t][s] = (prob * prob_t12[0], 0)

# 2D st convolution using FFT
def convolve_2d_fft(st1, st2, st12, st1_int, st2_int, rate1, rate2, sd_gran, f_out, rb_total):
	# Determine conditional probabilties of st1 and st2
        f = open(f_out, "w")
        f.write("# r " + str(rb_total[0]) + ' b ' + str(rb_total[1]) + "\n")		

	st1_cond = copy.deepcopy(st1)
	cond_prob(st1_cond)
	st2_cond = copy.deepcopy(st2)
	cond_prob(st2_cond)
	t1_set = sorted(set(list(st1.keys())))
	t2_set = sorted(set(list(st2.keys())))
	t12_set = sorted(set(t1_set + t2_set))
	for t in t12_set:
		#if (t in st1) and (t in st2):
			prob_t1 = sum([v[0] for v in st1[t].values()]) if t in st1 else 0
			prob_t2 = sum([v[0] for v in st2[t].values()]) if t in st2 else 0
			prob_t12 = (((rate1 / (rate1 + rate2)) * prob_t1) + ((rate2 / (rate1 + rate2)) * prob_t2), 0)
			st12[t] = {}
			st1_int[t] = {}
			st2_int[t] = {}

			# Get floor_t for st*_cond
			#st1_cond = copy.deepcopy(st1[t])
			st1_c = st1_cond[floor(sorted(set(st1_cond.keys())), t)]

			#st2_cond = copy.deepcopy(st2[t])

			st2_c = st2_cond[floor(sorted(set(st2_cond.keys())), t)]

			# Convolution using fft

			min_st1_s = min(st1_c.keys())
			max_st1_s = max(st1_c.keys())
			min_st2_s = min(st2_c.keys())
			max_st2_s = max(st2_c.keys())
			out_k = set([])
			out_k2 = set([])
			out_k = sorted([i for i in range(min_st1_s + min_st2_s, max_st1_s + max_st2_s + 1, sd_gran)])

			st1_tmp = [st1_c[k][0] if k in st1_c else 0 for k in range(min_st1_s, max_st1_s + 1, sd_gran)]
			st2_tmp = [st2_c[k][0] if k in st2_c else 0 for k in range(min_st2_s, max_st2_s + 1, sd_gran)]

			st1_fft = fft.fft(st1_tmp, len(st1_tmp) + len(st2_tmp) - 1)
			st2_fft = fft.fft(st2_tmp, len(st1_tmp) + len(st2_tmp) - 1)
			st12_fft = [0 for i in range(len(st1_tmp) + len(st2_tmp) - 1)]
			for i in range(len(st12_fft)):
				st12_fft[i] = st1_fft[i] * st2_fft[i]
			st12_conv = fft.ifft(st12_fft)

			for i in range(len(st12_conv)):
				#if out_k[i] in out_k2:
				#if float(st12_conv[i]) > 1e-5:
				#st12[t][out_k[i]] = (float(st12_conv[i]) * prob_t12[0], float(st12_conv[i]) * prob_t12[0])
                                f.write(str(t) + " " + str(out_k[i]) + " " + str(float(st12_conv[i]) * prob_t12[0]) + " " + str(float(st12_conv[i]) * prob_t12[0]))
                                f.write("\n")
                                #f.flush()

                                if float(st12_conv[i]) * prob_t12[0] < 1e-10:
                                        break

				# Interference hit rates
				#st12[t][out_k[i]] = (float(st12_conv[i]) * prob_t1, 0)
				#st1_int[t][out_k[i]] = (float(st12_conv[i]) * prob_t1, 0)
				#st2_int[t][out_k[i]] = (float(st12_conv[i]) * prob_t2, 0)

                        print("t : ", t)
                        f.flush()
                        
                        # sds = list(st12[t].keys())
                        # sds.sort()                        
                        # for s in sds:
                        #         f.write(str(t) + ' ' + str(s) + ' ' + str(st12[t][s][0]) + ' ' + str(st12[t][s][1]) + "\n")


                        del st12[t]
                                

# Get interference hit rate for each TC
def get_int_hrc():
	pass

# Merge st for fd-add
def merge_st(st, st_new, sd_gran):
	for t in st.keys():
		prob_sum = sum([v[0] for v in st[t].values()])
		sd = 0
		for s in st[t].keys():
			sd += s * (st[t][s][0] / prob_sum)
		st_new[t] = {}
		sd = max((sd // sd_gran) * sd_gran, sd_gran)		
		st_new[t][sd] = (prob_sum, 0)

# FD-add - GENERALIZED
def fd_add(st1, st2, st12, rate1, rate2, sd_gran):
	st1_new = {}
	st2_new = {}
	merge_st(st1, st1_new, sd_gran)
	merge_st(st2, st2_new, sd_gran)
	t_set = sorted(set(list(st1_new.keys()) + list(st2_new.keys())))
	for t in t_set:
		t1_f = floor(sorted(set(st1_new.keys())), t)
		t2_f = floor(sorted(set(st2_new.keys())), t)
		std1 = int(list(st1_new[t1_f].keys())[0])
		std2 = int(list(st2_new[t2_f].keys())[0])
		#print(t, sd1, sd2)
		std = std1 + std2
		prob1 = st1_new[t1_f][std1][0] if t in st1_new.keys() else 0
		prob2 = st2_new[t2_f][std2][0] if t in st2_new.keys() else 0
		prob12 = ((prob1 * rate1) + (prob2 * rate2))/(rate1 + rate2)
		st12[t] = {}
		st12[t][std] = (prob12, 0) # (req frac, bytes frac) 
		#print(std, std1, std2)

# Brute force addition of stack distance curves
def brute_force_addition(sd1, sd2, sd12, rate1, rate2, sd_gran):
	for s1 in sd1:
		s2 = floor(sorted(set(sd2.keys())), s1)
		sd = ((s1 + s2) // sd_gran) * sd_gran
		sd12[s1 + s2] = ((rate1 * sd1[s1][0] + rate2 * sd2[s2][0]) / (rate1 + rate2), 0) # ONLY ohr

"""
# Brute force addition of stack distance curves -- add capacities that have same hit rate
def strawman_addition(sd1, sd2, sd12, rate1, rate2, sd_gran):
	for s1 in sd1:
		s2 = floor(sorted(set(sd2.keys())), s1)
		sd = ((s1 + s2) // sd_gran) * sd_gran
		sd12[s1 + s2] = ((rate1 * sd1[s1][0] + rate2 * sd2[s2][0]) / (rate1 + rate2), 0) # ONLY ohr
"""

# Simple scale
def simple_scale(st, delta, N1_frac, st_new):
	#for t in st.keys():
	#	st_new[t / delta] = copy.deepcopy(st[t])
	# Scale and renormalize
	for t in st.keys():
		t_s = t / delta
		if t_s not in st_new:
			st_new[t_s] = {}
		for s in st[t].keys():
			#if s not in st_new[t_s]:
				#st_new[t_s][s] = (0, 0)
			#st_new[t_s][s] = (st[t][s][0] * (1 + N1_frac), st[t][s][1] * (1 + N1_frac))
			st_new[t_s][s] = (st[t][s][0] * (1), st[t][s][1] * (1))

# st generator - st[t][s] = (req_frac, bytes_frac)
def st_gen(st, trace, iat_gran, sd_gran, rb_total):
	req_total = 0
	bytes_total = 0


        ii = 0
	with open(trace, 'r') as f:
		for l in f:
			l = l.split()

                        if l[0] == '#':
                                req_total = int(l[2])
                                bytes_total = int(float(l[4]))
                                rb_total.append((req_total, bytes_total))

                        else:
                                ii += 1
                                t = (float(l[0]) // iat_gran) * iat_gran
                                sd = max((int(float(l[1])) // sd_gran) * sd_gran, sd_gran)
                                req_frac = float(l[3])
                                bytes_frac = float(l[3])
                                if t not in st:
                                        st[t] = {}
                                if sd not in st[t]:
                                        st[t][sd] = [0, 0]   
                                st[t][sd][0] += req_frac
                                st[t][sd][1] += bytes_frac

if __name__ == "__main__":
	random.seed(1988)
	# if len(sys.argv) != 6:
	# 	print("USAGE:", sys.argv[0], "<stdtime_1> <rate1> <stdtime_2> <rate2> <out_name> <int_hrc_1> <int_hrc_2>")
	# 	#print("USAGE:", sys.argv[0], "<trace_st1> <rate1> <trace_st2> <rate2> <trace_st12>")
	# 	sys.exit(0)

	# # Input files
	# trace_st1 = sys.argv[1]
	# rate1 = float(sys.argv[2])
	# trace_st2 = sys.argv[3]
	# rate2 = float(sys.argv[4])
	# out_name = sys.argv[5]
	# #int_hrc_1 = sys.argv[6]
	# #int_hrc_2 = sys.argv[7]
	# # Output files
	# stdtime_out = "stdtime." + out_name
	# stdspace_out = "stdspace." + out_name


        dir1 = "/mnt/nfs/scratch1/asabnis/data/binary/small/" + str(sys.argv[1])
        dir2 = "/mnt/nfs/scratch1/asabnis/data/binary/small/" + str(sys.argv[2])
        
        trace_st1 = dir1 + "/st_out"
        trace_st2 = dir2 + "/st_out"

        f = open(dir1 + "/bytes.txt", "r")
        l = f.readline()
        l = l.strip().split(" ")
        l = [int(x) for x in l]
        td1 = (int(l[1]) - int(l[0]))
        rate1 = float(l[2])/td1

        bytes1 = float(l[2])
        min_tm = int(l[0])
        max_tm = int(l[1])


        f.close()


        f = open(dir2 + "/bytes.txt", "r")
        l = f.readline()
        l = l.strip().split(" ")
        l = [int(x) for x in l]
        td2 = (int(l[1]) - int(l[0]))
        rate2 = float(l[2])/td2

        bytes2 = float(l[2])
        if int(l[0]) < min_tm:
                min_tm = int(l[0])

        if int(l[1]) > max_tm:
                max_tm = int(l[1])

        f.close()


        lvl = sys.argv[3]
        out_dr = "/mnt/nfs/scratch1/asabnis/data/binary/small/" + str(lvl) + "_" + str(int((int((sys.argv[1]).split("_")[-1])/2)))        
        

        if not os.path.exists(out_dr):
                os.mkdir(out_dr)
                                                        

        print(str(int((int((sys.argv[1]).split("_")[-1])/2))))

	"""
	# Output trace files
	stdtime_st1 = "stdtime2." + str(trace_st1.split('.')[1])
	stdspace_st1 = "stdspace2." + str(trace_st1.split('.')[1])
	stdtime_st2 = "stdtime2." + str(trace_st2.split('.')[1])
	stdspace_st2 = "stdspace2." + str(trace_st2.split('.')[1])
	stdtime_out = "stdtime2." + str(trace_st1.split('.')[1]) + "." + str(trace_st2.split('.')[1])
	stdspace_out = "stdspace2." + str(trace_st1.split('.')[1]) + "." + str(trace_st2.split('.')[1])
	stdtime_actual = "stdtime2." + str(trace_st1.split('.')[1]) + "." + str(trace_st2.split('.')[1]) + ".actual"
	stdspace_actual = "stdspace2." + str(trace_st1.split('.')[1]) + "." + str(trace_st2.split('.')[1]) + ".actual"
	stdtime_fa = "stdtime2." + str(trace_st1.split('.')[1]) + "." + str(trace_st2.split('.')[1]) + ".fa"
	stdspace_fa = "stdspace2." + str(trace_st1.split('.')[1]) + "." + str(trace_st2.split('.')[1]) + ".fa"
	"""


	# Keep track of req_total and bytes_total for all maps; 0 - mr1, 1 - mr2, 2 - mr1.mr2
	#rb_total = [[num_lines1, rate1], [num_lines1, rate2]]
        rb_total = []
        out_name = out_dr + "/st_out"

	# IAT and stack distance granularity
	iat_gran = 200
	sd_gran = 100000
	# st (stdtime)
	st1 = {}
	st_gen(st1, trace_st1, iat_gran, sd_gran, rb_total)
	st2 = {}
	st_gen(st2, trace_st2, iat_gran, sd_gran, rb_total)


        print("Reading ST done\n")


	st12 = {}
	# Scale
	delta = 1
	r = rb_total[0][0] + rb_total[1][0]
	b = rb_total[0][1] + rb_total[1][1]
	rb_total.append((r, b))

	# Intereference st
	st1_int = {}
	st2_int = {}
	convolve_2d_fft(st1, st2, st12, st1_int, st2_int, rate1, rate2, sd_gran, out_name, rb_total[2])
	
	# Fprint stdtime.mr1.mr2
	#f_print_out_st(outname, st12, rb_total[2])

        f = open(out_dr + "/bytes.txt", "w")
        f.write(str(min_tm) + " " + str(max_tm) + " " + str(bytes1 + bytes2))
        f.close()
