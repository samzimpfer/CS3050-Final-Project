from gameobjects import *
from resource import ResourceGraphic

class Inventory:

    DEFAULT_AMOUNTS = {
            Resource.BRICK: 99,
            Resource.SHEEP: 99,
            Resource.STONE: 99,
            Resource.WHEAT: 99,
            Resource.WOOD: 99
    }

    DEFAULT_LIMITS = {
        Resource.BRICK: 1000,
        Resource.SHEEP: 1000,
        Resource.STONE: 1000,
        Resource.WHEAT: 1000,
        Resource.WOOD: 1000
    }

    def __init__(self, show_buttons, on_change=None):
        self.show_buttons = show_buttons

        self.x = 0
        self.y = 0
        self.width = 0

        self.inventory = {
            Resource.BRICK: ResourceGraphic(Resource.BRICK, show_buttons, on_change),
            Resource.SHEEP: ResourceGraphic(Resource.SHEEP, show_buttons, on_change),
            Resource.STONE: ResourceGraphic(Resource.STONE, show_buttons, on_change),
            Resource.WHEAT: ResourceGraphic(Resource.WHEAT, show_buttons, on_change),
            Resource.WOOD: ResourceGraphic(Resource.WOOD, show_buttons, on_change)
        }

        self.limits = {
            Resource.BRICK: ResourceGraphic(Resource.BRICK, show_buttons, on_change),
            Resource.SHEEP: ResourceGraphic(Resource.SHEEP, show_buttons, on_change),
            Resource.STONE: ResourceGraphic(Resource.STONE, show_buttons, on_change),
            Resource.WHEAT: ResourceGraphic(Resource.WHEAT, show_buttons, on_change),
            Resource.WOOD: ResourceGraphic(Resource.WOOD, show_buttons, on_change)
        }


    def set_position_and_size(self, x, y, width):
        resource_sprite_width = width / 8
        spacing = resource_sprite_width * 1.5
        x = x - (width / 2) + resource_sprite_width
        for r in self.inventory.values():
            r.set_position_and_size(x, y, resource_sprite_width)
            x += spacing


    # resets the resource amounts to defaults
    def reset(self):
        self.change_amounts(Inventory.DEFAULT_AMOUNTS)

    # resets limits to "infinity" (1000)
    def reset_limits(self):
        self.set_limits(Inventory.DEFAULT_LIMITS)


    # sets limits for each resource
    def set_limits(self, limits):
        for r, l in limits.items():
            self.inventory[r].set_limit(l)


    # change amounts based on dictionary in form { Resource.TYPE: integer_amount }
    def change_amounts(self, change):
        for r, c in change.items():
            self.inventory[r].change_amount(c)


    # change amounts based on adding another inventory to this inventory
    def combine_with_inventory(self, inv2):
        for t, r in self.inventory.items():
            r.change_amount(inv2[t].amount)


    # returns dictionary of the amounts of each resource currently held in the inventory
    def get_amounts(self):
        amts = {}
        for t, r in self.inventory.items():
            amts[t] = r.amount
        return amts


    # checks if this inventory contains a certain set of resources specified
    # by dictionary in form { Resource.TYPE: integer_amount }
    def contains(self, need):
        for r, req in need.items():
            if self.inventory[r].amount < req:
                return False
        return True


    def on_draw(self):
        for r in self.inventory.values():
            r.on_draw()


    def on_mouse_press(self, x, y):
        for r in self.inventory.values():
            r.on_mouse_press(x, y)


    def on_mouse_motion(self, x, y):
        for r in self.inventory.values():
            r.on_mouse_motion(x, y)