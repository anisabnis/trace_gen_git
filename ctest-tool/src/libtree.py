from itertools import count
import numpy as np
import sys

root = None
MAX_CHILDREN = 8

class node:
    _ids = count(1)

    def __init__(self, obj_id, size):

        # Each node maintains an id and corresponds could correspond to an object
        # in the cache        
        self.id = next(self._ids)
        self.obj_id = obj_id
        
        # Sum of size of all the objects below the node in the tree
        self.s = size

        # Each node has upto MAX_CHILDREN children
        self.children = []

        # A node points to the immediate neighbour to its right
        self.next = None

        # Maintain a parent pointer
        self.parent = None

        # Each node maintains its index in the children list of the parent
        self.child_idx = 0

        # Check if the node is the root
        self.is_root = False


    # Find the least common ancestor of a node and other node n in the tree
    def LCA(self, n):

        a = self
        while a != None:
            b = n
            while b != None:
                if a.id == b.id:                    
                    return a.id
                b = b.parent
            a = a.parent

        # It is impossible to not have a least common ancestor
        print('Error in function : %s for nodes  %d %d\n' % (whoami(), self.id, n.id))
        sys.exit()


    # Add a child node n 
    def add_child(self, n):
        n.child_idx = len(self.children)
        self.children.append(n)
        n.parent = self


    # Set parent as n
    def set_parent(self, n):
        self.parent = n


    # Find the unique total size between self and node n in the cache
    def findUniqBytes(self, n, debug):
        curr = self
        ub = 0

        # If curr and next have the same parent
        if curr.parent.id == n.parent.id:

            for i in range(curr.child_idx + 1, n.child_idx):
                ub += curr.parent.children[i].s

            return ub

        # Find the least common ancestor        
        lca_id = curr.lca(n)

        # Left of lca : Find the total size to the left of LCA
        parent = curr.parent
        child  = curr
        while parent.id != lca_id:
            if child.child_idx != len(parent.children):
                for i in range(child.child_idx + 1, len(parent.children)):
                    ub += parent.children[i].s        
            parent = parent.parent
            child  = child.parent
        save1 = child
        
        # Right of lca : Find the total size to the right of LCA
        parent = n.parent
        child = n
        while parent.id != lca_id:
            if child_idx != 0:
                for i in range(0, child.child_idx):
                    ub += parent.children[i].s
            parent = parent.parent
            child  = child.parent
        save2 = child

        ## In between the two nodes
        for i in range(save1.child_idx + 1, save2.child_idx):
            ub += save1.parent.children[i].s

        return ub

    

    def cleanUpAfterInsertion(self, sd, inserted_node, debug):
        curr = self
        next = curr.next

        if next == None:
            self.delete_node(debug)
            return

        uniq_bytes = curr.s
        cnt = 0
        to_del_nodes = []

        while uniq_bytes < sd:

            if next_node == None:
                break

            to_del_nodes.append(curr)
            uniq_bytes += curr_node.findUniqBytes(next_node)
            next_node = next_node.next
            curr_node = curr_node.next

        for d in to_del_nodes:
            inserted_node.next = d.next
            d.delete_node()

        return to_del_nodes
