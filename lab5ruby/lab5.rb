Dir[File.expand_path('../lib/*.rb', __FILE__)].each {|f| require f}
require 'pry'
require 'highline/import'

POLYNOM_MIN = 7
POLYNOM_MAX = 10

lsrf, states = Lsrf.new, []

1.upto(2**Scheme::INPUTS-1) do
  states << lsrf.state.dup
  lsrf.next
end

data = PolynomGenerator.new(*[POLYNOM_MIN...POLYNOM_MAX]).generate

complexity, result = 100, []

data.each do |power, polynoms|
  puts "\n\tPower #{power}"

  polynoms.each do |polynom|
    analyzer = Analyzer.new(polynom)
    coverage = (CoverageCounter.new(states, analyzer).count * 100).round
    str = "Coverage: #{coverage.to_s} \t Complexity: #{analyzer.complexity} \t\t  #{polynom.to_s}"
    if analyzer.complexity < complexity
      complexity = analyzer.complexity
      result = [] << polynom
    elsif analyzer.complexity == complexity
      result  << polynom
    end
    puts str
  end
end

puts "\nOptimal polynoms(#{complexity} complexity):"
puts "\n"
result.each { |polynom| puts "#{polynom.to_s}" }
