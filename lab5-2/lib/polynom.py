class Polynom

  def __init__(self, arr)
    self.arr = arr

  def indexes
    #TODO: map.with_index
    self.indexes ||= self.arr.map.with_index{|v,i| v == 1 ? i : nil}.
                 reject{|i| i.nil? || i == 0}.
                 map{|i| i - 1}

  def to_a
    self.arr

  def to_s
    indexes.reverse.map{|i| "x#{i+1}"}.join(" \u2295 ") + " \u2295 1"
