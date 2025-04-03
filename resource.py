from gameobjects import *
from button import Button
import arcade

class ResourceGraphic:

    def __init__(self, resource, show_buttons, on_change):
        self.resource_type = resource
        self.amount = 0
        self.limit = 100

        self.x = 0
        self.y = 0
        self.width = 0

        self.sprite = None
        if self.resource_type == Resource.BRICK:
            self.sprite = arcade.Sprite("sprites/resources/brick.png")
        elif self.resource_type == Resource.SHEEP:
            self.sprite = arcade.Sprite("sprites/resources/sheep.png")
        elif self.resource_type == Resource.STONE:
            self.sprite = arcade.Sprite("sprites/resources/stone.png")
        elif self.resource_type == Resource.WHEAT:
            self.sprite = arcade.Sprite("sprites/resources/wheat.png")
        elif self.resource_type == Resource.WOOD:
            self.sprite = arcade.Sprite("sprites/resources/wood.png")
        self.sprites = arcade.SpriteList()
        self.sprites.append(self.sprite)


        self.show_buttons = show_buttons
        self.dec_button = None
        self.inc_button = None
        if show_buttons:
            self.dec_button = Button("-")
            self.inc_button = Button("+")
            self.dec_button.on_click = self.decrement
            self.inc_button.on_click = self.increment
        self.on_change = on_change


    def set_limit(self, limit):
        self.limit = limit


    def change_amount(self, change):
        if change < 0:
            for _ in range(-change):
                self.decrement()
        else:
            for _ in range(change):
                self.increment()


    def increment(self):
        if self.amount < self.limit:
            self.amount += 1
            if self.on_change is not None:
                self.on_change()


    def decrement(self):
        if self.amount > 0:
            self.amount -= 1
            if self.on_change is not None:
                self.on_change()


    def set_position_and_size(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width

        self.sprite.center_x = x
        self.sprite.center_y = y
        self.sprite.width = width
        self.sprite.height = width

        if self.show_buttons:
            self.dec_button.set_position_and_size(self.x - (self.width / 4), self.y - (self.width * 1.5),
                                                  (self.width / 2), (self.width / 2))
            self.inc_button.set_position_and_size(self.x + (self.width / 4), self.y - (self.width * 1.5),
                                                  (self.width / 2), (self.width / 2))
            self.dec_button.set_visible(True)
            self.inc_button.set_visible(True)


    def on_draw(self):
        self.sprites.draw()

        arcade.draw_text(f"x{self.amount}", self.sprite.center_x,
                         self.sprite.center_y - self.width, arcade.color.BLACK,
                         font_size=(self.width / 3), anchor_x="center")

        if self.show_buttons:
            self.dec_button.on_draw()
            self.inc_button.on_draw()


    def on_mouse_press(self, x, y):
        if self.show_buttons:
            self.dec_button.on_mouse_press(x, y)
            self.inc_button.on_mouse_press(x, y)


    def on_mouse_motion(self, x, y):
        if self.show_buttons:
            self.dec_button.on_mouse_motion(x, y)
            self.inc_button.on_mouse_motion(x, y)