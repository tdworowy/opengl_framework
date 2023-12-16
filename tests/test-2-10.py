from core.base import Base


class Test(Base):
    def initialize(self):
        print("initializing program...")

    def update(self):
        if len(self.input.key_down_list) > 0:
            print(f"Keys down: {self.input.key_down_list}")

        if len(self.input.key_up_list) > 0:
            print(f"Keys up: {self.input.key_up_list}")

        if len(self.input.key_pressed_list) > 0:
            print(f"Keys pressed: {self.input.key_pressed_list}")


if __name__ == "__main__":
    Test().run()
