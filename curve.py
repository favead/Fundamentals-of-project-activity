from point import Point
from point import distance
from line import Line
import copy


class Bezier_Curve:
    def __init__(self, reference_points: list) -> None:
        self.reference_points = copy.deepcopy(reference_points)

    def _bezier_cycle(self, t: float) -> list:
        tmp = copy.deepcopy(self.reference_points)
        tmp_size = len(self.reference_points)
        for i in range(len(self.reference_points)):
            tmp_size -= 1
            for j in range(tmp_size):
                tmp[j] = tmp[j] + (tmp[j+1] - tmp[j])*t
        return tmp

    def get_point(self, t: float) -> Point:
        if (t < 1e-6):
            return self.reference_points[0]
        elif(abs(1-t) < 1e-6):
            return self.reference_points[-1]
        tmp = self._bezier_cycle(t)
        return tmp[0]

    def derivative(self, t: float) -> Line:
        points = copy.deepcopy(self.reference_points)
        if(t < 1E-6):
            p1 = points[0]
            p2 = points[0] + (points[1] - points[0])
            p2 = p2 / distance(points[1], points[0])
            return Line(p1, p2)
        if(abs(1-t) < 1E-6):
            p1 = points[-1]
            p2 = points[-1] - (points[-2] - points[-1])
            p2 = p2 / distance(points[-1], points[-2])
            return Line(p1, p2)
        tmp = self._bezier_cycle(t)
        p1 = tmp[0]
        p2 = tmp[0] + (tmp[1] - tmp[0])
        p2 = p2 / distance(tmp[1], tmp[0])
        return Line(p1, p2)
