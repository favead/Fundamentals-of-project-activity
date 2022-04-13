from line import Line
from parser import Parser
from curve import BezierCurve
from point import Point
from profile import AerodanymicProfile

parser = Parser("geom_ciam004.txt","004.txt")
points = parser.getCoords()
info = parser.getInfoAboutCircles()
profile = AerodanymicProfile(points,info)
p = profile.getCircleCenters()