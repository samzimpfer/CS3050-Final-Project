import random

import arcade

# This class consists of two dice sprites, which are contained in a clickable box.
# Upon clicking, the dice are animated to "roll" for a few frames.
# When the dice settle, self.sum is set to their sum, and self.ready is set to True.
# NOTE: always use dice.get_sum_and_reset() to retrieve the sum, never dice.sum
class Dice:
    def __init__(self, x, y, w, h):
        # positional fields
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.die1_x = x - (w // 2) + (h // 2)
        self.die2_x = x + (w // 2) - (h // 2)

        # sprites
        self.box = arcade.SpriteSolidColor(w, h, x, y, (0, 0, 0, 0))
        self.die1 = {}
        self.die2 = {}

        for i in range(1, 7):
            sprite1 = arcade.Sprite(f"sprites/dice/{i}.png")
            sprite1.width = self.height
            sprite1.height = self.height
            sprite1.center_x = self.die1_x
            sprite1.center_y = self.y

            sprite2 = arcade.Sprite(f"sprites/dice/{i}.png")
            sprite2.width = self.height
            sprite2.height = self.height
            sprite2.center_x = self.die2_x
            sprite2.center_y = self.y

            self.die1[i] = sprite1
            self.die2[i] = sprite2

        self.sprites = arcade.SpriteList()
        self.sprites.append(self.box)
        self.sprites.append(self.die1[1])
        self.sprites.append(self.die2[1])

        # value fields
        self.value1 = 1
        self.value2 = 1
        self.sum = 0

        # roll animation fields
        self.ready = False # set to True when the dice have settled
        self.rolling = False # set to True when the roll animation is running
        self.roll_timer = 0 # used as a counter for animation purposes
        self.roll_speed = 3 # used to control how fast the animation changes frames (higher number = slower animation)
        self.roll_length = 5 # used to control how long the dice are rolling for (higher number = longer time)

    # sets the dice to a random combination
    def randomize(self):
        self.value1 = random.randrange(1, 7)
        self.value2 = random.randrange(1, 7)
        self.sum = self.value1 + self.value2

        self.sprites.clear()
        self.sprites.append(self.box)
        self.sprites.append(self.die1[self.value1])
        self.sprites.append(self.die2[self.value2])

    def roll(self):
        self.rolling = True

    def get_sum_and_reset(self):
        self.ready = False
        return self.sum

    def on_draw(self):
        self.sprites.draw()

    # runs the rolling animation if rolling is set to True
    def on_update(self, delta_time):
        if self.rolling:
            if self.roll_timer % self.roll_speed == 0:
                self.randomize()
            if self.roll_timer > self.roll_length * self.roll_speed:
                self.rolling = False
                self.ready = True
                self.roll_timer = -1

            self.roll_timer += 1

    def on_mouse_press(self, x, y):
        if self.box.collides_with_point((x, y)):
            self.roll()