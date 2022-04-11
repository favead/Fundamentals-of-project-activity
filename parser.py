import re;

class Parser:
  def __init__(self, airflow_file:str, circles_file:str):
    self.airflow_file = airflow_file
    self.circles_file = circles_file

  def getCoords(self):
    x,y = [],[]
    with open(self.airflow_file,"r") as f:
      for row in f:
        self.splitRowAndSaveData(row,x,y)
    return x,y

  def getCircleCentres(self):
    x,y = [],[]
    with open(self.circles_file,"r") as f:
      for row in f:
        self.splitRowAndSaveData(row,x,y)
    return x,y

  def splitRowAndSaveData(self,row:str,x:list,y:list):
    tmp = re.split(r'\s',row)
    x.append(float(tmp[0]))
    y.append(float(tmp[1]))
