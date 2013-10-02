require 'highline/import'
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

schema = {
  f1 => [f6],
  f2 => [f5, f6],
  f3 => [f4, f5, f6],
  f4 => [f5, f6],
  f5 => [f6],
  f6 => []
}
blocks = [f1,f2,f3,f4,f5,f6]

# input
node = ask("Error at node(f1)?  ") { |node| node.default = "f3" }
val  = ask("Error value(1 or 0)?  ") { |val| val.default = "0" }
error_at = instance_eval(node)
error_value = val.to_i

d = DCube.new
d_cubes = DCube.generate_error error_at, error_value
# First point
d_functions = schema[error_at]
d_functions.each { |func| DCube.generate_for(func) }
s_functions = blocks[0...blocks.index(error_at)]
# Second point
final_set = []
d_cubes.each_with_index do |d, index|
  # Each D-error cube
  puts "\nError d-cube N#{index}"
  puts d.join(", ")
  res = [] # result after D-intersect
  result = [] # final result
  if d_functions.any?
  puts "\n D-cubes intersect"
  # For each Func at up-path
  d_functions.each do |func|
    puts "With Function #{func.operation.upcase}"
    # With all D-cubes for func
    func.d_cubes.each_with_index do |cube, index|
      puts "N#{index} intersect "
      res = DCube.intersect_cubes(d, cube)
      puts res.join(", ")
      if DCube.have_empty?(res)
        puts "Empty detected. Next element"
        next
      else
        puts "Going on!"
        break
      end
    end
  end
  else
    res = d
    puts "No D-cube intersections"
  end
  #Third point
  if s_functions.any?
  puts "\n S-cubes intersect"
  # For each func to down-path
  s_functions.each do |func|
    puts "With Function #{func.operation.upcase}"
    func.singulars.each_with_index do |sing|
      puts "N#{index} intersect "
      result = DCube.intersect_cubes(res, sing)
      puts result.join(", ")
      if DCube.have_empty?(res)
        puts "Empty detected. Next element"
        next
      else
        puts "Going on!"
        break
      end
    end
  end
  else
    result = res
    puts "No S-cubes intersections"
  end
  puts "\n#{index} Result"
  puts result.join(", ")
  final_set << result
end

puts "\n\n"
puts "Final results sets"
final_set.each { |set| puts set.join(", ")}
