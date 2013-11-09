class CoverageCounter

  SIGNALS = [0,1]
  INPUTS = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6']
  OUTPUTS = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6']
  MOCKS = [INPUTS, OUTPUTS].flatten

  def __init__(self, states, analyzer)
    self.states = states
    self.analyzer = analyzer
    self.analyzer.reset
    self.standart_signature = signature(Scheme.new)

  def count
    errors = 0
    for signal in SIGNALS:
      for mock in MOCKS:
        self.analyzer.reset
        scheme = Scheme.new(mock: {mock => signal})
        errors += 1 if signature(scheme) != standart_signature

    errors / total_errors

  def signature(scheme)
    for state in self.states:
      self.analyzer.shift(scheme.process(state))
    self.analyzer.state

  def total_errors
    self.total_errors ||= (SIGNALS.size * MOCKS.size).to_f
