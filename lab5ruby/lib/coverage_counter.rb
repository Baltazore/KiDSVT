class CoverageCounter

  SIGNALS = [0,1].freeze
  INPUTS = %i(x0 x1 x2 x3 x4 x5 x6).freeze
  OUTPUTS = %i(f1 f2 f3 f4 f5 f6).freeze
  MOCKS = [INPUTS, OUTPUTS].flatten.freeze

  attr_reader :standart_signature

  def initialize(states, analyzer)
    @states = states
    @analyzer = analyzer
    @analyzer.reset
    @standart_signature = signature(Scheme.new)
  end

  def count
    errors = 0
    SIGNALS.each do |signal|
      MOCKS.each  do |mock|
        @analyzer.reset
        scheme = Scheme.new(mock: {mock => signal})
        errors += 1 if signature(scheme) != standart_signature
      end
    end
    errors / total_errors
  end

  def signature(scheme)
    @states.each { |state| @analyzer.shift scheme.process(state) }
    @analyzer.state
  end

  def total_errors
    @total_errors ||= (SIGNALS.size * MOCKS.size).to_f
  end

end
