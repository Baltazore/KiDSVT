Dir[File.expand_path('../lib/*.rb', __FILE__)].each {|f| require f}
require 'pry'
require 'highline/import'
require 'colorize'
require 'matrix'

SEED = 42
STATES_NUMBER = 256
L = 44
POLYNOM = [1,0,0,0,1,1,0,1]

# polynom = X8+Х6+Х5+Х+1
# l = 40

random = Random.new(SEED)
polynom = Polynom.new([1,POLYNOM].flatten)
data = ("%0#{L}d" % random.rand(0...2**L).to_s(2)).each_char.to_a.map(&:to_i)

analyzer = Analyzer.new(polynom)
coverage = CoverageCounter.new(data, analyzer).count

puts "Single analyzer"

coverage.each do |number_errors, hash|
  puts "\n\tNumber of errors: #{number_errors}" + "\tCoverage: #{hash[:coverage]}" + "\tWrong errors:" unless hash[:errors].empty?
  hash[:errors].each { |error| puts error.inspect }
end

analyzer = DoubleAnalyzer.new(polynom)
coverage = DoubleCoverageCounter.new(data, analyzer).count

puts "\n\n\n\n"
puts "Double analyzer"

coverage.each do |number_errors, hash|
  puts "\t\nNumber of errors: #{number_errors}"+ "\tCoverage: #{hash[:coverage]}"+ "\tWrong errors:" unless hash[:errors].empty?
  hash[:errors].each { |error| puts error.inspect }
end
