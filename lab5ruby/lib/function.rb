class Function

  def initialize(operation, *inputs)
    @operation = operation
    @inputs = inputs
  end

  def value
    values = @inputs.map { |i| i.is_a?(Function) ? i.value : i }
    self.launch(values)
  end

  def launch(values)
    num = values.size == 1 ? "" : values.size.to_s
    self.send("#{@operation}#{num}", *values)
  end

  def not(op)
    op == 1 ? 0 : 1
  end

  def or2(op1, op2)
    op1 | op2
  end

  def or3(op1, op2, op3)
    op1 | op2 | op3
  end

  def and2(op1, op2)
    op1 & op2
  end

  def and3(op1, op2, op3)
    op1 & op2 & op3
  end

  def nand3(op1, op2, op3)
    self.not(and3(op1, op2, op3))
  end

  def nor2(op1, op2)
    self.not(or2(op1, op2))
  end

  def xor2(op1, op2)
    op1 ^ op2
  end

end
