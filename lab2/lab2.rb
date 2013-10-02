require 'pry'
require_relative 'lib/function'
require_relative 'lib/d_cube'
require_relative 'lib/input'
#schema init
f1 = Function.new(7,  "xor",  2, Input.new(0), Input.new(1))
f2 = Function.new(8,  "no",   1, Input.new(2))
f3 = Function.new(9,  "nor",  2, Input.new(4), Input.new(5))
f4 = Function.new(10, "nand", 3, Input.new(3), Input.new(9), Input.new(6) )
f5 = Function.new(11, "or",   2, Input.new(8), Input.new(10))
f6 = Function.new(12, "nor",  2, Input.new(7), Input.new(11))

schema = [ f1, f2, f3, f4, f5, f6 ]

# input
error_at = instance_eval('f3')
error_value = '1'.to_i

d = DCube.new
d_cubes = DCube.generate_error error_at, error_value
# First point
d_functions = schema[(schema.index(error_at)+1)..-1]
d_functions.each { |func| DCube.generate_for(func) }
# Second point
d_cubes.each do |d|
  puts d.join(", ")
  binding.pry
end
