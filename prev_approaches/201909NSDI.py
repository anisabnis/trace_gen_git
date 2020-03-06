

import os, sys, time, pickle, math, json
import logging
import copy
from multiprocessing import Process
import struct
from collections import defaultdict

sys.path.append(os.path.expanduser("~/GDCMU/1900JPlot/"))
sys.path.append(os.path.expanduser("~/1900JPlot/"))
import JPlot
JPlot.set_plot_style("publication-twocol-largeFont")
JPlot.set_auto_open(False)
import JPlot.pyplot as plt


logging.basicConfig(format='%(asctime)s: %(levelname)s: \t%(message)s', level=logging.INFO, datefmt='%H:%M:%S')

KB = 1000
MB = 1000*1000
GB = 1000*1000*1000
GiB = 1024*1024*1024

if not os.path.exists("data"):
    os.mkdir("data")


########################## popularity ###########################
#### see 201907Popularoty.py  ####



######################### request size ##########################
def cal_size_distribution(dat, req=True, obj=True):
    sz_cnt_req = defaultdict(int)
    sz_cnt_obj = defaultdict(int)

    if os.path.exists("data/{}.sizeCntObj.json".format(dat.split("/")[-1])):
        if obj:
            with open("data/{}.sizeCntObj.json".format(dat.split("/")[-1])) as ifile:
                sz_cnt_obj = json.load(ifile)
        if req:
            with open("data/{}.sizeCntReq.json".format(dat.split("/")[-1])) as ifile:
                sz_cnt_req = json.load(ifile)
        return sz_cnt_req, sz_cnt_obj


    seen_obj = set()
    cnt = 0

    s = struct.Struct("III")
    with open(dat, "rb") as ifile:
        b = ifile.read(12)
        while b:
            cnt += 1
            if cnt % 100000000 == 0:
                logging.info("calculated {}".format(cnt))
            r = s.unpack(b)
            sz = r[2]
            sz_cnt_req[sz] += 1
            if r[1] not in seen_obj:
                sz_cnt_obj[sz] += 1
                seen_obj.add(r[1])
            b = ifile.read(12)

    with open("data/{}.sizeCntObj.json".format(dat.split("/")[-1]), "w") as ofile:
        json.dump(sz_cnt_obj, ofile)
    with open("data/{}.sizeCntReq.json".format(dat.split("/")[-1]), "w") as ofile:
        json.dump(sz_cnt_req, ofile)

    return sz_cnt_req, sz_cnt_obj


def plot_req_size_distr_cdf(dat1, dat2, logbase=1.008):
    sz_cnt_req1, _ = cal_size_distribution(dat1, req=True, obj=False)
    sz_cnt_req2, _ = cal_size_distribution(dat2, req=True, obj=False)
    max_sz1 = max([int(i) for i in sz_cnt_req1.keys()])
    max_sz2 = max([int(i) for i in sz_cnt_req2.keys()])
    logging.info("max size {} {}".format(max_sz1, max_sz2))

    y1 = [0] * (int(math.log(max_sz1, logbase)) + 1)
    for sz, cnt in sorted(sz_cnt_req1.items(), key=lambda x:x[0]):
        y1[int(math.log(int(sz), logbase))] += cnt
    for i in range(1, len(y1)):
        y1[i] = y1[i] + y1[i-1]
    for i in range(len(y1)):
        y1[i] = y1[i] / y1[-1]

    y2 = [0] * (int(math.log(max_sz2, logbase)) + 1)
    for sz, cnt in sorted(sz_cnt_req2.items(), key=lambda x:x[0]):
        y2[int(math.log(int(sz), logbase))] += cnt
    for i in range(1, len(y2)):
        y2[i] = y2[i] + y2[i-1]
    for i in range(len(y2)):
        y2[i] = y2[i] / y2[-1]

    plt.semilogx([logbase**i for i in range(0, len(y2))], y2, label="video")
    plt.semilogx([logbase**i for i in range(0, len(y1))], y1, label="web")
    plt.xlabel("Object Size")
    plt.grid()
    plt.yticks((0, 0.25, 0.5, 0.75, 1))
    plt.xticks((KB, MB, GB), ("1 KB", "1 MB", "1 GB"))
    plt.ylabel("Fraction of request (CDF)")
    plt.legend()
    plt.savefig("reqSz")
    plt.clf()


