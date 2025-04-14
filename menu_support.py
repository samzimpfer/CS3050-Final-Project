#from scratchpad import WINDOW_WIDTH, WINDOW_HEIGHT
import arcade
from button import Button

#BLANK_BUTTON = Button("", [0,0,0,0])
BLANK_BUTTON = Button("", True)
screen_width, screen_height = arcade.get_display_size()
WINDOW_WIDTH = screen_width - 100
WINDOW_HEIGHT = screen_height - 100
#print(WINDOW_WIDTH, WINDOW_HEIGHT)

SPRITE_PATHS = {
        0:"sprites/resources/brick.png",
        1:"sprites/resources/sheep.png",
        2:"sprites/resources/stone.png",
        3:"sprites/resources/wheat.png",
        4:"sprites/resources/wood.png"
    }

l = WINDOW_WIDTH / 4
r = (3 * WINDOW_WIDTH) / 4
b = (2 * WINDOW_HEIGHT) / 5
t = (3 * WINDOW_HEIGHT) / 5
r_select_width = r - l
r_select_height = t - b
r_select_section = r_select_width / 5
center_align_offset = r_select_height / 2

YOP_selection_spacing = (
    ((WINDOW_WIDTH / 2) - (r_select_width / 2), t + (r_select_height / 2),r_select_width,r_select_height),
    ((WINDOW_WIDTH / 2) + (r_select_width / 2), t + (r_select_height / 2),r_select_width,r_select_height)
)

def get_YOP_selection_sprite(pathname, selection_num):
    sprite = arcade.Sprite(pathname, center_y=t + (r_select_height / 2))
    if selection_num == 1:
        sprite.center_x = (WINDOW_WIDTH / 2) - (r_select_section / 2)
    else:
        sprite.center_x = (WINDOW_WIDTH / 2) + (r_select_section / 2)
    sprite.width = r_select_section
    sprite.height = r_select_height
    return sprite

def draw_YOP_selection_backing():
    arcade.draw_lrbt_rectangle_filled((WINDOW_WIDTH / 2) - r_select_section,
                                      (WINDOW_WIDTH / 2) + r_select_section,
                                      t,
                                      t + r_select_height,
                                      arcade.color.GRAY,)

single_selection_spacing = (WINDOW_WIDTH / 2, t + (r_select_height / 2),r_select_width,r_select_height)

def draw_single_selection_backing():
    arcade.draw_lrbt_rectangle_filled((WINDOW_WIDTH / 2) - (r_select_section / 2),
                                      (WINDOW_WIDTH / 2) + (r_select_section / 2),
                                      t,
                                      t + r_select_height,
                                      arcade.color.GRAY)

def get_single_selection_sprite(pathname):
    sprite = arcade.Sprite(pathname,
                           center_y=t + r_select_height / 2,
                           center_x=WINDOW_WIDTH / 2)
    sprite.width = r_select_section
    sprite.height = r_select_height
    return sprite


def draw_default_resource_view():
    draw_resource_backing()
    #print(f"from ms: {r_select_section, r_select_width, r_select_height}")
    for i in range(5):
        # sprite = arcade.Sprite(SPRITE_PATHS[i],
        #                        center_x=(l + ((i + 1) * r_select_section)) - center_align_offset,
        #                        center_y=WINDOW_HEIGHT / 2,
        #                        width=r_select_section,
        #                        height=r_select_height)
        sprite = arcade.Sprite(SPRITE_PATHS[i],
                               center_x=(l + ((i + 1) * r_select_section)) - center_align_offset,
                               center_y=WINDOW_HEIGHT / 2)
        sprite.width = r_select_section
        sprite.height = r_select_height
        #print(f"scale {sprite.scale}")
        arcade.draw_sprite(sprite)


SIZE_SCALAR = 2 / 3

trade_selection_spacing = (
    ((l + ((0 + 1) * r_select_section)) - center_align_offset,
            WINDOW_HEIGHT / 2,
            SIZE_SCALAR * r_select_section,
            r_select_height
    ),
    ((l + ((1 + 1) * r_select_section)) - center_align_offset,
            WINDOW_HEIGHT / 2,
            SIZE_SCALAR * r_select_section,
            SIZE_SCALAR * r_select_height
    ),
    ((l + ((2 + 1) * r_select_section)) - center_align_offset,
            WINDOW_HEIGHT / 2,
            SIZE_SCALAR * r_select_section,
            SIZE_SCALAR * r_select_height
    ),
    ((l + ((3 + 1) * r_select_section)) - center_align_offset,
            WINDOW_HEIGHT / 2,
            SIZE_SCALAR * r_select_section,
            SIZE_SCALAR * r_select_height
    ),
    ((l + ((4 + 1) * r_select_section)) - center_align_offset,
            WINDOW_HEIGHT / 2,
            SIZE_SCALAR * r_select_section,
            SIZE_SCALAR * r_select_height
    )
)
#defaults to position based on center with height and width, if not the origin is left bottom corner
def get_positional_scaled_resource_display(xPos, yPos, scalar=1, origin_center=True):
    positions = []
    scaled_width = r_select_width * scalar
    scaled_height = r_select_height * scalar
    scaled_r_select_section = r_select_width / 5
    scaled_center_align_offset = scaled_r_select_section / 2
    if origin_center:
        xPos = xPos - (scaled_width / 2)
        yPos = yPos - (scaled_height / 2)

    for i in range(5):
        positions.append(
            {"path":SPRITE_PATHS[i],
             "center_x": (xPos + ((i + 1) * scaled_r_select_section)) - scaled_center_align_offset,
             "center_y": yPos + (scaled_height / 2),
             "width": scaled_r_select_section,
             "height": scaled_height
             }
        )
    return positions

def get_positional_scaled_sprites(xPos, yPos, scalar=1, origin_center=True, give_button_positions=False):
    positions = get_positional_scaled_resource_display(xPos, yPos, scalar, origin_center)
    sprites = []
    for position in positions:
        sprite = arcade.Sprite(**position)
        sprites.append(sprite)
    return sprites





# trade_selection_spacing = (
#     ((l + ((0 + 1) * r_select_section)) - center_align_offset,
#             WINDOW_HEIGHT / 2,
#             r_select_section,
#             r_select_height
#     ),
#     ((l + ((1 + 1) * r_select_section)) - center_align_offset,
#             WINDOW_HEIGHT / 2,
#             r_select_section,
#             r_select_height
#     ),
#     ((l + ((2 + 1) * r_select_section)) - center_align_offset,
#             WINDOW_HEIGHT / 2,
#             r_select_section,
#             r_select_height
#     ),
#     ((l + ((3 + 1) * r_select_section)) - center_align_offset,
#             WINDOW_HEIGHT / 2,
#             r_select_section,
#             r_select_height
#     )
# )




def draw_resource_backing():
    arcade.draw_lrbt_rectangle_filled(l, r, b, t, arcade.color.GRAY)

def create_resource_select_buttons():
    buttons = []
    for i in range(5):
        buttons.append(Button("", True))
    set_resource_button_positions(buttons)
    return buttons

#TODO: make this constant
def set_resource_button_positions(buttons: list[Button]):
    for i, button in enumerate(buttons):
        button.set_position_and_size(
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
#TODO: make this constant
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
        button.set_position_and_size(
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
