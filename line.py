from point import Point

class Line:
  def __init__(self,p1:Point,p2:Point)->None:
    self.p1 = p1
    self.p2 = p2
    self.k = (self.p1.y - self.p2.y) / (self.p1.x - self.p2.x)
    self.b = self.p2.y - self.k * self.p2.x
