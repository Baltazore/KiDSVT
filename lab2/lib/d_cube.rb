class DCube

  attr_accessor :cube, :prev_cube

  def initialize()
    self.cube = %W( x x x x x x x x x x x x x )
  end

  def self.generate(function, error)
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
        cube[i] = kube[index]
      end
      kubes << cube
    end
    kubes
  end

  def generate_after(function)

  end

  def check_empty
    self.cube = prev_cube if cube.have_empty?
  end

  def have_empty?
    self.cube.select{ |el| el == "e"}.any?
  end

  def intersect_with(cube1)
    new_cube = []
    self.prev_cube = cube
    cube.size.times do |i|
      new_cube << intersect(cube[i], cube1[i])
    end
    self.cube = new_cube
  end

  private

  def intersect(a,b)
    return a if (a == b) || (b == "x")
    return b if (b == a) || (a == "x")
    "e"
  end
end
