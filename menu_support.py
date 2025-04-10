#from scratchpad import WINDOW_WIDTH, WINDOW_HEIGHT
import arcade
from button import Button

#BLANK_BUTTON = Button("", [0,0,0,0])
BLANK_BUTTON = Button("", (255,255,255,255))
screen_width, screen_height = arcade.get_display_size()
WINDOW_WIDTH = screen_width - 100
WINDOW_HEIGHT = screen_height - 100

l = WINDOW_WIDTH / 4
r = (3 * WINDOW_WIDTH) / 4
b = (2 * WINDOW_HEIGHT) / 5
t = (3 * WINDOW_HEIGHT) / 5
r_select_width = r - l
r_select_height = t - b
r_select_section = r_select_width / 5
center_align_offset = r_select_height / 2

def draw_resource_backing():
    arcade.draw_lrbt_rectangle_filled(l, r, b, t, arcade.color.GRAY)

def create_resource_select_buttons():
    buttons = []
    for i in range(5):
        buttons.append(Button("", [0, 0, 0, 0]))
    set_resource_button_positions(buttons)
    return buttons

def set_resource_button_positions(buttons: list[Button]):
    for i, button in enumerate(buttons):
        button.set_pos(
            (l + ((i + 1) * r_select_section)) - center_align_offset,
            WINDOW_HEIGHT / 2,
            r_select_section,
            r_select_height
        )

dc_l = WINDOW_WIDTH / 4
dc_r = (3 * WINDOW_WIDTH) / 4
dc_b = WINDOW_HEIGHT / 4
dc_t = (3 * WINDOW_HEIGHT) / 4
display_width = dc_r - dc_l
display_height = dc_t - dc_b
sprite_width = display_width / 5
sprite_x_offset = sprite_width / 2

sprite_height = display_height / 2
sprite_y_offset = sprite_height / 2

def draw_devcard_backing():
    arcade.draw_lrbt_rectangle_filled(WINDOW_WIDTH / 4,
                                      (3 * WINDOW_WIDTH) / 4,
                                      WINDOW_HEIGHT / 4,
                                      (3 * WINDOW_HEIGHT) / 4,
                                      arcade.color.GRAY)

# this is going to be used every time the dev card menu is opened as button positions are going to be based on dev cards
# in hand. not as fast but a lot easier

def create_devcard_select_buttons():
    buttons = []
    for i in range(10):
        buttons.append(Button("", [0, 0, 0, 0]))
    set_devcard_button_positions(buttons)
    return buttons

def set_devcard_button_positions(buttons: list[Button]):
    colCount = 1
    # this just draws the array of dev cards
    for button in buttons:
        xPos = 0
        yPos = 0
        width = 0
        height = 0
        if colCount > 5:
            xPos = dc_l + (((colCount - 5) * display_width) / 5) - sprite_x_offset
            yPos = dc_b + (display_height / 4)
        else:
            xPos = dc_l + ((colCount * display_width) / 5) - sprite_x_offset
            yPos = dc_b + (3 * (display_height / 4))
        width = sprite_width
        height = sprite_height
        button.set_pos(
            xPos,
            yPos,
            width,
            height
        )
        colCount += 1

def set_buttons_visible(buttons: list[Button]):
    for button in buttons:
        button.set_visible(True)

def set_buttons_not_visible(buttons: list[Button]):
    for button in buttons:
        button.set_visible(False)