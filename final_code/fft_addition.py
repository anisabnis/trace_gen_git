
#! /Users/asundar/.local/bin/python3

"""
FFT addition - read stdtime as input and output stdtime and stdspace of mixed traffic
"""

import random, sys, math, copy
import numpy as np
import scipy as sp
import scipy.signal
from scipy.optimize import linprog, brentq
import numpy.fft as fft
sys.path.append('Utils')
import StackDistance
import cmath

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
	with open(f_out, 'w') as f:
		f.write("# r " + str(rb_total[0]) + ' b ' + str(rb_total[1]) + "\n")		
		#f.write("#" + ' ' + str(rb_total[0]) + ' ' + str(rb_total[1]) + "\n")
		for t in sorted(st.keys()):
			for s in sorted(st[t].keys()):
				f.write(str(t) + ' ' + str(s) + ' ' + str(st[t][s][0]) + ' ' + str(st[t][s][1]) + "\n")

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
def convolve_2d_fft(st1, st2, st12, st1_int, st2_int, rate1, rate2, sd_gran):
	# Determine conditional probabilties of st1 and st2
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
			#for i in range(min_st1_s, max_st1_s + 1, sd_gran):
			#	for j in range(min_st2_s, max_st2_s + 1, sd_gran):
			#		out_k.add(i + j)
			#		if (i in st1_c.keys()) and (j in st2_c.keys()):
			#			out_k2.add(i + j)
			#out_k = sorted(out_k)
			#out_k2 = sorted(out_k2)
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
				st12[t][out_k[i]] = (float(st12_conv[i]) * prob_t12[0], float(st12_conv[i]) * prob_t12[0])
				# Interference hit rates
				#st12[t][out_k[i]] = (float(st12_conv[i]) * prob_t1, 0)
				st1_int[t][out_k[i]] = (float(st12_conv[i]) * prob_t1, 0)
				st2_int[t][out_k[i]] = (float(st12_conv[i]) * prob_t2, 0)

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
def st_gen(st, trace, iat_gran, sd_gran, rb_total, rates, times):
        req_total = 0
	bytes_total = 0
	with open(trace, 'r') as f:
                for l in f:
			l = l.split()
			if l[0] == '#':
		                req_total = int(l[0])
			        bytes_total = int(float(l[1]))
                                total_rate = bytes_total/(int(l[3]) - int(l[2]))
                                times.append((int(l[2], int(l[3])))
                                rates.append(total_rate)                                
				rb_total.append((req_total, bytes_total))
			else:
				t = (float(l[0]) // iat_gran) * iat_gran
				#t = float(max((float(l[0]) // iat_gran) * iat_gran, iat_gran))
				#t = float(l[0])
				sd = max((int(float(l[1])) // sd_gran) * sd_gran, sd_gran)
				req_frac = float(l[2])
				bytes_frac = float(l[2])
				if t not in st:
					st[t] = {}
				if sd not in st[t]:
					st[t][sd] = [0, 0]   
				st[t][sd][0] += req_frac
				st[t][sd][1] += bytes_frac

if __name__ == "__main__":
	random.seed(1988)
	if len(sys.argv) != 6:
		print("USAGE:", sys.argv[0], "<stdtime_1> <stdtime_2> <traffic_frac1> <traffic_frac2> <out_name>")
		#print("USAGE:", sys.argv[0], "<trace_st1> <rate1> <trace_st2> <rate2> <trace_st12>")
		sys.exit(0)

	# Input files
	trace_st1 = sys.argv[1]
	trace_st2 = sys.argv[2]
        rate1 = float(sys.argv[3])
        rate2 = float(sys.argv[4])
	out_name = sys.argv[5]

	# Output files
	stdtime_out = "stdtime." + out_name
	stdspace_out = "stdspace." + out_name
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
	rb_total = []
        rates = []
        times = []

	# IAT and stack distance granularity
	iat_gran = 1
	sd_gran = 1

	# st (stdtime)
	st1 = {}
	st_gen(st1, trace_st1, iat_gran, sd_gran, rb_total, rates, times)
	st2 = {}
	st_gen(st2, trace_st2, iat_gran, sd_gran, rb_total, rates, times)

        rate1 = rate1 * rates[0]
        rate2 = rate2 * rates[1]
	# Merged trace st12_v to get actual output
	#st12_v = {}
	#st_gen(st12_v, trace_st12, iat_gran, sd_gran, rb_total)
	# Convolution using fft -- TRY only request convolution first
	st12 = {}
	#print('HERE')

	# Scale
	delta = 1
	#N1_frac = 1
	#st1_s = {}
	#simple_scale(st1, delta, N1_frac, st1_s)
	#st1 = copy.deepcopy(st1_s)

	r = rb_total[0][0] + rb_total[1][0]
	b = rb_total[0][1] + rb_total[1][1]
	rb_total.append((r, b))
	# Intereference st
	st1_int = {}
	st2_int = {}
	convolve_2d_fft(st1, st2, st12, st1_int, st2_int, rate1, rate2, sd_gran)
	# Convolution 2d-- TRY only request hit rate first
	#st12_2d = {}
	#convolve_2d(st1, st2, st12_2d, rate1, rate2, sd_gran)
	# fd-add
	#st12_fa = {}
	#fd_add(st1, st2, st12_fa, rate1, rate2, sd_gran)

	#sd12 = {}
	#st_2_sd(st12, sd12)
	#pdf_2_cdf_sd(sd12)
	#print(sd12[80][0])

	#sd12_fa = {}
	#st_2_sd(st12_fa, sd12_fa)
	#pdf_2_cdf_sd(sd12_fa)
	#print(sd12_fa[80][0])

	#sys.exit(0)

	"""
	# Fprint stdtime.mr1
	f_print_out_st(stdtime_st1, st1, rb_total[0])
	# Fprint stdspace.mr1
	sd1 = {}
	st_2_sd(st1, sd1)
	pdf_2_cdf_sd(sd1)
	f_print_out_sd(stdspace_st1, sd1, rb_total[0])
	
	# Fprint stdtime.mr2
	f_print_out_st(stdtime_st2, st2, rb_total[1])
	# Fprint stdspace.mr2
	sd2 = {}
	st_2_sd(st2, sd2)
	pdf_2_cdf_sd(sd2)
	f_print_out_sd(stdspace_st2, sd2, rb_total[1])
	"""

	
	# Fprint stdtime.mr1.mr2
	f_print_out_st(stdtime_out, st12, rb_total[2])
	# Fprint stdspace.mr1.mr2.actual
	sd12 = {}
	st_2_sd(st12, sd12)
	pdf_2_cdf_sd(sd12)
	f_print_out_sd(stdspace_out, sd12, rb_total[2])
	# Fprint int_hrc_1
	#sd1_int = {}
	#st_2_sd(st1_int, sd1_int)
	#pdf_2_cdf_sd(sd1_int)
	#f_print_out_sd("stdspace." + int_hrc_1, sd1_int, rb_total[2])
	# Fprint int_hrc_2
	#sd2_int = {}
	#st_2_sd(st2_int, sd2_int)
	#pdf_2_cdf_sd(sd2_int)
	#f_print_out_sd("stdspace." + int_hrc_2, sd2_int, rb_total[2])
	

	"""
	# Fprint stdtime.mr1.mr2.actual
	f_print_out_st(stdtime_actual, st12_v, rb_total[2])
	# Fprint stdspace.mr1.mr2.actual
	sd12_v = {}
	st_2_sd(st12_v, sd12_v)
	pdf_2_cdf_sd(sd12_v)
	f_print_out_sd(stdspace_actual, sd12_v, rb_total[2])
	
	# Fprint stdtime.mr1.mr2.fa
	f_print_out_st(stdtime_fa, st12_fa, rb_total[2])
	# Fprint stdspace.mr1.mr2.fa
	sd12_fa = {}
	st_2_sd(st12_fa, sd12_fa)
	pdf_2_cdf_sd(sd12_fa)
	f_print_out_sd(stdspace_fa, sd12_fa, rb_total[2])
	"""
	# Fprint brute force - ONLY stack distance
	#sd12_bf = {}
	#brute_force_addition(sd1, sd2, sd12_bf, rate1, rate2, sd_gran)
	#stdspace_bf = stdspace_out + '.bf'
	#f_print_out_sd(stdspace_bf, sd12_bf, rb_total[2])



