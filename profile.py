from point import Point
from line import Line

class AerodanymicProfile:
  def __init__(self, points:list,info:list):
    self.points = points
    self.firstCircle = info[0][0]
    self.secondCircle = info[1][0]
    self.upperPoints,self.downPoints = self.slicePoints(info)
    #self.intersectionPoint = self.getIntersectionPoint()

  def getCircleCenters(self)->list:    
    x = [point.x for point in self.points]
    y = [point.y for point in self.points]
    i_min_x,i_min_y = x.index(min(x)),y.index(min(y))
    x_min,y_x_min = min(x),y[i_min_x]
    y_min,x_y_min = min(y),x[i_min_y]
    print(y_min,x_min)

  def slicePoints(self,info:list)->tuple:
    startUpper,endUpper = info[0][1],info[1][1]
    startDown,endDown = info[1][2], info[0][2]
    upperPoints = self.points[67:128]
    downPoints = self.points[6:41]
    return upperPoints,downPoints

  def getIntersectionPoint(self)->Point:
    x0,y0 = self.firstCircle.x, self.firstCircle.y
    x0s,y0s = self.secondCircle.x, self.secondCircle.y
    x1,y1 = self.points[142].x, self.points[14].y
    x2,y2 = self.points[1].x, self.points[1].y
    x1s,y1s = self.points[56].x, self.points[56].y
    x2s,y2s = self.points[63].x, self.points[63].y
    k1 = -1 / ((y1 - y0) / (x1 - x0))
    k2 = -1 / ((y2 - y0) / (x2 - x0))
    k1s = -1 / ((y1s - y0s) / (x1s - x0s))
    k2s = -1 / ((y2s - y0s) / (x2s - x0s))
    x3 = (y2 - y1 + k1 * x1 - k2 * x2) / (k1 - k2)
    x3s = (y2s - y1s + k1s * x1s - k2s * x2s) / (k1s - k2s)
    y3 = k2 * x3 + y2 - k2 * x2
    y3s = k2s * x3s + y2s - k2s * x2s
    k3 = (y3 - y0) / (x3 - x0)
    k3s = (y3s - y0) / (x3s - x0)
    b3 = y3 - k3 * x3
    b3s = y3s - k3s * x3s
    x4 = (b3s - b3) / (k3 - k3s)
    y4 = k3s * x4 + b3s
    return Point(x4,y4)



'''
    k1 = -1 / ((y1 - y0) / (x1 - x0))
    k2 = -1 / ((y2 - y0) / (x2 - x0))
    k1s = -1 / ((y1s - y0s) / (x1s - x0s))
    k2s = -1 / ((y2s - y0s) / (x2s - x0s))
    x3 = (y2 - y1 + k1 * x1 - k2 * x2) / (k1 - k2)
    x3s = (y2s - y1s + k1s * x1s - k2s * x2s) / (k1s - k2s)
    y3 = k2 * x3 + y2 - k2 * x2
    y3s = k2s * x3s + y2s - k2s * x2s
    k3 = (y3 - y0) / (x3 - x0)
    k3s = (y3s - y0) / (x3s - x0)
    b3 = y3 - k3 * x3
    b3s = y3s - k3s * x3s
    x4 = (b3s - b3) / (k3 - k3s)
    y4 = k3s * x4 + b3s


    k1 = -(x1 - x0) / (y1 - y0)
    k2 = -(x2 - x0) / (y2 - y0)
    k1s = -(x1s - x0s) / (y1s - y0s)
    k2s = -(x2s - x0s) / (y2s - y0s)
    x3 = (y1 - y2 + k1 * x1 - k2 * x2) / (k1 - k2)
    y3 = y1 - k1 * (x3 - x1)
    x3s = (y1s - y2s + k1s * x1s - k2s * x2s) / (k1s - k2s)
    y3s = y1s - k1s * (x3s - x1s)
    numerator_x4 = y0s - y0 + (x0 * (y3 - y0) / (x1 - x0)) - (x0s * (y3s - y0s) / (x1s - x0s))
    denominator_x4 = (y3 - y0) / (x3 - x0) - (y3s - y0s) / (x3s - x0s)
    x4 = numerator_x4/denominator_x4
    y4 = (y3 - y0) / (x3 - x0) * x4 + y0 - x0 * (y3 - y0) / (x1 - x0)
'''