from parser import Parser

parser = Parser("geom_ciam004.txt")
x,y = [],[]
parser.readAndFillCoords(x,y)
print(x,y)