class CoverageCounter

  ERRORS = 1024

  attr_reader :standart_signature

  def initialize(data, analyzer)
    @data = data
    @analyzer = analyzer
    @analyzer.reset
    @standart_signature = signature(@data)
  end

  def count
    {1 => coverage_for(1),
     2 => coverage_for(2),
     3 => coverage_for(3),
     4 => coverage_for(4)}
  end

  def coverage_for(number_errors)
    num, errors = 0, []

    1.upto(ERRORS) do
      @analyzer.reset
      data = @data.dup

      1.upto(number_errors) do
        index = rand(@data.size)
        data[index] = data[index] == 0 ? 1 : 0
      end

      if signature(data) != standart_signature
        num += 1
      else
        errors << data
      end

    end

    { coverage: num.to_f / ERRORS, errors: errors }
  end

  def signature(data)
    data.each { |input| @analyzer.shift(input) }
    @analyzer.state
  end

end
