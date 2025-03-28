import arcade

class Button:

    def __init__(self, text, color):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

        self.main_color = color
        hover_color_amt = 20
        self.hover_color = (color[0] - hover_color_amt, color[1] - hover_color_amt, color[2] - hover_color_amt)

        self.sprites = arcade.SpriteList()
        self.box = arcade.SpriteSolidColor(10, 10, 0, 0, color)
        self.sprites.append(self.box)

        self.text = text

        self.on_click = lambda: None

    def set_pos(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.box.center_x = x
        self.box.center_y = y
        self.box.width = width
        self.box.height = height

    def on_draw(self):
        self.sprites.draw()
        arcade.draw_text(self.text, self.x, self.y, arcade.color.BLACK, font_size=(self.height * 0.5), anchor_x="center", anchor_y="center")

    def on_mouse_press(self, mouse_sprite):
        if arcade.check_for_collision(mouse_sprite, self.box):
            self.on_click()

    def on_mouse_motion(self, mouse_sprite):
        if arcade.check_for_collision(mouse_sprite, self.box):
            self.box.color = self.hover_color
        else:
            self.box.color = self.main_color