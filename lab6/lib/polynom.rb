class Polynom

  def initialize(arr)
    @arr = arr
  end

  def indexes
    @indexes ||= @arr.map.with_index{|v,i| v == 1 ? i : nil}.
                 reject{|i| i.nil? || i == 0}.
                 map{|i| i - 1}
  end

  def to_a
    @arr
  end

  def to_s
    indexes.reverse.map{|i| "x#{i+1}"}.join(" xor ") + " xor 1"
  end

end
