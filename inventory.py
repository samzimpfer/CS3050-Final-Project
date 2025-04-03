from gameobjects import *
from resource import ResourceGraphic

class Inventory:

    def __init__(self, show_buttons):
        self.show_buttons = show_buttons

        self.x = 0
        self.y = 0
        self.width = 0

        self.inventory = {
            Resource.BRICK: ResourceGraphic(Resource.BRICK, show_buttons),
            Resource.SHEEP: ResourceGraphic(Resource.SHEEP, show_buttons),
            Resource.STONE: ResourceGraphic(Resource.STONE, show_buttons),
            Resource.WHEAT: ResourceGraphic(Resource.WHEAT, show_buttons),
            Resource.WOOD: ResourceGraphic(Resource.WOOD, show_buttons)
        }


    def set_position_and_size(self, x, y, width):
        resource_sprite_width = width / 8
        spacing = resource_sprite_width * 1.5
        x = x - (width / 2) + resource_sprite_width
        for r in self.inventory.values():
            r.set_position_and_size(x, y, resource_sprite_width)
            x += spacing


    # checks if this inventory contains a certain set of resources specified
    # by dictionary in form { Resource.TYPE: integer_amount }
    def contains(self, need):
        for r, req in need.items():
            if self.inventory[r].amount < req:
                return False
        return True


    # change amounts based on dictionary in form { Resource.TYPE: integer_amount }
    def change_amounts(self, change):
        for r, c in change.items():
            self.inventory[r].change_amount(c)


    # change amounts based on adding another inventory to this inventory
    def combine_with_inventory(self, inv2):
        for t, r in self.inventory.items():
            r.change_amount(inv2[t].amount)


    def on_draw(self):
        for r in self.inventory.values():
            r.on_draw()


    def on_mouse_press(self, x, y):
        for r in self.inventory.values():
            r.on_mouse_press(x, y)


    def on_mouse_motion(self, x, y):
        for r in self.inventory.values():
            r.on_mouse_motion(x, y)