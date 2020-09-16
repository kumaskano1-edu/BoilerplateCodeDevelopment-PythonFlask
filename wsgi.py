from run import create_app, app
if __name__ == "__main__":
  app = create_app("config")
  app.run()