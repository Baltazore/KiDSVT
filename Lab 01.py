# -*- coding: utf-8 -*-
import sys
from types import *

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
		ret = self.func_name +"( " 

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
## 

def main():

	X = {'x1' : 1,
		 'x2' : 1,
		 'x3' : 1,
		 'x4' : 1,
		 'x5' : 0,
		 'x6' : 0,
		 'x7' : 1}

	# Y = nor( xor( x1, x2 ), or( not( x3 ), nand( x4, x7, nor( x5, x6 ) ) ) )	

	# Formula description
	Field = {}

	Field["F1"] = Block("F1",X,"xor",'x1','x2')
	Field["F2"] = Block("F2",X,"not",'x3')
	Field["F3"] = Block("F3",X,"nor",'x5','x6')
	Field["F4"] = Block("F4",X,"nand",'x4','x7',Field["F3"])
	Field["F5"] = Block("F5",X,"or",Field["F2"],Field["F4"])
	Field["F6"] = Block("F6",X,"nor",Field["F1"],Field["F5"])

	print ("Formula: Y = "+str(Field["F6"]))
	
	############ Tests
	test_field = "F1"
	error_bind_to = 0

	print("Error: {0} ({1}) stuck at {2}".format(test_field,str(Field[test_field]),error_bind_to))

	print (Field["F6"].value) # Y
	Field[test_field] = error_bind_to
	print (Field["F6"].value) # Y

##################################
if __name__=="__main__":
	main()
