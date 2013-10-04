# -*- coding: utf-8 -*-
import sys
from types import *
from itertools import *

map_path = [ 'F1', 'F2', 'F3', 'F4','F5'  ]

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

	print("Error: {0} ({1}) stuck at {2}".format(test_field,str(Field[test_field]),error_bind_to))

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
	# Generate Test Cases
	Test_Cases = {}
	for block in map_path:
		BadPin = block

		for stuck in [0,1]:
			BadStuckAt = stuck

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

			for i in items:
				
				test = ""
				for var in ["x1","x2","x3","x4","x5","x6","x7"]:
					test += str(i[var])
					if var != "x7": test+=" "

				#print (Test_Cases.index(test))
				if test in Test_Cases.keys():
					if BadStuckAt == 0:
						Test_Cases[test][1].append(BadPin)
					else:
						Test_Cases[test][0].append(BadPin)
				else:
					S0 = []
					S1 = []
					if BadStuckAt == 0:
						S0.append(BadPin)
					else:
						S1.append(BadPin)

					Test_Cases[test] = [S1,S0]

	# Output
	# for test in Test_Cases:
	# 	print(test,Test_Cases[test])

	# Sort Lists by count
	MinMaxList = {}
	for case in Test_Cases:
		num = len(Test_Cases[case][0]) + len(Test_Cases[case][1])

		if num in MinMaxList.keys():
			MinMaxList[num].append(case)
		else:
			MinMaxList[num] = [case]

	UncoveredFailures = map_path
	
	ReversedOrder = list(reversed(sorted(MinMaxList.keys())))

	FinalTests = []
	flag = False

	for n in ReversedOrder:
		cases = MinMaxList[n]

		if flag :
			break

		for case in cases:
			S1 = Test_Cases[case][0]
			S0 = Test_Cases[case][1]

			# Remove all 1's
			for cs1 in S1:
				if cs1 in UncoveredFailures:
					UncoveredFailures.remove(cs1)
			for cs0 in S0:
			 	if cs0 in UncoveredFailures:
			 		UncoveredFailures.remove(cs0)

			FinalTests.append(case)

			if len(UncoveredFailures) == 0:
				flag = True
				break

	print ("Final covering tests: ",FinalTests)

##################################
if __name__=="__main__":
	main()
