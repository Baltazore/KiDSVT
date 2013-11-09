from lib import *

POLYNOM_MIN = 7
POLYNOM_MAX = 10

lsrf = Lsrf.new
states = Array.new

for x in range(2**Scheme::INPUTS-1):
  states << lsrf.state.dup
  lsrf.next

data = PolynomGenerator.new(*[POLYNOM_MIN...POLYNOM_MAX]).generate

complexity = 100
result = []

data.each do |power, polynoms|
  puts "Power #{power}"

  polynoms.each do |polynom|
    analyzer = Analyzer.new(polynom)
    coverage = (CoverageCounter.new(states, analyzer).count * 100).round
    str = "#{polynom.to_s} | #{coverage.to_s} | #{analyzer.complexity}"
    if coverage == 100
      if analyzer.complexity < complexity
        complexity = analyzer.complexity
        result = [] << polynom
      elsif analyzer.complexity == complexity
        result  << polynom
      end
      str = str.green
    else
      str = str.red
    end

    puts str
  end
end

puts "Optimal polynoms with #{complexity} complexity"

result.each { |polynom| puts "#{polynom.to_s}" }
