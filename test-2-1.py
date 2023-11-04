from core.base import Base

class Test(Base):

    def initialize(self):
        print("initializing program ...")

    def update(self):
        pass

if __name__ == "__main__":
    Test().run()