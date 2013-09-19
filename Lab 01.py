#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from types import *
from itertools import *

map_path = { 'F1': 'B6'      , 'F2': 'B5,B6', 
			 'F3': 'B4,B5,B6', 'F4': 'B5,B6',
			 'F5': 'B6' }


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

	def __init__(self,name,vars,func,*inp):
		self._name = name
		self._vars = vars
		self._logic = Logic()
		self.func_name = func
		self.func = self._logic.Func(func.upper())
		if (len(inp) == 1):
			self.inp = inp[0]
		else:
			self.inp = inp

	def __str__(self):
		ret = self.func_name +" ( " 

		if type(self.inp) is tuple:
			for num,item in enumerate(self.inp):
				ret += str(item)
				if num != len(self.inp) - 1:
					ret += ", "

		else:
			ret += str(self.inp)
		ret += " )"
		return ret

	def __getattr__(self,name):

		if   (name == "value"):
			if type(self.inp) is tuple:
				ret = []
				for item in self.inp:
					if type(item) is Block:
						ret.append(item.value)
					elif type(item) is str:
						ret.append(self._vars[item])
					else:
						ret.append(item)
				return self.func(*tuple(ret))

			elif type(self.inp) is Block:
				return self.func(self.inp.value)
			
			elif type(self.inp) is str:
				return self.func(self._vars[self.inp])
			else:
				return self.func(self.inp)
		elif (name == "type"):
			return self.func_name
		elif (name == "name"):
			return self._name
		else:
			super().__getattr__(name)
## 

def FuncInit(inputX,BadPin,BadStuckAt):
	# Formula description
	Field = {}

	Field["F1"] = BadStuckAt if BadPin == "F1" else Block("F1",inputX,"xor",'x1','x2')
	Field["F2"] = BadStuckAt if BadPin == "F2" else Block("F2",inputX,"not",'x3')
	Field["F3"] = BadStuckAt if BadPin == "F3" else Block("F3",inputX,"nor",'x5','x6')
	Field["F4"] = BadStuckAt if BadPin == "F4" else Block("F4",inputX,"nand",'x4','x7',Field["F3"])
	Field["F5"] = BadStuckAt if BadPin == "F5" else Block("F5",inputX,"or",Field["F2"],Field["F4"])
	Field["F6"] = BadStuckAt if BadPin == "F6" else Block("F6",inputX,"nor",Field["F1"],Field["F5"])

	Out = Field["F6"]

	#print ("Formula: Y = "+str(Out))

	return Out

def FuncCalc(inputX,BadPin="",BadStuckAt=-1):
	LastCall = FuncInit(inputX,BadPin,BadStuckAt)
	
	return LastCall.value


def main():

	# Generate all input variants
	X_variants = []

	perm = list(range(128))
	i =0 
	for variant in perm:

		var_X = {}
		# Gen inputs
		inp = '{0:07b}'.format(variant)

		var_pos = 1
		for pos in inp:

			if pos == "0":
				val = 0
			else:
				val = 1

			var_X["x"+str(var_pos)] = val
			var_pos += 1

		X_variants.append(var_X)

	## Test them out!
	BadPin = input()
	BadStuckAt = int(input())
	#BadPin = "F2"
	#BadStuckAt = 0


	normal_Y = []
	bad_Y = []
	items = []

	for var_X in X_variants:
		Y = FuncCalc(var_X)
		normal_Y.append(Y)

		bY = FuncCalc(var_X,BadPin,BadStuckAt)
		bad_Y.append(bY)

	for pos in range(len(normal_Y)):
		val1 = normal_Y[pos]
		val2 = bad_Y[pos]

		if val1 != val2:
			items.append(X_variants[pos])
			#print(X_variants[pos])


	print (len(items))

	for i in items:
		for var in ["x1","x2","x3","x4","x5","x6","x7"]:
			sys.stdout.write(str(i[var])+" ")
		print("")


##################################
if __name__=="__main__":
	main()
