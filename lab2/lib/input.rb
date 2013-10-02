class Input
  attr_accessor :position, :value

  def initialize(position, value="x")
    self.position = position
    self.value = value
  end
end
