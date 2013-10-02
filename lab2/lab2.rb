require 'pry'
require_relative 'lib/function'
require_relative 'lib/d_cube'
require_relative 'lib/input'
#                 1 2 3 4 5 6 7 8 9 0 1 2 3
INITIAL_CUBE = %w(x x x x x x x x x x x x x)
f1 = Function.new(7,  "xor",  2, Input.new(0), Input.new(1))
f2 = Function.new(8,  "no",   1, Input.new(2))
f3 = Function.new(9,  "nor",  2, Input.new(4), Input.new(5))
f4 = Function.new(10, "nand", 3, Input.new(3), Input.new(9), Input.new(6) )
f5 = Function.new(11, "or",   2, Input.new(8), Input.new(10))
f6 = Function.new(12, "nor",  2, Input.new(7), Input.new(11))


d = DCube.new
binding.pry
