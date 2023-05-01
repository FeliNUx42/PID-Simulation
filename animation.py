import pygame
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

    self.screen = None
    self.rSurface = None
    self.nSurface = None

  def run(self):
    pygame.init()
    self.screen = pygame.display.set_mode((self.wS, self.wS))
    pygame.display.set_caption("PID Animation")
    clock = pygame.time.Clock()

    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          return pygame.quit()
        
      self.screen.fill((36,36,36))
      self.draw()
      
      pygame.display.update()
      clock.tick(self.fR)

  def set(self, val, df):
    self.wS = val["wSize"]
    self.fR = val["fRate"]
    self.rL = rL = val["rLength"]
    self.rW = rW = val["rWidth"]
    self.nL = nL = val["nLength"]
    self.nW = nW = val["nWidth"]
    self.nR = nR = val["nRotPoint"]
    self.iter = val["iter"]

    self.df = df
    self.i = 0

    self.rSurface = pygame.Surface((rW, rL+2*rW), pygame.SRCALPHA)
    pygame.draw.polygon(
      self.rSurface, (86,91,94),
      ((rW/2,0), (0,rW), (0,rL+rW), (rW,rL+rW), (rW,rW))
    )

    self.nSurface = pygame.Surface((nW, 2*(nL-nR)), pygame.SRCALPHA)
    pygame.draw.rect(self.nSurface, (122,127,130), (0,nL-2*nR,nW,nL))

  def draw(self):
    rA = self.df.loc[self.i]["rAngle"]
    nA = self.df.loc[self.i]["nAngle"]

    self.i += 1

    rPos = (self.wS/2, self.wS/2)
    nPos = [
      self.wS/2 + math.sin(math.radians(rA)) * self.rL/2,
      self.wS/2 + math.cos(math.radians(rA)) * self.rL/2
    ]

    rRotated = pygame.transform.rotate(self.rSurface, rA)    
    nRotated = pygame.transform.rotate(self.nSurface, rA+nA)

    rRect = rRotated.get_rect(center=rPos)
    nRect = nRotated.get_rect(center=nPos)

    self.screen.blit(nRotated, nRect)
    self.screen.blit(rRotated, rRect)

    if self.i > self.iter:
      font = pygame.font.Font(None, 36)
      text = font.render("Finished", True, (122,127,130))
      self.screen.blit(text, (30,self.wS-48))

      self.i -= 1

      self.df.loc[self.i]["rAngle"] = int(self.df.loc[self.i]["rAngle"])
      self.df.loc[self.i]["nAngle"] = int(self.df.loc[self.i]["nAngle"])


