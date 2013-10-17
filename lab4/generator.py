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
# Короче тут надо делать тики и проверять обратную связь
# подаем начальное состояние и перебираем пока не найдем 100% покрытие
# То есть:
# 1. метод обратной связи который будет выдавать значение которое надо запихнуть на вход
# 2. по тикам проверять что набор покрывает  и считать тики до 100% покрытия
# 3. если не 100% то задвигаем  из метода значение и делаем сдвиг
    # poly = 1010011 - x7 xor x5 xor x2 xor x1 xor 1 
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
        res_pos = self.poly.index('1')
        res = self.state[res_pos]

        for pos in range(res_pos,len(self.state)):
            if self.poly[pos] == '1':
                res = Xor(res,self.state[pos])
        ## final xor
        res = Xor(res,'1')

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
    
            if self.state == self.initState:
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
        period = self.findGenPeriod()

        for tick in range(period):
            states.append( self.tick() )    

        self.state = oldState
        self.tiks = oldTiks

        return states
