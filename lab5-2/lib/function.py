class Function

  def __init__(self, operation, *inputs)
    self.operation = operation
    self.inputs = inputs

  def value
    values = Array.new
    for i in self.inputs:
      values << i.is_a?(Function) ? i.value : i

    self.launch(values)

  def launch(values)
    num = values.size == 1 ? "" : values.size.to_s
    # TODO: metaprogramming convert
    self.send("#{self.operation}#{num}", *values)

  def not(op)
    op == 1 ? 0 : 1

  def or2(op1, op2)
    op1 | op2

  def or3(op1, op2, op3)
    op1 | op2 | op3

  def and2(op1, op2)
    op1 & op2

  def and3(op1, op2, op3)
    op1 & op2 & op3

  def nor2(op1, op2)
    self.not(or2(op1, op2))
