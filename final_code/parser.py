import struct
from collections import defaultdict

class parser:
    def __init__(self, f_name):

        self.file = f_name
        self.sz_dst = defaultdict()
        self.pop_dst = defaultdict(int)
        
    def readline(self):
        pass

    def open(self):
        pass

class binaryParser(parser):
    def __init__(self, f_name):

        parser.__init__(self, f_name)

    def open(self):

        self.s = struct.Struct("III")
        self.ifile = open(self.file, "rb")

    def readline(self):

        b   = self.ifile.read(12)
        r   = self.s.unpack(b)
        sz  = r[2]
        obj = r[1]
        tm  = r[0]
        
        self.sz_dst[obj]   = sz
        self.pop_dst[obj] += 1

        return obj, sz, tm


class euParser(parser):
    def __init__(self, f_name):

        parser.__init__(self, f_name)

    def open(self):
        pass

    def readline(self):
        pass

class listParser(parser):
    def __init__(self, f_name):
        parser.__init__(self, f_name)

    def open(self):
        self.ifile = open(self.file, "r")
        self.reqs = self.ifile.readline().strip().split(",")
        self.reqs = [int(x) for x in self.reqs if x!= ""]
        self.no_reqs = len(self.reqs)
        self.counter = 0
        
    def readline(self):
        r = self.reqs[self.counter]
        self.counter += 1
        return r

    def length(self):
        return self.no_reqs
    
    
