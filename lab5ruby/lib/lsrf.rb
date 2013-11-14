class Lsrf
  DEFAULT_STATE = [1,0,0,0,0,0,0]
  attr_reader :cycle

  def initialize(state=DEFAULT_STATE)
    @state = state.dup
    @cycle = 0
  end

  def next
    @state.unshift(@state[6] ^ @state[0])
    @state.pop
    @cycle += 1
  end

  def state
    @state.dup
  end

end
