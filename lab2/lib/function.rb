class Function

  attr_accessor :position, :operation, :inputs_number, :input0, :input1, :input2

  SINGULAR_CUBES = {
    #           0 1 2 3 4 5 6 7 8 9 0 1 2
    'f1' => [%w(0 0 x x x x x 0 x x x x x),
             %w(0 1 x x x x x 1 x x x x x),
             %w(1 0 x x x x x 1 x x x x x),
             %w(1 1 x x x x x 0 x x x x x)],

    'f2' => [%w(x x 0 x x x x x 1 x x x x),
             %w(x x 1 x x x x x 0 x x x x)],

    'f3' => [%w(x x x x 0 0 x x x 1 x x x),
             %w(x x x x x 1 x x x 0 x x x),
             %w(x x x x 1 x x x x 0 x x x)],

    'f4' => [%w(x x x 0 x x x x x x 1 x x),
             %w(x x x x x x 0 x x x 1 x x),
             %w(x x x x x x x x x 0 1 x x),
             %w(x x x 1 x x 1 x x 1 0 x x)],

    'f5' => [%w(x x x x x x x x 0 x 0 0 x),
             %w(x x x x x x x x x x 1 1 x),
             %w(x x x x x x x x 1 x x 1 x)],

    'f6' => [%w(x x x x x x x 0 x x x 0 1),
             %w(x x x x x x x x x x x 1 0),
             %w(x x x x x x x 1 x x x x 0)]
  }

  def initialize(position, operation, inputs_number, *inputs)
    self.position      = position
    self.operation     = operation
    self.inputs_number = inputs_number
    inputs.each_with_index do |input, index|
      self.send("input#{index}=", input)
    end
  end

  def or(op1, op2)
    op1 | op2
  end

  def nor(op1, op2)
    no(op1 | op2)
  end

  def no(op)
    op == 1 ? 0 : 1
  end

  def nand(op1, op2, op3)
    not(op1 & op2 & op3)
  end

  def xor(op1, op2)
    op1 ^ op2
  end

  def launch(*args)
    send(operation, *args)
  end

  def positions
    ps = []
    inputs_number.times do |i|
      ps << send("input#{i}").position
    end
    ps.push(position)
  end
end
