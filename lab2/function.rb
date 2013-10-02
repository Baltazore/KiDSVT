class Function

  attr_accessor :position, :function, :operands

  def initialize(position, function, operands)
    self.position = position
    self.function = function
    self.operands = operands
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
