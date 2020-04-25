from popularity import *
from obj_size_dst import *
import sys
from util_theory import *

class node:
    def __init__(self, lvl, index, val):        
        self.val = val
        self.lvl = lvl
        self.id = index
        self.children = []

    def add_child(self, n):
        self.children.append(n)

    def del_child(self, n):
        self.children = [c for c in self.children if c.id != n.id]

    def assign_parent(self, n):
        self.parent = n


def init_trace(trace, obj_sizes):
    node_trace = [[]]
    for i in range(len(trace)):
        n = node(0, i, obj_sizes[trace[i]])
        node_trace[0].append(n)
    return node_trace

def gen_node_tree(node_trace):
    lvl = 0
    while len(node_trace[lvl]) > 1 :
        node_trace.append([])
        index = 0
        #for i in range(int(len(node_trace[lvl]))/2):
        for i in range(int(len(node_trace[lvl])/2)):

            ## make n1 and n2 siblings
            n1 = node_trace[lvl][2*i]
            n2 = node_trace[lvl][2*i+1]        

            ## new node is the parent
            new_node = node(lvl+1, index, n1.val + n2.val)

            ## Assign parents            
            n1.assign_parent(new_node)

            ## Assign children            
            new_node.add_child(n1)
            new_node.add_child(n2)
            
            node_trace[lvl+1].append(new_node)        
            index += 1
            
        try:            
            ## There could be a leftover node in the list
            child = node_trace[lvl][2*(i+1)] 
            val = child.val
            parent = node_trace[lvl+1][-1]            
            parent.add_child(child)
            child.add_parent(parent)
        except:
            pass

        lvl += 1

    return node_trace

def print_node_levels(node_trace):
    for lvl in range(len(node_trace)):
        nodes = node_trace[lvl]
        for n in nodes:
            c_ids = " ".join([str(c.id) for c in n.children])
            print(n.id, c_ids)

        print("\n")
        


def generate_trace(trace, sd, sds, obj_sizes):

    node_trace = init_trace(trace, obj_sizes)
    node_trace = gen_node_tree(node_trace)

    trace_len = len(trace)
    i = 0

    while i < trace_len:
        curr_item 





## To test the above functions
if __name__ == "__main__":

    total_objects = 100
    length_trace = int(sys.argv[1])
    max_obj_sz = 15000
    alpha = 0.8
    

    obj_dst = obj_size_three_distribution(100, 200, 5000, 7000, 12000, 15000, 0.6, 0.2, 0.2)
    objects, dst = obj_dst.get_objects(total_objects)
    pop = PopularityDst(alpha)
    pop.assignPopularities(objects)
    trace, loc_frac, obj_sizes = pop.get_trace(objects, length_trace)    
    fd, sfd1, sds1 = gen_fd(trace, objects, "fd1", sc)

    print("objects : ", len(objects))

    print("obj_sizes : ", len(obj_sizes))

    print("generated first trace !")

    generate_trace(trace, fd, sds1, objects)


    #node_trace = init_trace(trace, objects)
    #node_trace = gen_node_tree(node_trace)

    #print_node_levels(node_trace)

    
