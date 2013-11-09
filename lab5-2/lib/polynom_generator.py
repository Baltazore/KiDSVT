class PolynomGenerator

  def __init__(self, powers)
    self.powers = powers

  def generate
    tmp = Array.new
    for power in self.powers:
      tmp << [power, polynoms(power)]
    tmp

  protected

  def polynoms(power)
    # TODO: wtf!!!
    [*0..2**power].map{|i| ("%0#{power}d" % i.to_s(2)).each_char.to_a.map(&:to_i)}.
                   select{|polynom| polynom[power-1] == 1}.
                   select{|polynom| polynom.inject(:+) > 1 }.
                   map {|polynom| Polynom.new(polynom.unshift(1))}
