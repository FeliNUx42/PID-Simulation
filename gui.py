import customtkinter as ct
import subprocess
import platform

from physics import Simulation
from animation import Animation
from plot import Plotter


class Parameter(ct.CTkFrame):
  def __init__(self, master, text, switch=False):
    super().__init__(master, fg_color="transparent")

    self.columnconfigure((0,1), weight=1)

    self.label = ct.CTkLabel(self, text=text, font=ct.CTkFont(size=14))
    self.label.grid(row=0, column=0, padx=30, sticky="w")

    self.value = ct.StringVar()
    self.switch = switch

    if self.switch:
      self.input = ct.CTkSwitch(self, text="")
      self.input.grid(row=0, column=1, sticky="e")
    else:
      self.input = ct.CTkEntry(self, textvariable=self.value, justify="right", font=ct.CTkFont(size=14))
      self.input.grid(row=0, column=1, padx=30, sticky="e")
  
  def get(self):
    if self.switch:
      return bool(self.input.get())
    else:
      return float(self.value.get())

  def set(self, val):
    if self.switch:
      if val:
        self.input.select()
      else:
        self.input.deselect()
      
    else:
      self.value.set(val)


class RocketFrame(ct.CTkFrame):
  def __init__(self, master):
    super().__init__(master)

    self.columnconfigure(0, weight=1)

    self.title = ct.CTkLabel(self, text="Rocket Settings", font=ct.CTkFont(size=26))
    self.title.grid(row=0, column=0, padx=10, pady=(25,0), sticky="ew")

    self.subtitle0 = ct.CTkLabel(self, text="Simulation Parameters", font=ct.CTkFont(size=18))
    self.subtitle0.grid(row=1, column=0, padx=30, pady=(20, 10), sticky="w")

    self.mmoi = Parameter(self, "MMOI")
    self.mmoi.grid(row=2, column=0, pady=5, sticky="ew")

    self.rAngle = Parameter(self, "Start Rocket Angle (deg)")
    self.rAngle.grid(row=3, column=0, pady=5, sticky="ew")

    self.gAngle = Parameter(self, "Desired Rocket Angle (deg)")
    self.gAngle.grid(row=4, column=0, pady=5, sticky="ew")

    self.nMaxAngle = Parameter(self, "Max Nozzle Angle (deg)")
    self.nMaxAngle.grid(row=5, column=0, pady=5, sticky="ew")

    self.subtitle1 = ct.CTkLabel(self, text="Drawing Parameters", font=ct.CTkFont(size=18))
    self.subtitle1.grid(row=6, column=0, padx=30, pady=(20, 10), sticky="w")

    self.wSize = Parameter(self, "Window Size")
    self.wSize.grid(row=7, column=0, pady=5, sticky="ew")

    self.rLength = Parameter(self, "Rocket Length")
    self.rLength.grid(row=8, column=0, pady=5, sticky="ew")

    self.rWidth = Parameter(self, "Rocket Width")
    self.rWidth.grid(row=9, column=0, pady=5, sticky="ew")

    self.nLength = Parameter(self, "Nozzle Length")
    self.nLength.grid(row=10, column=0, pady=5, sticky="ew")

    self.nWidth = Parameter(self, "Nozzle Width")
    self.nWidth.grid(row=11, column=0, pady=5, sticky="ew")

    self.nRotPoint = Parameter(self, "Nozzle Rotation Point")
    self.nRotPoint.grid(row=12, column=0, pady=(5, 25), sticky="ew")


class PIDFrame(ct.CTkFrame):
  def __init__(self, master):
    super().__init__(master)

    self.columnconfigure(0, weight=1)

    self.title = ct.CTkLabel(self, text="Controller Settings", font=ct.CTkFont(size=26))
    self.title.grid(row=0, column=0, padx=10, pady=(25,20), sticky="n")

    self.kp = Parameter(self, "kp (percent)")
    self.kp.grid(row=1, column=0, pady=5, sticky="ew")

    self.kd = Parameter(self, "kd (derivative)")
    self.kd.grid(row=2, column=0, pady=5, sticky="ew")

    self.ki = Parameter(self, "ki (integral)")
    self.ki.grid(row=3, column=0, pady=5, sticky="ew")

    self.iLength = Parameter(self, "Integral length")
    self.iLength.grid(row=4, column=0, pady=(5, 25), sticky="ew")


class SimulationFrame(ct.CTkFrame):
  def __init__(self, master):
    super().__init__(master)

    self.columnconfigure(0, weight=1)

    self.title = ct.CTkLabel(self, text="Simulation Settings", font=ct.CTkFont(size=26))
    self.title.grid(row=0, column=0, padx=10, pady=(25,20), sticky="ew")

    self.iter = Parameter(self, "Iterations")
    self.iter.grid(row=1, column=0, pady=5, sticky="ew")

    self.fRate = Parameter(self, "Frame Rate")
    self.fRate.grid(row=2, column=0, pady=5, sticky="ew")

    self.rAnim = Parameter(self, "Rocket Animation", switch=True)
    self.rAnim.grid(row=3, column=0, pady=5, sticky="ew")

    self.rGraph = Parameter(self, "Rocket Angle Graph", switch=True)
    self.rGraph.grid(row=4, column=0, pady=5, sticky="ew")

    self.nGraph = Parameter(self, "Nozzle Angle Graph", switch=True)
    self.nGraph.grid(row=5, column=0, pady=(5, 25), sticky="ew")


