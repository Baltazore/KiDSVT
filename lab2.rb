require 'pry'

def intersect(a,b)
  return a if (a == b) || (b == 'x')
  return b if (b == a) || (a == 'x')
  'e'
end

def check_empty(cube)
  cube.select{ |el| el == 'e'}.any?
end

def cubes_intersect(cube1, cube2)
  new_cube = []
  cube1.size.times do |i|
    new_cube << intersect(cube1[i], cube2[i])
  end
  new_cube
end

def generete_d_cube

end

binding.pry
