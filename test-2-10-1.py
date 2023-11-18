from core.base import Base


class Test(Base):
    def initialize(self):
        print("initializing program...")

    def update(self):
        if self.input.is_key_down("space"):
            print("Space key was pressed down.")


if __name__ == "__main__":
    Test().run()