class BtnFrame(ct.CTkFrame):
  def __init__(self, master):
    super().__init__(master, fg_color="transparent")

    self.columnconfigure((0,1,2,3), weight=1, uniform="fred")

    self.start = ct.CTkButton(self, text="Simulate", command=master.simulate)
    self.start.grid(row=0, column=0, columnspan=2, padx=(0,15), pady=0, sticky="ew")

    self.clear = ct.CTkButton(self, text="Clear History", command=master.plotter.clear)
    self.clear.grid(row=0, column=2, padx=15, pady=0, sticky="ew")

    self.end = ct.CTkButton(self, text="Quit", command=master.destroy)
    self.end.grid(row=0, column=3, padx=(15,0), pady=0, sticky="ew")


class GUI(ct.CTk):
  def __init__(self):
    super().__init__()

    self.plotter = Plotter()
    self.animation = None
    self.simulation = Simulation()


    ct.set_appearance_mode("System")
    ct.set_default_color_theme("blue")

    self.title("PID Simulation")
    self.geometry("1000x690")

    self.columnconfigure((0,1), weight=1, uniform="fred")
    self.rowconfigure((0,1), weight=1)

    self.rocketTab = RocketFrame(self)
    self.rocketTab.grid(row=0, column=0, rowspan=2, padx=(30, 15), pady=(30, 15), sticky="nswe")

    self.pidTab = PIDFrame(self)
    self.pidTab.grid(row=0, column=1, padx=(15, 30), pady=(30, 15), sticky="nswe")

    self.simTab = SimulationFrame(self)
    self.simTab.grid(row=1, column=1, padx=(15, 30), pady=(15, 15), sticky="nswe")

    self.btnTab = BtnFrame(self)
    self.btnTab.grid(row=2, column=0, columnspan=2, padx=30, pady=(15, 30), sticky="nswe")
  
  def run(self):
    self.mainloop()

  def set(self, val):
    self.rocketTab.mmoi.set(val["mmoi"])
    self.rocketTab.rAngle.set(val["rAngle"])
    self.rocketTab.gAngle.set(val["gAngle"])
    self.rocketTab.nMaxAngle.set(val["nMaxAngle"])
    self.rocketTab.wSize.set(val["wSize"])
    self.rocketTab.rLength.set(val["rLength"])
    self.rocketTab.rWidth.set(val["rWidth"])
    self.rocketTab.nLength.set(val["nLength"])
    self.rocketTab.nWidth.set(val["nWidth"])
    self.rocketTab.nRotPoint.set(val["nRotPoint"])

    self.pidTab.kp.set(val["kp"])
    self.pidTab.kd.set(val["kd"])
    self.pidTab.ki.set(val["ki"])
    self.pidTab.iLength.set(val["iLength"]),

    self.simTab.iter.set(val["iter"])
    self.simTab.fRate.set(val["fRate"])
    self.simTab.rAnim.set(val["rAnim"])
    self.simTab.rGraph.set(val["rGraph"])
    self.simTab.nGraph.set(val["nGraph"])

  def get(self):
    try:
      return {
        "mmoi": self.rocketTab.mmoi.get(),
        "rAngle": self.rocketTab.rAngle.get(),
        "gAngle": self.rocketTab.gAngle.get(),
        "nMaxAngle": self.rocketTab.nMaxAngle.get(),
        "wSize": self.rocketTab.wSize.get(),
        "rLength": self.rocketTab.rLength.get(),
        "rWidth": self.rocketTab.rWidth.get(),
        "nLength": self.rocketTab.nLength.get(),
        "nWidth": self.rocketTab.nWidth.get(),
        "nRotPoint": self.rocketTab.nRotPoint.get(),

        "kp": self.pidTab.kp.get(),
        "kd": self.pidTab.kd.get(),
        "ki": self.pidTab.ki.get(),
        "iLength": self.pidTab.iLength.get(),

        "iter": self.simTab.iter.get(),
        "fRate": self.simTab.fRate.get(),
        "rAnim": self.simTab.rAnim.get(),
        "rGraph": self.simTab.rGraph.get(),
        "nGraph": self.simTab.nGraph.get()
      }
    except ValueError:
      self.error()

  def error(self):
    title = "Error"
    body = "Check if all the parameters are valid numbers..."

    if platform.system() == "Linux":
      subprocess.run(["notify-send", "-u", "critical", title, body])
    else:
      print(title)
      print(body)
  
  def simulate(self):
    val = self.get()
    self.plotter.close()

    self.simulation.set(val)
    self.simulation.run()
    df = self.simulation.get()

    if val["rAnim"]:
      self.animation = Animation()
      self.animation.set(val, df)
      self.animation.run()

    if val["rGraph"] or val["nGraph"]:
      self.plotter.set(df, val)
      self.plotter.run()