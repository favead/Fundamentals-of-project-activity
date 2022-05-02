from parser import Parser
from aerodynamic_profile import Aerodanymic_Profile
import matplotlib.pyplot as plt


parser = Parser("geom_claim176.txt", "176.txt")
points = parser.get_coords()
info = parser.get_info_about_circles()
profile = Aerodanymic_Profile(points, info)
fig, ax = plt.subplots()


def show(profile: Aerodanymic_Profile):
    p_h = []
    p_d = []
    for t in range(100):
        t = float(t/100)
        p_h.append(profile.upper_curve.get_point(t))
        p_d.append(profile.down_curve.get_point(t))
    ax.scatter([p.x for p in p_h], [p.y for p in p_h], c='green')
    ax.scatter([p.x for p in p_d], [p.y for p in p_d], c='blue')
    plt.show()


def show_points(profile):
    p_h = profile.upper_curve_const_points
    p_d = profile.down_curve_const_points
    ps = []
    ps.append(profile.skeleton.get_point(0.3))
    ps.append(profile.skeleton.get_point(0.45))
    ps.append(profile.skeleton.get_point(0.7))
    ax.scatter([p.x for p in p_h], [p.y for p in p_h], c='green')
    ax.scatter([p.x for p in p_d], [p.y for p in p_d], c='red')
    ax.scatter([p.x for p in ps], [p.y for p in ps], c='orange')
    plt.show()


def show_tangent(p):
    k, b = p._get_second_circle_upper_tangent()
    k2, b2 = p._get_second_circle_down_tangent()
    k3, b3 = p._get_first_circle_down_tangent()
    k4, b4 = p._get_first_circle_upper_tangent()
    ax.plot([pd.x for pd in p.points], [b + k * pd.x for pd in p.points],
            c='red')
    ax.plot([pd.x for pd in p.points], [b2 + k2 * pd.x for pd in p.points],
            c='orange')
    ax.plot([pd.x for pd in p.points], [b3 + k3 * pd.x for pd in p.points],
            c='green')
    ax.plot([pd.x for pd in p.points], [b4 + k4 * pd.x for pd in p.points],
            c='purple')
    ax.scatter([pd.x for pd in p.points], [pd.y for pd in p.points], c='blue')
    ax.set_ylim(-1.0, 0.3)
    ax.set_xlim(-0.05, 0.7)
    plt.show()


def show_curves(p):
    b1, b2 = p.upper_curve, p.down_curve
    pb1, pb2 = [], []
    pbs = []
    for t in range(25):
        pb1.append(b1.get_point(t / 100.0 * 4.0))
        pb2.append(b2.get_point(t / 100.0 * 4.0))
        pbs.append(p.skeleton.get_point(t / 100.0 * 4.0))
    ax.scatter([p.x for p in pb1], [p.y for p in pb1], c='green')
    ax.scatter([p.x for p in pb2], [p.y for p in pb2], c='red')
    ax.scatter([p.x for p in pbs], [p.y for p in pbs], c='orange')
    ax.set_ylim(-0.85, 0.25)
    ax.set_xlim(-0.1, 0.7)
    plt.show()


def show_profile(p):
    ax.scatter([p.x for p in p.points], [p.y for p in p.points], c='blue')
    ax.set_ylim(-0.85, 0.25)
    ax.set_xlim(-0.1, 0.7)
    plt.show()


show_curves(profile)
show_profile(profile)
