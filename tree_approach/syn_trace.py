import sys
from treelib import *
from collections import defaultdict
from gen_trace import *
from obj_size_dst import *
from obj_pop_dst import *
from parse_fd import *
import datetime

if __name__ == "__main__":
            
    t_len = int(sys.argv[1])
    no_objects = int(sys.argv[2])

