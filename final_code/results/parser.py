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

    
    
