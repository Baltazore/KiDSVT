class Analyzer

  def __init__(self, polynom)
    self.polynom = polynom
    self.complexity = polynom.indexes.size
    reset

  def shift(value)
    i = self.polynom.indexes.inject(value) {|input, index| input ^ self.state[index]}
    self.state.unshift(i)
    self.state.pop

  def state
    self.state.dup

  def reset
    self.state = Array.new(self.polynom.to_a.size - 1) { 0 }
