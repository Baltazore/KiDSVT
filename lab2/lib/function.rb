class Function

  attr_accessor :position, :operation, :inputs_number, :input0, :input1, :input2

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