def plot_req_size_traffic_cdf(dat1, dat2, logbase=1.008):
    COLOR = plt.set_n_colors(2)
    sz_cnt_req_video, _ = cal_size_distribution(dat1, req=True, obj=False)
    max_sz1 = max([int(i) for i in sz_cnt_req_video.keys()])

    x_video, y_video = zip(*(list(sorted(sz_cnt_req_video.items(), key=lambda x: int(x[0])))))
    x_video_req, y_video_req = [int(i) for i in x_video], [int(i) for i in y_video]
    for i in range(1, len(y_video_req)):
        y_video_req[i] = y_video_req[i] + y_video_req[i-1]
    for i in range(len(y_video_req)):
        y_video_req[i] = y_video_req[i] / y_video_req[-1]
    plt.semilogx(x_video_req, y_video_req, label="request count (video)", nomarker=True, color=next(COLOR))

    plt.axvline(x=128*KB, linestyle="dotted", linewidth=4, color="k")
    plt.xlabel("Request Size")
    plt.grid(linestyle="--")
    plt.yticks((0, 0.25, 0.5, 0.75, 1))
    plt.xlim(1, 8*GB)
    plt.xticks((KB, MB, GB), ("1 KB", "1 MB", "1 GB"))
    plt.ylabel("CDF")
    plt.legend(loc="upper left")
    plt.savefig("reqnoTraffic_video")

    x_video_traffic, y_video_traffic = [int(i) for i in x_video], [int(y_video[i])*int(x_video[i]) for i in range(len(y_video))]
    for i in range(1, len(y_video_traffic)):
        y_video_traffic[i] = y_video_traffic[i] + y_video_traffic[i-1]
    for i in range(len(y_video_traffic)):
        y_video_traffic[i] = y_video_traffic[i] / y_video_traffic[-1]
    plt.semilogx(x_video_traffic, y_video_traffic, label="request byte (video)", nomarker=True, color=next(COLOR))


    plt.xlabel("Request Size")
    plt.grid(linestyle="--")
    plt.yticks((0, 0.25, 0.5, 0.75, 1))
    plt.xlim(1, 8*GB)
    plt.xticks((KB, MB, GB), ("1 KB", "1 MB", "1 GB"))
    plt.ylabel("CDF")
    plt.legend(loc="upper left")
    plt.savefig("reqTraffic_video")
    plt.clf()


    COLOR = plt.set_n_colors(2)
    sz_cnt_req_web, _ = cal_size_distribution(dat2, req=True, obj=False)
    max_sz2 = max([int(i) for i in sz_cnt_req_web.keys()])

    x_web, y_web = zip(*(list(sorted(sz_cnt_req_web.items(), key=lambda x: int(x[0])))))
    x_web_req, y_web_req = [int(i) for i in x_web], [int(i) for i in y_web]
    for i in range(1, len(y_web_req)):
        y_web_req[i] = y_web_req[i] + y_web_req[i-1]
    for i in range(len(y_web_req)):
        y_web_req[i] = y_web_req[i] / y_web_req[-1]
    plt.semilogx(x_web_req, y_web_req, label="request count (web)", nomarker=True, color=next(COLOR))

    plt.axvline(x=128*KB, linestyle="dotted", linewidth=4, color="k")
    plt.xlabel("Request Size")
    plt.grid(linestyle="--")
    plt.yticks((0, 0.25, 0.5, 0.75, 1))
    plt.xlim(1, 8*GB)
    plt.xticks((KB, MB, GB), ("1 KB", "1 MB", "1 GB"))
    plt.ylabel("CDF")
    plt.legend(loc="upper left")
    plt.savefig("reqnoTraffic_web")


    x_web_traffic, y_web_traffic = [int(i) for i in x_web], [int(y_web[i])*int(x_web[i]) for i in range(len(y_web))]
    for i in range(1, len(y_web_traffic)):
        y_web_traffic[i] = y_web_traffic[i] + y_web_traffic[i-1]
    for i in range(len(y_web_traffic)):
        y_web_traffic[i] = y_web_traffic[i] / y_web_traffic[-1]
    plt.semilogx(x_web_traffic, y_web_traffic, label="request byte (web)", nomarker=True, color=next(COLOR))


    plt.xlabel("Request Size")
    plt.grid(linestyle="--")
    plt.yticks((0, 0.25, 0.5, 0.75, 1))
    plt.xlim(1, 8*GB)
    plt.xticks((KB, MB, GB), ("1 KB", "1 MB", "1 GB"))
    plt.ylabel("CDF")
    plt.legend(loc="upper left")
    plt.savefig("reqTraffic_web")
    plt.clf()



#########################


if __name__ == "__main__":
    dat1 = "/home/jason/data/akamai/nodeID/akamai.bin"
    dat2 = "/home/jason/data/akamai/video/akamai2.bin"

    # cal_size_distribution(dat1)
    # cal_size_distribution(dat2)
    # plot_req_size_distr_cdf(dat1, dat2)

    plot_req_size_traffic_cdf(dat2, dat1)


