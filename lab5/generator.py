# -*- coding: utf-8 -*-
class Generator:
    ''' Usage example:
    init_state = "1000110"
    gen = Generator(start=init_state)
    #gen.DEBUG = True
    # Ticks
    state = gen.tick() # 1100011
    state = gen.tick() # 0110001
    # Period
    period = gen.findGenPeriod() # 62
    # States
    states = gen.getPossibleStates() # ['1100011','0110001', ... ] , len(states) = 62
    '''  
    DEBUG = False

    def __init__(self,poly="1010011",start="0000000"):
        self.poly = poly
        self.initState = start
        self.state = start
        self.tiks = 0

    def init(self,start):
        self.tiks = 0
        self.initState = start
        self.state = start

    def tick(self):
        def Xor(ch1,ch2):
            if ch1 == ch2:
                return '0'
            else:
                return '1'
        # calback function
        rev_poly = self.poly[::-1]
        res_pos = rev_poly.index('1')
        res = self.state[res_pos]

        #print ("B",res,res_pos)
        for pos in range(res_pos+1,7):
            if rev_poly[pos] == '1':
                res = Xor(res,self.state[pos])
        ## final xor
        res = Xor(res,'1')
        #print ("A",res)

        # New State
        old_state = self.state[:6]
        self.state = res + old_state

        self.tiks += 1

        if self.DEBUG : print (self.tiks,self.state)

        return self.state

    def findGenPeriod(self):
        tiks = self.tiks
        oldState = self.state

        # Calc
        self.state = self.initState
        self.tiks = 0
        flag = True
        while flag:
            state = self.tick()
    
            if state == self.initState:
                flag = False

        period = self.tiks

        # restoring
        self.tiks = 0
        self.state = oldState

        return period

    def getPossibleStates(self):
        oldState = self.state
        oldTiks = self.tiks

        self.state = self.initState
        self.tiks = 0

        states = []
        #period = self.findGenPeriod()
        state = ""
        while state != self.initState:
        #for tick in range(period):
            state = self.tick()
            states.append( state )    

        self.state = oldState
        self.tiks = oldTiks

        return states