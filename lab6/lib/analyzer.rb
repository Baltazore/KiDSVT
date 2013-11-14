class Analyzer

  attr_reader :complexity

  def initialize(polynom)
    @polynom = polynom
    @complexity = @polynom.indexes.size
    reset
  end

  def shift(value)
    i = @polynom.indexes.inject(value) {|input, index| input ^ @state[index]}
    @state.unshift(i)
    @state.pop
  end

  def state
    @state.dup
  end

  def reset
    @state = Array.new(@polynom.to_a.size - 1) { 0 }
  end

end
