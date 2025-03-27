import random

import arcade

class Dice:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.box = arcade.SpriteSolidColor(w, h, x, y, (0, 0, 0, 0))

        self.die1_x = x - (w // 2) + (h // 2)
        self.die2_x = x + (w // 2) - (h // 2)

        self.value1 = 1
        self.value2 = 1
        self.sum = 0
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

        self.ready = False
        self.rolling = False
        self.roll_timer = 0
        self.roll_speed = 3
        self.roll_length = 5

    def randomize(self):
        self.value1 = random.randrange(1, 7)
        self.value2 = random.randrange(1, 7)

        self.sprites.clear()
        self.sprites.append(self.box)
        self.sprites.append(self.die1[self.value1])
        self.sprites.append(self.die2[self.value2])

    def roll(self):
        self.rolling = True

    def on_draw(self):
        self.sprites.draw()

    def on_update(self, delta_time):
        if self.rolling:
            if self.roll_timer % self.roll_speed == 0:
                self.randomize()
            if self.roll_timer > self.roll_length * self.roll_speed:
                self.rolling = False
                self.sum = self.value1 + self.value2
                self.ready = True
                self.roll_timer = -1

            self.roll_timer += 1

    def on_mouse_press(self, mouse_sprite):
        if arcade.check_for_collision(mouse_sprite, self.box):
            self.roll()