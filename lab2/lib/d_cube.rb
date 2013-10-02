class DCube

  attr_accessor :cube

  def initialize()
    self.cube = %W( x x x x x x x x x x x x x )
  end

  def check_empty
    self.cube.select{ |el| el == "e"}.any?
  end

  def intersect_with(cube1)
    new_cube = []
    self.cube.size.times do |i|
      new_cube << intersect(cube[i], cube1[i])
    end
    new_cube
  end

  def generate(function, error)
    error_sym = error == 1 ? "nd" : "d"
    cubes = []
    [0, 1].repeated_permutation(function.inputs_number).to_a.each do |inputs|
      if function.launch(*inputs) != error
        cubes << inputs.push(error_sym)
      end
    end
    cubes
  end

  private

  def intersect(a,b)
    return a if (a == b) || (b == "x")
    return b if (b == a) || (a == "x")
    'e'
  end
end
