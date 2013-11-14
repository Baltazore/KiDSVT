class PolynomGenerator

  def initialize(powers)
    @powers = powers
  end

  def generate
    @powers.map{|power| [power, polynoms(power)] }
  end

  protected

  def polynoms(power)
    [*0..2**power].map{|i| ("%0#{power}d" % i.to_s(2)).each_char.to_a.map(&:to_i)}.
                   select{|polynom| polynom[power-1] == 1}.
                   select{|polynom| polynom.inject(:+) > 1 }.
                   map {|polynom| Polynom.new(polynom.unshift(1))}
  end

end
