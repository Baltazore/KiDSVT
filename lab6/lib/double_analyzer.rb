class DoubleAnalyzer < Analyzer

  def initialize(polynom)
    @polynom = polynom
    reset
  end

  def shift(y,y1)
    state = Array.new(@polynom.to_a.size - 1)
    state[0] = @state[0] ^ @state[2] ^ @state[4] ^ @state[5] ^ @state[6] ^ @state[7] ^ y ^ y1
    state[1] = @state[0] ^ @state[4] ^ @state[5] ^ @state[7] ^ y
    state[2] = @state[0]
    state[3] = @state[1]
    state[4] = @state[2]
    state[5] = @state[3]
    state[6] = @state[4]
    state[7] = @state[5]
    @state = state
  end

  def state
    @state.dup
  end

  def reset
    @state = Array.new(@polynom.to_a.size - 1) { 0 }
  end

end
