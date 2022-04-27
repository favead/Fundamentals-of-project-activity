import re
from point import Point


class Parser:
    def __init__(self, airflow_file: str, circles_file: str):
        self.airflow_file = airflow_file
        self.circles_file = circles_file

    def get_coords(self) -> list:
        points = []
        with open(self.airflow_file, "r") as f:
            for row in f:
                tmp = re.split(r'\s', row)
                x, y = map(float, tmp[0:2])
                points.append(Point(x, y))
        return points

    def get_info_about_circles(self) -> list:
        info = []
        with open(self.circles_file, "r") as f:
            for row in f:
                tmp = row.split()
                x, y = map(float, tmp[0:2])
                n, m = map(int, tmp[-2:])
                info.append([Point(x, y), n, m])
        return info
