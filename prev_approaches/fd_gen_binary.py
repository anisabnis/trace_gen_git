#!/usr/local/bin/python3
"""
Compute FD
"""

import sys, math, random, copy, gzip
import multiprocessing as mp
#from Utils import StackDistance
from StackDistance import *
import struct
import logging

# Print key value from dict (for stdspace)
def f_print_out_sd(f_out, sd, rb_total):
	with open(f_out, 'w') as f:
		f.write("# r " + str(rb_total[0]) + ' b ' + str(rb_total[1]) + "\n")
		#f.write("#" + ' ' + str(rb_total[0]) + ' ' + str(rb_total[1]) + "\n")
		for k in sorted(list(sd.keys())):
			f.write(str(k) + ' ' + str(sd[k][0]) + ' ' + str(sd[k][1]) + "\n")

# Print stdtime
def f_print_out_st(f_out, st, rb_total):
	with open(f_out, 'w') as f:
		f.write("# r " + str(rb_total[0]) + ' b ' + str(rb_total[1]) + "\n")		
		#f.write("#" + ' ' + str(rb_total[0]) + ' ' + str(rb_total[1]) + "\n")
		for t in sorted(st.keys()):
			for s in sorted(st[t].keys()):
				f.write(str(t) + ' ' + str(s) + ' ' + str(st[t][s][0]) + ' ' + str(st[t][s][1]) + "\n")

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

# Merge st for fd_add
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
def fd_add(st_dict, st_out, rate_dict, sd_gran):
	# Merge st
	st_new_dict = {}
	for k in st_dict.keys():
		st_new_dict[k] = {}
		merge_st(st_dict[k], st_new_dict[k], sd_gran)
	# Get t_set
	t_set = []
	for k in st_new_dict.keys():
		t_set += st_new_dict[k].keys()
	t_set = set(t_set)
	# Sorted scaled t_j's
	sorted_t = {}
	for k in st_new_dict.keys():
		sorted_t[k] = sorted(set(st_new_dict[k].keys()))

	# Addition
	for t in t_set:
		c_tmp = 0
		# Output prob
		prob_dict = {}
		for k in st_new_dict.keys():
			#t_floor = floor(sorted(set(st_new_dict[k].keys())), t)
			t_floor = floor(sorted_t[k], t)
			c_floor = int(list(st_new_dict[k][t_floor].keys())[0])
			prob_dict[k] = st_new_dict[k][t_floor][c_floor][0] if t in st_new_dict[k].keys() else 0
			c_tmp += c_floor
		prob_out = 0
		for k in st_new_dict.keys():
			prob_out += prob_dict[k] * rate_dict[k]
		prob_out /= sum(rate_dict.values())
		# Output st
		st_out[t] = {}
		st_out[t][c_tmp] = (prob_out, prob_out) # (req frac, bytes frac)

# st generator
def st_gen(trace_list, sd_gran, iat_gran, st):
	#arrivals = copy.deepcopy(arrivals_orig)
	pop = {} # (key, value) = (oid, lat)
	count = 0 # object count
	bytes = 0 # total bytes
	# Stack distance
	sd_multiple = sd_gran
	stackDistance1 = SDHitrate(100, 10, sd_multiple) # 100 - bytelimit (not required!)
	for l in trace_list:	
		count += 1
		w = l
		t = float(w[0])
		oid = (w[1])
		osize = int(w[2])
		bytes += osize
		iat = -1
		# Update stack distance
		sd = max((stackDistance1.updateHist(oid, osize, 1, False, 0) // sd_gran) * sd_gran, sd_gran) # 0=time, min sd = sd_gran
		#sd = stackDistance1.updateHist(oid, 1, 1, False, 0)
		if oid in pop:
			iat = ((t - pop[oid]) // iat_gran) * iat_gran
		pop[oid] = t
		if iat not in st:
			st[iat] = {}
		if sd not in st[iat]:
			st[iat][sd] = (0, 0)
		c, b = st[iat][sd]
		st[iat][sd] = (c + 1, b + osize) 
	# st pdf
	for t in st.keys():
		for s in st[t].keys():
			#ohr, bhr = st[t][s]
			st[t][s] = (st[t][s][0] / count, st[t][s][1] / bytes)
	# Delete iat 0 -- CHECK?
	del(st[-1])	
	return (count, bytes)

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('USAGE: ', sys.argv[0], '<input-trace>')
		sys.exit(0)

	trace_in = sys.argv[1]

	trace_l = []
# 	with open(trace_in, 'r') as f:
# 		for l in f:
# 			w = l.strip().split()
# 			if w[0] != "#":
# 				trace_l.append(l)


	curr_time = 0
	req_per_sec = 0
	req_rate = []

	cnt = 0
	s = struct.Struct("III")
	with open(trace_in, "rb") as ifile:
		        b = ifile.read(12)
			while b:
				cnt += 1

				if cnt >= 140000000:
					break

				if cnt % 100000000 == 0:
					print("Number of lines : ", cnt)

				r = s.unpack(b)
				

				if cnt > 100000000:
					trace_l.append(r)

				if int(r[0]) != curr_time:
					req_rate.append(req_per_sec)
					req_per_sec = 0
					curr_time = int(r[0])
				else:
					req_per_sec += 1					

				b = ifile.read(12)


	file_req_rate = open("data/req_rate.txt", "w")
	for r in req_rate:
		file_req_rate.write(str(r) + "\n")
	file_req_rate.close()

	rb_total = []
	st = {}
	sd_gran = 200
	iat_gran = 1
	c, b = st_gen(trace_l, sd_gran, iat_gran, st)
	rb_total.append((c, b))
	# Calculate sd
	sd = {}
	st_2_sd(st, sd)
	pdf_2_cdf_sd(sd)

	# Print st
	st_f = 'st_out'
	f_print_out_st(st_f, st, rb_total[0])
	# Print sd
	sd_f = 'sd_out'
	f_print_out_sd(sd_f, sd, rb_total[0])
