from pyglet import window, shapes, app, gl, text
import math


class Animation:
  def __init__(self):
    self.wS = None
    self.fR = None
    self.rL = None
    self.rW = None
    self.nL = None
    self.nW = None
    self.nR = None
    self.iter = None

    self.df = None
    self.i = None
    self.finished = None

    self.window = None
    self.rocket = None
    self.nozzle = None

  def run(self):
    try:
      app.run(interval=1/self.fR)
    except:
      pass

  def set(self, val, df):
    self.wS = int(val["wSize"])
    self.fR = val["fRate"]
    self.rL = val["rLength"]
    self.rW = val["rWidth"]
    self.nL = val["nLength"]
    self.nW = val["nWidth"]
    self.nR = val["nRotPoint"]
    self.iter = val["iter"]

    self.df = df
    self.i = 0
    self.done = text.Label(
      "Done",
      x=20, y=20, 
      font_size=16,
      color=(122,127,130,255)
    )

    self.window = window.Window(self.wS,self.wS, resizable=True)

    self.rocket = shapes.Polygon(
      (0,0), (self.rW,0), (self.rW,self.rL),
      (self.rW/2,self.rL+self.rW), (0,self.rL),
      color=(86,91,94)
    )
    self.rocket.anchor_position = (self.rW/2, self.rL/2)

    self.nozzle = shapes.Rectangle(
      x=0, y=0, width=self.nW, height=self.nL,
      color=(122,127,130)
    )
    self.nozzle.anchor_position = (self.nW/2, self.nL-self.nR)

    @self.window.event
    def on_draw():
      self.draw()

  def draw(self):
    if self.i > self.iter:
      self.done.draw()
      return

    rA = self.df.loc[self.i]["rAngle"]
    nA = self.df.loc[self.i]["nAngle"]
    self.rocket.rotation = rA
    self.nozzle.rotation = rA + nA

    self.i += 1

    self.rocket.x = self.window.width/2
    self.rocket.y = self.window.height/2

    t = math.radians(rA) + 0

    self.nozzle.x = self.window.width/2 - math.sin(t) * self.rL/2
    self.nozzle.y = self.window.height/2 - math.cos(t) * self.rL/2

    gl.glClearColor(0.141,0.141,0.141,1)
    self.window.clear()
    self.nozzle.draw()
    self.rocket.draw()