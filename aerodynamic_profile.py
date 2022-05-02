from point import Point
from point import get_point_by_k_b
from curve import Bezier_Curve
from line import Line
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import copy
import math


class Aerodanymic_Profile:
    def __init__(self, points: list, info: list):
        self.points = points
        self.first_circle = info[0][0]
        self.second_circle = info[1][0]
        self.upper_points, self.down_points = self.slice_points(info)
        self.skeleton = self.build_skeleton()
        self.upper_curve, self.down_curve = self.get_curves()

    def slice_points(self, info: list) -> tuple:
        start_upper, end_upper = info[0][2], info[1][2]
        start_down, end_down = info[0][1], info[1][1]
        upper_points = self.points[end_upper:start_upper]
        down_points = self.points[start_down:end_down]
        return upper_points, down_points

    def get_intersection_point(self) -> Point:
        p0, p0s = self.first_circle, self.second_circle
        k1, b1 = self._get_first_circle_upper_tangent()
        k2, b2 = self._get_first_circle_down_tangent()
        k1s, b1s = self._get_second_circle_upper_tangent()
        k2s, b2s = self._get_second_circle_down_tangent()
        p3 = get_point_by_k_b(k1, k2, b1, b2)
        p3s = get_point_by_k_b(k1s, k2s, b1s, b2s)
        k3, b3 = Line(p3, p0).k, Line(p3, p0).b
        k3s, b3s = Line(p3s, p0s).k, Line(p3s, p0s).b
        p4 = get_point_by_k_b(k3s, k3, b3s, b3)
        return p4

    def build_skeleton(self) -> Bezier_Curve:
        intersection_point = self.get_intersection_point()
        t = [self.first_circle, intersection_point, self.second_circle]
        return Bezier_Curve(t)

    def _get_upper_curve_const_points(self) -> list:
        l_05t = self.skeleton.derivative(0.05)
        k_05t, b_05t = l_05t.get_tangent_equation()
        k_tfcu, b_tfcu = self._get_first_circle_upper_tangent()
        p2 = get_point_by_k_b(k_05t, k_tfcu, b_05t, b_tfcu)
        l_95t = self.skeleton.derivative(0.95)
        k_95t, b_95t = l_95t.get_tangent_equation()
        k_tscu, b_tscu = self._get_second_circle_upper_tangent()
        p5 = get_point_by_k_b(k_95t, k_tscu, b_95t, b_tscu)
        return [self.upper_points[-1], p2, p5, self.upper_points[0]]

    def _get_down_curve_const_points(self) -> list:
        l_05t = self.skeleton.derivative(0.05)
        k_05t, b_05t = l_05t.get_tangent_equation()
        k_tfcu, b_tfcu = self._get_first_circle_down_tangent()
        p2 = get_point_by_k_b(k_05t, k_tfcu, b_05t, b_tfcu)
        l_95t = self.skeleton.derivative(0.95)
        k_95t, b_95t = l_95t.get_tangent_equation()
        k_tscu, b_tscu = self._get_second_circle_down_tangent()
        p5 = get_point_by_k_b(k_95t, k_tscu, b_95t, b_tscu)
        t = [self.down_points[0], p2, p5, self.down_points[-1]]
        return t

    def get_curves(self) -> tuple:
        upper_curve_points = [self.upper_points[-1], self.upper_points[0]]
        down_curve_points = [self.down_points[0], self.down_points[-1]]
        t = [0.25, 0.4, 0.65, 0.8]
        k = copy.deepcopy(self.upper_points)
        k.reverse()
        u_c = self.optimize_curve(upper_curve_points, t, k, True)
        d_c = self.optimize_curve(down_curve_points, t, self.down_points, False)
        return u_c, d_c

    def optimize_curve(self, const_p: list, t_vr: list, train_p: list,
                       is_upper: bool) -> list:
        p = []
        k_b = []
        h0 = []
        for t in t_vr:
            p.append(self.skeleton.get_point(t))
            k, b = self.skeleton.derivative(t).get_tangent_equation()
            k_b.append((k, b))
            h0.append(0.015)
        h0 = np.array(h0)
        res = minimize(loss_func, h0,
                       args=(const_p, train_p, k_b, p, is_upper),
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
        p = [self.upper_points[-1], self.first_circle]
        return Line(p[0], p[1]).get_tangent_equation(is_upper)

    def _get_first_circle_down_tangent(self, is_upper=True):
        return Line(
            self.down_points[0], self.first_circle
            ).get_tangent_equation(is_upper)

    def _get_second_circle_upper_tangent(self, is_upper=True):
        return Line(
            self.upper_points[0], self.second_circle
            ).get_tangent_equation(is_upper)

    def _get_second_circle_down_tangent(self, is_upper=True):
        return Line(
            self.down_points[-1], self.second_circle
            ).get_tangent_equation(is_upper)


def loss_func(h0: list, p: list, train: list, k_b: list,
              p_f_h: list, is_upper: bool) -> float:
    opt_p = []
    for i in range(len(h0)):
        ys = h0[i] + p_f_h[i].y if is_upper else -h0[i] + p_f_h[i].y
        k, b = k_b[i]
        xs = (ys - b) / k
        opt_p.append(Point(xs, ys))
    ref_points = p[:1] + opt_p + p[1:]
    curve = Bezier_Curve(ref_points)
    dt = 1.0 / len(train)
    x_pred, x_now = 0.0, 0.0
    t = 0.0
    s = 0.0
    s1 = 0.0
    p_h, p_t = [], []
    for i in range(len(train)):
        p1, p2 = curve.get_point(t), train[i]
        x_now = p2.x
        s = math.sqrt(
            math.pow(p1.x - p2.x, 2) + math.pow(p1.y - p2.y, 2)
            )
        s1 += s
        if x_now - x_pred > 1E-5:
            t += dt
        x_pred = x_now
        p_h.append(curve.get_point(t))
        p_t.append(train[i])
    fig, ax = plt.subplots()
    ax.scatter([p.x for p in p_h], [p.y for p in p_h], c='green')
    ax.scatter([p.x for p in p_t], [p.y for p in p_t], c='blue')
    ax.set_ylim(-1.0, 0.3)
    ax.set_xlim(-0.1, 0.7)
    plt.show()
    return s1
