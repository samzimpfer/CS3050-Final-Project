from gameobjects import *
import arcade

class Button:

    def __init__(self, text, clear=False):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.hover_width = 0
        self.hover_height = 0
        self.hover_expand_amt = 3
        self.color = BUTTON_COLOR
        self.is_clear = clear
        if self.is_clear:
            self.color = (0, 0, 0, 0)
        self.sprites = arcade.SpriteList()

        self.box = arcade.SpriteSolidColor(10, 10, 0, 0, self.color)
        self.sprites.append(self.box)

        self.og_color = BUTTON_COLOR
        self.hover_transparent_shade = (0, 0, 0, 50)

        self.text = text

        self.on_click = None

        self.show = False


    def set_visible(self, visible):
        self.show = visible


    def set_position_and_size(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hover_width = width + self.hover_expand_amt
        self.hover_height = height + self.hover_expand_amt

        self.box.center_x = x
        self.box.center_y = y
        self.box.width = width
        self.box.height = height


    def on_draw(self):
        if self.show:
            self.sprites.draw()
            arcade.draw_text(self.text, self.x, self.y, arcade.color.BLACK, font_size=(self.box.height * 0.5), anchor_x="center", anchor_y="center")


    def on_mouse_press(self, x, y):
        if self.show and self.box.collides_with_point((x, y)):
            self.on_click()


    def on_mouse_motion(self, x, y):
        if self.show and self.box.collides_with_point((x, y)):
            self.box.width = self.hover_width
            self.box.height = self.hover_height
            if self.is_clear:
                self.box.color = self.hover_transparent_shade
        else:
            self.box.width = self.width
            self.box.height = self.height
            self.box.color = self.color