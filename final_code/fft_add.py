import random, sys, math, copy
import numpy as np
import scipy as sp
import scipy.signal
from scipy.optimize import linprog, brentq
import numpy.fft as fft
import cmath

TB = 1000000000
epsilon=0

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

def f_get_frac_misses(f_out, st, rb_total, res_fd, times, misses, time_lt, sd_lt, b_misses):
    frac_misses = 0        
    
    for t in sorted(st.keys()):
        for s in sorted(st[t].keys()):
            if s > sd_lt or t > time_lt:
                frac_misses += st[t][s][0]

    return frac_misses, frac_misses

# Print stdtime
def f_print_out_st(f_out, st, rb_total, res_fd, times, misses, frac_misses, b_misses, frac_b_misses):

    with open("results/" + str(res_fd) + "/" + f_out , 'w') as f:
        
        f.write(str(rb_total[0]) + " " + str(rb_total[1]) + " " + str(times[0]) + " " + str(times[1]) + " " + str(misses + int(frac_misses * rb_total[0])) + " " + str(b_misses + int(frac_misses * rb_total[1])) + "\n")
    
        for t in sorted(st.keys()):
                for s in sorted(st[t].keys()):
                    if s <= sd_lt and t <= time_lt:
                        if st[t][s][0] > epsilon:
                            f.write(str(t) + ' ' + str(s) + ' ' + str(st[t][s][0]) + "\n")


# Determine conditional distribution, conditioned on t
def cond_prob(st):

    for t in st.keys():

     prob_sum_st = sum([v[0] for v in st[t].values()])

     for s in st[t].keys():
         st[t][s] = [st[t][s][0] / prob_sum_st, st[t][s][0] / prob_sum_st] if prob_sum_st else [0, 0]


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
        
        prob_t1 = sum([v[0] for v in st1[t].values()]) if t in st1 else 0
        prob_t2 = sum([v[0] for v in st2[t].values()]) if t in st2 else 0
     
        prob_t12 = (((rate1 / (rate1 + rate2)) * prob_t1) + ((rate2 / (rate1 + rate2)) * prob_t2), 0)

        st12[t] = {}
        st1_int[t] = {}
        st2_int[t] = {}

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

        print("convolving for time : ", t," and len : ", len(st12_conv))
        
        for i in range(len(st12_conv)):            
            st12[t][out_k[i]] = (float(st12_conv[i]) * prob_t12[0], float(st12_conv[i]) * prob_t12[0])
            st1_int[t][out_k[i]] = (float(st12_conv[i]) * prob_t1, 0)
            st2_int[t][out_k[i]] = (float(st12_conv[i]) * prob_t2, 0)


# st generator - st[t][s] = (req_frac, bytes_frac)
def st_gen(st, trace, iat_gran, sd_gran, rb_total, rates, times, res_dir, misses, b_misses):

    req_total = 0
    bytes_total = 0

    normalizing_factor = 0
    with open("results/" + str(res_dir) + "/" + trace, 'r') as f:

        l = f.readline().strip().split(" ")

        req_total = int(l[0])
        bytes_total = int(float(l[1]))
        total_rate = bytes_total/(int(l[3]) - int(l[2]))

        times.append((int(l[2]), int(l[3])))
        rates.append(total_rate)                                
        rb_total.append((req_total, bytes_total))

        misses.append(int(l[4]))
        b_misses.append(int(float(l[5])))
        
        t = -1
        
        for l in f:

            l = l.strip().split()
            t = (float(l[0]) // iat_gran) * iat_gran
                
            sd = (int(float(l[1])) // sd_gran) * sd_gran
            req_frac = float(l[2])
            bytes_frac = float(l[2])
            
            if t not in st:
                st[t] = {}

            if sd not in st[t]:
                st[t][sd] = [0, 0]   

            st[t][sd][0] += req_frac
            st[t][sd][1] += bytes_frac

            normalizing_factor += req_frac

    # for t in st:
    #     for sd in st[t]:
    #         st[t][sd][0] = float(st[t][sd][0])/normalizing_factor
    #         st[t][sd][1] = float(st[t][sd][1])/normalizing_factor


            
if __name__ == "__main__":
    random.seed(1990)

    if len(sys.argv) != 7:
        print("USAGE:", sys.argv[0], "<stdtime_1> <stdtime_2> <traffic_frac1> <traffic_frac2> <out_name> <res_dir>")
        sys.exit(0)

    trace_st1 = sys.argv[1]
    trace_st2 = sys.argv[2]
    rate1 = float(sys.argv[3])
    rate2 = float(sys.argv[4])
    out_name = sys.argv[5]
    res_dir = sys.argv[6]

    if res_dir == "v" or res_dir =="tc":
        time_lt = 4000000
        sd_lt   = 100 * TB
    else:
        time_lt = 40000
        sd_lt   = 25 * TB
    
    stdtime_out = out_name

    rb_total = []
    rates = []
    times = []
    misses = []
    b_misses = []
    
    # IAT and stack distance granularity
    iat_gran = 200
    sd_gran = 200000

    # st (stdtime)
    st1 = {}
    st_gen(st1, trace_st1, iat_gran, sd_gran, rb_total, rates, times, res_dir, misses, b_misses)

    st2 = {}
    st_gen(st2, trace_st2, iat_gran, sd_gran, rb_total, rates, times, res_dir, misses, b_misses)

    rate1 = rate1 * rates[0]
    rate2 = rate2 * rates[1]

    total_misses = misses[0] + misses[1]
    b_total_misses = b_misses[0] + b_misses[1]
    
    st12 = {}

    # Scale
    r = rb_total[0][0] + rb_total[1][0]
    b = rb_total[0][1] + rb_total[1][1]
    rb_total.append((r, b))
    times.append((min(times[0][0], times[1][0]), max(times[0][1], times[1][1])))
    
    # Intereference st
    st1_int = {}
    st2_int = {}
    convolve_2d_fft(st1, st2, st12, st1_int, st2_int, rate1, rate2, sd_gran)

    frac, frac_b = f_get_frac_misses(stdtime_out, st12, rb_total[2], res_dir, times[2], total_misses, time_lt, sd_lt, b_total_misses)

    print("frac : ", frac)
    
    f_print_out_st(stdtime_out, st12, rb_total[2], res_dir, times[2], total_misses, frac, b_total_misses, frac_b)


