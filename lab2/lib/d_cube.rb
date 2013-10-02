class DCube

  attr_accessor :cube, :prev_cube

  def initialize()
    self.cube = %W( x x x x x x x x x x x x x )
  end

  def self.generate_error(function, error)
    error_sym = error == 1 ? "nd" : "d"
    cubes = []
    [0, 1].repeated_permutation(function.inputs_number).to_a.each do |inputs|
      if function.launch(*inputs) != error
        cubes << inputs.push(error_sym)
      end
    end
    kubes = []
    cubes.each do |kube|
      cube = %W( x x x x x x x x x x x x x )
      function.positions.each_with_index do |i, index|
        cube[i] = kube[index].to_s
      end
      kubes << cube
    end
    kubes
  end

  def self.generate_for(function)
    output_index = function.position
    zeros = function.singulars.select{|cube| cube[output_index] == "0"}
    ones  = function.singulars.select{|cube| cube[output_index] == "1"}
    zeros.each do |zero|
      ones.each do |one|
        res = DCube.intersect_cubes zero, one
        function.d_cubes << res unless have_empty?(res)
      end
    end
  end

  def self.intersect_cubes(cube1, cube2)
    new_cube = []
    cube1.size.times do |i|
      new_cube << intersect(cube1[i], cube2[i])
    end
    new_cube
  end

  def check_empty
    self.cube = prev_cube if cube.have_empty?
  end

  def have_empty?(cube = self.cube)
    cube.select{ |el| el == "e"}.any?
  end

  def self.have_empty?(cube = self.cube)
    cube.select{ |el| el == "e"}.any?
  end

  def intersect_with(cube1)
    new_cube = []
    self.prev_cube = cube
    cube.size.times do |i|
      new_cube << intersect(cube[i], cube1[i])
    end
    self.cube = new_cube
  end

  def intersect(a,b)
    if (a == b) || (b == "x")
      return a
    elsif (b == a) || (a == "x")
      return b
    elsif (a == "1") && (b == "0")
      return 'd'
    elsif (a == "0") && (b == "1")
      return 'nd'
    else
      "e"
    end
  end

  def self.intersect(a,b)
    if (a == b) || (b == "x")
      return a
    elsif (b == a) || (a == "x")
      return b
    elsif (a == "1") && (b == "0")
      return 'd'
    elsif (a == "0") && (b == "1")
      return 'nd'
    else
      "e"
    end
  end

end
