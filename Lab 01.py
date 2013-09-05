import sys
from types import *

map_path = { 'F1': 'B1,B6'      , 'F2': 'B2,B5,B6', 
			 'F3': 'B3,B4,B5,B6', 'F4': 'B4,B5,B6',
			 'F5': 'B5,B6' }


map_blocks = {'B1': 'xor', 'B2' : 'not', 'B3' : 'nor',
			  'B4': 'nand', 'B5' : 'or', 'B6' : 'nor'}

## Logic functions
class Logic:
	def AND(self,*args):
		ret = 1
		for arg in args:
			ret = ret & arg
		return bool(ret)

	def OR(self,*args):
		ret = 0
		for arg in args:
			ret = ret | arg
		return bool(ret)

	def NOT(self,arg):
		return not arg

	def XOR(self,arg1,arg2):
		return bool(arg1 ^ arg2)

	def NOR(self,*args):
		return not self.OR(*args)
		
	def NAND(self,*args):
		return not self.AND(*args)

	def Call(self,name,*args):
		return getattr(self,name)(*args)

	def Func(self,name):
		return getattr(self,name)

## Blocks
class Block:

	def __init__(self,name,func,*inp):
		self.name = name
		self._logic = Logic()
		self.func = self._logic.Func(func.upper())
		if (len(inp) == 1):
			self.inp = inp[0]
		else:
			self.inp = inp

	def __str__(self):
		ret = str(self._logic) + str(self.func) + str(self.inp)
		return ret

	def __getattr__(self,value):
		if type(self.inp) is TupleType:
			ret = []
			for item in self.inp:
				if type(item) is InstanceType:
					ret.append(item.value)
				else:
					ret.append(item)
			return self.func(*tuple(ret))

		elif type(self.inp) is InstanceType:
			return self.func(self.inp.value)
		
		else:
			return self.func(self.inp)

## 

def main():

	#    	x1,x2,x3,x4,x5,x6,x7
	x = [-1, 1, 1, 1, 1, 0, 0, 1]

	# y = (x1 xor x2) nor ( not(x3) or ( x4 nand x7 nand (x5 nor x6) ) )
	# 			F1			F2								F3
	#												F4
	#								F5
	#					F6		

	B1 = Block("B1","xor",x[1],x[2])
	B2 = Block("B2","not",x[3])
	B3 = Block("B3","nor",x[5],x[6])
	B4 = Block("B4","nand",x[4],x[7],B3)
	B5 = Block("B5","or",B2,B4)
	B6 = Block("B6","nor",B1,B5)

	print (B6.value) # Y

##################################
if __name__=="__main__":
	main()
