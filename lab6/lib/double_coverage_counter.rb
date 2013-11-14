class DoubleCoverageCounter < CoverageCounter

  def signature(data)
    data.each_slice(2).each { |y, y1| @analyzer.shift(y, y1) }
    @analyzer.state
  end

end
