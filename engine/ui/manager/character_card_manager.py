import pygame

from engine.ui.core.manager import Manager
from engine.ui.core.bindable import Bindable
from engine.ui.core.renderable import Renderable
from engine.ui.core.zone import Zone

from engine.ui.element.window import Window
from engine.ui.element.text import Text
from engine.ui.element.image import Image
from engine.ui.element.bar import Bar
from engine.ui.element.item_icon import ItemIcon
from engine.ui.element.move_icon import MoveIcon

class CharacterCardManager(Manager):
    """Manages the rendering of the character card ui and all
    relevant variables and updates (inventory, moves, etc.)"""


    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.scale = 3
        self.cur_plyr = None
        self.win = Window(400, 400, self.x, self.y)
        self.plyr_img = None
        self.plyr_name = None
        self.plyr_hlth = None
        self.plyr_stats = None
        self.plyr_eqp = []
        self.ply_mv = []
        self.ply_inv = []
        # Ensure code doesn't try to render None or will crash


    def update(self, game):
        # add another condition so doesn't update unnecessarily
        # like during battles
        # only updates renderables when selected player changed
        if game.selected_player != self.cur_plyr:
            # update player
            self.cur_plyr = game.selected_player
            # update image
            img = pygame.image.load(self.cur_plyr.portrait)
            scl_img = pygame.transform.scale(img, (img.get_width()*self.scale, img.get_height()*self.scale))
            self.plyr_img = Image(scl_img, self.x+10, self.y+25)
            # update name
            self.plyr_name = Text(self.cur_plyr.name, 22, self.x+25, self.y+10)
            # update health bar
            self.plyr_hlth = Bar(100, 5, (116, 154, 104), self.x+10, self.plyr_img.y+self.plyr_img.surface.get_height()+10)
            self.plyr_hlth.percent = 100*self.cur_plyr.get_cur_health()/self.cur_plyr.get_stat("health")
            # update stats
            s = "Stats:\n"
            s += ("Attack: " + str(self.cur_plyr.get_stat("attack")) + "\n")
            s += ("Defense: " + str(self.cur_plyr.get_stat("defense")) + "\n")
            s += ("Magic: " + str(self.cur_plyr.get_stat("magic")) + "\n")
            s += ("Health: " + str(self.cur_plyr.get_stat("health")) + "\n")
            s += ("Resist: " + str(self.cur_plyr.get_stat("resist")) + "\n")
            self.plyr_stats = Text(s, 22, self.x+25, self.y+200, width=100)
            # update equipment
            self.plyr_eqp = []
            i=0
            # makes a grid, need to add header elements for each slot
            for itm in self.cur_plyr.equipment.values():
                self.plyr_eqp.append(ItemIcon(itm, self.x+(64*(i%4))+150, self.y+(100*(i//4))+15))
                i+=1
            # limited to 4 moves only at the moment, need to extend
            self.plyr_mv = []
            for i in range(0,4):
                if i < len(self.cur_plyr.moves):
                    self.plyr_mv.append(MoveIcon(self.cur_plyr.moves[i], self.x+(64*i)+15, self.y+200))
                else:
                    self.plyr_mv.append(MoveIcon(None, self.x+(64*i)+148, self.y+220))
            # update inventory
            self.plyr_inv = []
            i=0
            for itm in self.cur_plyr.inventory:
                self.plyr_eqp.append(ItemIcon(itm, self.x+(64*i)+148, self.y+300))
                i+=1
            # create new renderables list
            self.renderables = []
            self.renderables.append(self.win)
            self.renderables.append(self.plyr_img)
            self.renderables.append(self.plyr_name)
            self.renderables.append(self.plyr_stats)
            self.renderables.append(self.plyr_hlth)
            self.renderables.extend(self.plyr_eqp)
            self.renderables.extend(self.plyr_mv)


    def render(self, surface, game):
        # add conditions so that only renders outside of battles
        if game.selected_player:
            super().render(surface, game)