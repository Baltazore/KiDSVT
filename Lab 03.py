# -*- coding: utf-8 -*-
import sys
from types import *
from itertools import *

map_path = [ 'X1','X2','X3','X4','X5','X6','X7','F1', 'F2', 'F3', 'F4','F5'  ]

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

	return Out,Field

def FuncCalc(inputX,BadPin="",BadStuckAt=-1):
	LastCall,Field = FuncInit(inputX,BadPin,BadStuckAt)
	
	return LastCall.value

	print("Error: {0} ({1}) stuck at {2}".format(test_field,str(Field[test_field]),error_bind_to))

def FuncCallWithCount(inputX,BadPin="",BadStuckAt=-1):
	LastCall,Field = FuncInit(inputX,BadPin,BadStuckAt)
		
	vals = [ int(Field[inp].value) for inp in sorted(Field.keys()) ]
	inps = [ inputX[inp] for inp in sorted(inputX.keys()) ]

	ret = inps + vals
	return ret



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

				# Filtering xN for BadPins
				filtered_var_X = {}
				filtered_var_X["x1"] = BadStuckAt if BadPin == "X1" else var_X["x1"]
				filtered_var_X["x2"] = BadStuckAt if BadPin == "X2" else var_X["x2"]
				filtered_var_X["x3"] = BadStuckAt if BadPin == "X3" else var_X["x3"]
				filtered_var_X["x4"] = BadStuckAt if BadPin == "X4" else var_X["x4"]
				filtered_var_X["x5"] = BadStuckAt if BadPin == "X5" else var_X["x5"]
				filtered_var_X["x6"] = BadStuckAt if BadPin == "X6" else var_X["x6"]
				filtered_var_X["x7"] = BadStuckAt if BadPin == "X7" else var_X["x7"]


				bY = FuncCalc(filtered_var_X,BadPin,BadStuckAt)
				bad_Y.append(bY)

			for pos in range(len(normal_Y)):
				val1 = normal_Y[pos]
				val2 = bad_Y[pos]

				if val1 != val2:
					items.append(X_variants[pos])

			for i in items:
				test = ""
				for var in ["x1","x2","x3","x4","x5","x6","x7"]:
					test += str(i[var])
					if var != "x7": test+=" "

				if test in Test_Cases.keys():
					if BadStuckAt == 0:
						if BadPin not in Test_Cases[test][1]:
							Test_Cases[test][1].append(BadPin)
					else:
						if BadPin not in Test_Cases[test][0]:
							Test_Cases[test][0].append(BadPin)
				else:
					S0 = []
					S1 = []
					if BadStuckAt == 0:
						S0.append(BadPin)
					else:
						S1.append(BadPin)

					Test_Cases[test] = [S1,S0]

	# Find minimum test cases
	# Sort Lists by count of switches
	MinMaxList = {}
	for case in Test_Cases:
		num = len(Test_Cases[case][0]) + len(Test_Cases[case][1])

		if num in MinMaxList.keys():
			MinMaxList[num].append(case)
		else:
			MinMaxList[num] = [case]

	UncoveredFailures0 = map_path[:]
	UncoveredFailures1 = map_path[:]
	ReversedOrder = list(reversed(sorted(MinMaxList.keys())))

	FinalTests = []
	flag = False

	for n in ReversedOrder:
		cases = MinMaxList[n]

		if flag == True :
			break

		for case in cases:
			S1 = Test_Cases[case][0]
			S0 = Test_Cases[case][1]

			covered_pins = 0
			for cs1 in S1:
				if cs1 in UncoveredFailures1:
					covered_pins += 1
					UncoveredFailures1.remove(cs1)
			for cs0 in S0:
			 	if cs0 in UncoveredFailures0:
			 		covered_pins += 1
			 		UncoveredFailures0.remove(cs0)		

			if covered_pins != 0 : 
				FinalTests.append(case)

			if len(UncoveredFailures0) == 0 and len(UncoveredFailures0) == 1:
				flag = True
				break

	print ("Covering tests: ")
	for test in FinalTests:
		print ( test, Test_Cases[test] )

	print(" ")
	# Calc function switching
	calls = []
	for test in FinalTests:

		# Generate test input
		vals = test.split(" ")
		var_x = {}
		n = 1
		for val in vals:
			var_x["x"+str(n)] = int(val)
			n += 1

		calls.append(FuncCallWithCount(var_x))	
	
	# Calculate costs
	perm_list = {}
	n = 0
	for perm in permutations(calls):
		cost = 0
		for i in range(0,len(perm)-1):
			st1 = perm[i]
			st2 = perm[i+1]

			for j in range(0,len(st1)):
				if st1[j] != st2[j]:
					cost += 1


		if cost in perm_list:
			perm_list[cost].append(perm)
		else:
			perm_list[cost] = [perm]

	#
	optimal_list = list(sorted(perm_list.keys()))
	best_sw = optimal_list[0]

	print("Switches : ",best_sw)
	print("First three alternatives: ")

	#print (perm_list[best_sw])

	n = 0
	for perm in perm_list[best_sw]:

		n += 1
		if n==4: break
		for item in perm:
			print (item[:7])

		print ("=========================")

	


##################################
if __name__=="__main__":
	main()
