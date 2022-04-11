import math

class Point:
  def __init__(self, x:float, y:float) -> None:
      self.x = x
      self.y = y

  def __add__(self,other):
    return Point(self.x+other.x,self.y+other.y)

  def __sub__(self,other):
    return Point(self.x-other.x,self.y - other.y)

  def __mul__(self, other:float):
    return Point(self.x*other,self.y*other)

  def __truediv__(self, other:float):
    return Point(self.x/other,self.y/other)
    
def distance(p1:Point,p2:Point)->float:
  return math.sqrt(math.pow(p1.x-p2.x,2)+math.pow(p1.y-p2.y,2))
