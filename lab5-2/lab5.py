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

for power, polynoms in data:
  print "Power #{power}"

  for polynom in polyoms:
    analyzer = Analyzer.new(polynom)
    coverage = (CoverageCounter.new(states, analyzer).count * 100).round
    str = "#{polynom.to_s} | #{coverage.to_s} | #{analyzer.complexity}"
    if coverage == 100:
      if analyzer.complexity < complexity:
        complexity = analyzer.complexity
        result = [] << polynom
      elif analyzer.complexity == complexity:
        result  << polynom
      str = str.green
    else
      str = str.red

    print str

print "Optimal polynoms with #{complexity} complexity"

result.each { |polynom|  }
for polynom in result:
  print("#{polynom.to_s}")
