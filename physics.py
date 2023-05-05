import pandas as pd
import settings
import math


class Simulation:
  def __init__(self):
    self.gAngle = None
    self.rAngle = None
    self.rAngularVel = None
    self.rMMMOI = None

    self.nAngle = None
    self.maxAngle = None

    self.kp = None
    self.kd = None
    self.ki = None

    self.iter = None

    self.oldAngle = None
    self.error = None

    self.df = None
  
  def run(self):
    self.log()
    for _ in range(int(self.iter)):
      self.step()
      self.log()
  
  def set(self, val):
    self.gAngle = math.radians(val["gAngle"])
    self.rAngle = math.radians(val["rAngle"])
    self.rAngularVel = 0
    self.rMMMOI = val["mmoi"]

    self.nAngle = 0
    self.maxAngle = math.radians(val["nMaxAngle"])

    self.kp = val["kp"]
    self.kd = val["kd"]
    self.ki = val["ki"]

    self.iter = val["iter"]

    self.oldAngle = self.rAngle
    self.error = [0 for _ in range(int(val["iLength"]))]

    self.df = pd.DataFrame(settings.logs)
  
  def get(self):
    return self.df

  def clamp(self, n, diff):
    return max(min(diff, n), -diff)

  def step(self):
    err = perc = self.rAngle - self.gAngle
    derv = self.rAngle - self.oldAngle
    intgr = sum(self.error)

    self.oldAngle = self.rAngle

    a = perc*self.kp + derv*self.kd + intgr*self.ki
    self.nAngle = self.clamp(a, self.maxAngle)

    acc = math.sin(self.nAngle) / self.rMMMOI
    self.rAngularVel += acc
    self.rAngle -= self.rAngularVel

    self.error.pop(0)
    self.error.append(err)

  def log(self):
    self.df.loc[len(self.df)] = [
      0,
      math.degrees(self.gAngle),
      math.degrees(self.rAngle),
      math.degrees(self.nAngle)
    ]
