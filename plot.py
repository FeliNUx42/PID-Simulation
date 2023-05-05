import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt


class Plotter:
  def __init__(self):
    self.oldDF = []
    self.df = None

    self.rGraph = None
    self.nGraph = None

  def run(self):
    r = self.rGraph
    n = self.nGraph

    fig, axs = plt.subplots(r+n, figsize=(9.5,7.5))
    fig.canvas.manager.window.title("PID Simulation Results")

    if r and n:
      rax = axs[0]
      nax = axs[1]
    else:
      rax = axs
      nax = axs

    if r: rax.plot(self.df["gAngle"], "k-", linewidth=1, label="Desired Angle")

    for i, oDF in enumerate(self.oldDF):
      if r: rax.plot(oDF["rAngle"], linewidth=1, label=f"Rocket Angle ({i+1})")
      if n: nax.plot(oDF["nAngle"], linewidth=1, label=f"Nozzle Angle ({i+1})")

    if r:
      rax.plot(self.df["rAngle"], "b-", linewidth=1, label=f"Rocket Angle ({len(self.oldDF)+1})")
    if n:
      nax.plot(self.df["middle"], "k-", linewidth=1)
      nax.plot(self.df["nAngle"], "b-", linewidth=1, label=f"Nozzle Angle ({len(self.oldDF)+1})")

    if r:
      rax.set_title("Rocket Angle")
      rax.set_xlabel("Time")
      rax.set_ylabel("Angle (deg)")
      rax.set_xlim((0, self.df.shape[0]-1))
      rax.grid(True, axis="y", linestyle="--")
      rax.legend()

    if n:
      nax.set_title("Nozzle Angle")
      nax.set_xlabel("Time")
      nax.set_ylabel("Angle (deg)")
      nax.set_xlim((0, self.df.shape[0]-1))
      nax.grid(True, axis="y", linestyle="--")
      nax.legend()

    fig.subplots_adjust(left=0.11, right=0.92, bottom=0.1, top=0.9, hspace=0.4)

    plt.show()

  def set(self, df, val):
    if self.df is not None:
      self.oldDF.append(self.df)
    
    self.df = df

    self.rGraph = val["rGraph"]
    self.nGraph = val["nGraph"]

  def clear(self):
    self.oldDF = []
    self.df = None

    self.close()

  def close(self):
    plt.close()

