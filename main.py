from gui import GUI
import settings


if __name__ == "__main__":
  app = GUI()
  app.set(settings.default)
  app.run()
