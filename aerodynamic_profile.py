from point import Point
from curve import Bezier_Curve
from line import Line
import numpy as np
from scipy.optimize import minimize
import copy
import math


class Aerodanymic_Profile:
    def __init__(self, points: list, info: list):
        self.points = points
        self.firstCircle = info[0][0]
        self.secondCircle = info[1][0]
        self.upperPoints, self.downPoints = self.slice_points(info)
        self.skeleton = self.build_skeleton()
        self.upper_curve_const_points = self._get_upper_curve_const_points()
        self.down_curve_const_points = self._get_down_curve_const_points()
        self.upper_curve, self.down_curve = self.get_curves()

    def slice_points(self, info: list) -> tuple:
        startUpper, endUpper = info[0][2], info[1][2]
        startDown, endDown = info[0][1], info[1][1]
        upperPoints = self.points[endUpper:startUpper]
        downPoints = self.points[startDown:endDown]
        return upperPoints, downPoints

    def get_intersection_point(self) -> Point:
        p0, p0s = self.firstCircle, self.secondCircle
        k1, b1 = self._get_first_circle_upper_tangent()
        k2, b2 = self._get_first_circle_down_tangent()
        k1s, b1s = self._get_second_circle_upper_tangent()
        k2s, b2s = self._get_second_circle_down_tangent()
        x3 = (b1 - b2) / (k2 - k1)
        y3 = k2 * x3 + b2
        x3s = (b1s - b2s) / (k2s - k1s)
        y3s = k2s * x3s + b2s
        p3, p3s = Point(x3, y3), Point(x3s, y3s)
        k3, b3 = Line(p3, p0).k, Line(p3, p0).b
        k3s, b3s = Line(p3s, p0s).k, Line(p3s, p0s).b
        x4 = (b3s - b3) / (k3 - k3s)
        y4 = k3s * x4 + b3s
        return Point(x4, y4)

    def build_skeleton(self) -> Bezier_Curve:
        intersection_point = self.get_intersection_point()
        t = [self.firstCircle, intersection_point, self.secondCircle]
        return Bezier_Curve(t)

    def _get_upper_curve_const_points(self) -> list:
        l_15t = self.skeleton.derivative(0.15)
        k_15t, b_15t = l_15t.get_tangent_equation()
        k_tfcu, b_tfcu = self._get_first_circle_upper_tangent()
        x2 = (b_15t - b_tfcu) / (k_tfcu - k_15t)
        y2 = k_15t * x2 + b_15t
        p2 = Point(x2, y2)
        l_75t = self.skeleton.derivative(0.85)
        k_75t, b_75t = l_75t.get_tangent_equation()
        k_tscu, b_tscu = self._get_second_circle_upper_tangent()
        x5 = (b_75t - b_tscu) / (k_tscu - k_75t)
        y5 = k_75t * x5 + b_75t
        p5 = Point(x5, y5)
        t = [self.upperPoints[-1], p2, p5, self.upperPoints[0]]
        return t

    def _get_down_curve_const_points(self) -> list:
        l_15t = self.skeleton.derivative(0.15)
        k_15t, b_15t = l_15t.get_tangent_equation()
        k_tfcu, b_tfcu = self._get_first_circle_down_tangent()
        x2 = (b_15t - b_tfcu) / (k_tfcu - k_15t)
        y2 = k_15t * x2 + b_15t
        p2 = Point(x2, y2)
        l_75t = self.skeleton.derivative(0.85)
        k_75t, b_75t = l_75t.get_tangent_equation()
        k_tscu, b_tscu = self._get_second_circle_down_tangent()
        x5 = (b_75t - b_tscu) / (k_tscu - k_75t)
        y5 = k_75t * x5 + b_75t
        p5 = Point(x5, y5)
        t = [self.downPoints[0], p2, p5, self.downPoints[-1]]
        return t

    def get_curves(self) -> tuple:
        upper_curve_points = [self.upperPoints[-1], self.upperPoints[0]]
        down_curve_points = [self.downPoints[0], self.downPoints[-1]]
        t = [0.15, 0.45, 0.75, 0.92]
        k = copy.deepcopy(self.upperPoints)
        k.reverse()
        u_c = self.optimize_curve(upper_curve_points, t, k)
        d_c = self.optimize_curve(down_curve_points, t, self.downPoints)
        return u_c, d_c

    def optimize_curve(self, const_p: list, t_vr: list, train_p: list) -> list:
        p = []
        k_b = []
        h0 = []
        for t in t_vr:
            p.append(self.skeleton.get_point(t))
            k, b = self.skeleton.derivative(t).get_tangent_equation()
            k_b.append((k, b))
            h0.append(0.015)
        h0 = np.array(h0)
        res = minimize(loss_func, h0, args=(const_p, train_p, k_b, p),
                       method='CG', options={'disp': True})
        h = res.x
        opt_p = []
        for i in range(len(h)):
            ys = h[i] + p[i].y
            k, b = k_b[i]
            xs = (ys - b) / k
            opt_p.append(Point(xs, ys))
        ref_points = const_p[:1] + opt_p + const_p[1:]
        curve = Bezier_Curve(ref_points)
        return curve

    def _get_first_circle_upper_tangent(self, is_upper=True):
        p = [self.upperPoints[-1], self.firstCircle]
        return Line(p[0], p[1]).get_tangent_equation(is_upper)

    def _get_first_circle_down_tangent(self, is_upper=True):
        return Line(
            self.downPoints[0], self.firstCircle
            ).get_tangent_equation(is_upper)

    def _get_second_circle_upper_tangent(self, is_upper=True):
        return Line(
            self.upperPoints[0], self.secondCircle
            ).get_tangent_equation(is_upper)

    def _get_second_circle_down_tangent(self, is_upper=True):
        return Line(
            self.downPoints[-1], self.secondCircle
            ).get_tangent_equation(is_upper)


def loss_func(h0: list, p: list, train: list, k_b: list, p_f_h: list) -> float:
    opt_p = []
    for i in range(len(h0)):
        ys = h0[i] + p_f_h[i].y
        k, b = k_b[i]
        xs = (ys - b) / k
        opt_p.append(Point(xs, ys))
    ref_points = p[:1] + opt_p + p[1:]
    curve = Bezier_Curve(ref_points)
    dt = 1.0 / len(train)
    t = 0.0
    s = 0.0
    s1 = 0.0
    p_h, p_t = [], []
    for i in range(len(train)):
        p1, p2 = curve.get_point(t), train[i]
        s = math.sqrt(
            math.pow(p1.x - p2.x, 2) + math.pow(p1.y - p2.y, 2)
            )
        s1 += s
        t += dt
        p_h.append(curve.get_point(t))
        p_t.append(train[i])
#    fig, ax = plt.subplots()
#    ax.scatter([p.x for p in p_h], [p.y for p in p_h], c='green')
#    ax.scatter([p.x for p in p_t], [p.y for p in p_t], c='blue')
#    ax.set_ylim(-1.0, 0.2)
#    ax.set_xlim(-0.1, 0.7)
#    plt.show()
    return s1
