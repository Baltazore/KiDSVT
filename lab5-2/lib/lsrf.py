class Lsrf
  DEFAULT_STATE = [1,0,0,0,0,0,0]

  def __init__(self, state=DEFAULT_STATE)
    self.state = state.dup
    self.cycle = 0

  def next
    self.state.unshift(self.state[6] ^ self.state[0])
    self.state.pop
    self.cycle += 1

  def state
    self.state.dup
