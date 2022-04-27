from point import Point


class Line:
    def __init__(self, p1: Point, p2: Point, k=0, b=0) -> None:
        self.p1 = p1
        self.p2 = p2
        self.k = (self.p1.y - self.p2.y) / (self.p1.x - self.p2.x)
        self.b = self.p2.y - self.k * self.p2.x

    def get_tangent_equation(self, is_upper=True) -> tuple:
        n_k = -1/self.k
        p = self.p1 if is_upper else self.p2
        n_b = p.y - n_k * p.x
        return n_k, n_b
