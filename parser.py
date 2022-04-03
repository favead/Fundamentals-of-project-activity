import re;

class Parser:

    def __init__(self, airflow_file:string, circles_file:string):
        self.airflow_file = airflow_file
        self.circles_file = circles_file

    def readAndFillCoords(self, x:list, y:list):
        with open(self.airflow_file,"r") as f:
            for row in f:
                splitRowAndSaveData(row,x,y)

    def reanAndSaveCircleCentres(self, x:list, y:list):
        with open(self.circles_file,"r") as f:
            for row in f:
                splitRowAndSaveData(row,x,y)

    def splitRowAndSaveData(self,row:string,x:list,y:list):
        tmp = re.split(r'\s',row)
        x.append(float(tmp[0]))
        y.append(float(tmp[1]))