# -*- coding: utf-8 -*-
class sigAnalyser:
    DEBUG = False

    def __init__(self,poly="101011110"):
        self.poly = poly
        self.init()

    def init(self):
        self.initState = "00000000"
        self.state = self.initState
        self.tiks = 0

    def tick(self,signal):
        def Xor(ch1,ch2):
            if str(ch1) == str(ch2):
                return '0'
            else:
                return '1'
        
        # callback function
        revPoly = self.poly[::-1]
        resPos = revPoly.index('1')

        res = Xor(self.state[-1], self.state[ -resPos - 1 ] ) 

        for pos in range(len(self.poly) - resPos - 2 , 0 , -1):
            if self.poly[pos] == '1':
                #if self.DEBUG : print("XOR: ",pos,res)
                res = Xor(res,self.state[pos-1])
        res = Xor(signal,res)

        
        # New State
        old_state = self.state[:7]
        self.state = res + old_state
        self.tiks += 1

        if self.DEBUG : print (self.tiks,self.state)

        return self.state


# sig = sigAnalyser()
# sig.DEBUG = False

# res = []
# for i in range(256):
#     sig.tick('1')
#     res.append(sig.state)

# def f7(seq):
#     seen = set()
#     seen_add = seen.add
#     return [ x for x in seq if x not in seen and not seen_add(x)]

# res = f7(res)
# res = list( sorted(res))
# print len(res),res