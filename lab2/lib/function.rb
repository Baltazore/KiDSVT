class Function

  attr_accessor :position, :function, :input0, :input1, :input2, :output

  def initialize(position, function, *inputs)
    self.position = position
    self.function = function
    inputs.each_with_index do |input, index|
      self.send("input#{index}=", input)
    end
  end

  def or(op1, op2)
    op1 || op2
  end

  def nor(op1, op2)
    !(op1 || op2)
  end

  def not(op)
    !op
  end

  def nand(op1, op2, op3)
    !(op1 & op2 & op3)
  end

  def xor(op1, op2)
    op1 ^ op2
  end

  def launch(*args)
    self.send(self.function, *args)
  end
end
