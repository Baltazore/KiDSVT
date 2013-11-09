class Scheme

  INPUTS = 7

  def __init__(self, mock: {})
    self.mock = mock
    self.signals = Array.new

  # TODO: metaprogramming
  # 0.upto(INPUTS) do |i|
  #   define_method "x#{i}".to_sym do
  #     self.mock["x#{i}".to_sym] || self.signals[i]
  #   end
  # end

  def f1
    self.mock[:f1] || Function.new('and', x0, x1).value

  def f2
    self.mock[:f2] || Function.new('not', x2).value

  def f3
    self.mock[:f3] || Function.new('or',  x4, x5).value

  def f4
    self.mock[:f4] || Function.new('and', x3, x6, f3).value

  def f5
    self.mock[:f5] || Function.new('nor', f2, f4).value

  def f6
    self.mock[:f6] || Function.new('and', f1, f5).value

  def process(signals)
    self.signals = signals
    f6

  def state
    [x0, x1, x2, x3, x4, x5, x6, x6, f1, f2, f3, f4, f5, f6]
