from functools import partial

import pygame

from engine.ui.core.manager import Manager
from engine.ui.core.zone import Zone
import engine.ui.element as element

class TravelManager(Manager):

    def __init__(self, width, height, x, y):
        super(TravelManager, self).__init__()
        # cur_dungeon given by game manager, not built yet
        self.path = []
        self.dungeon = None
        self.location = None
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Window
        self.window = element.Window(width, height, x, y)
        self.renderables.append(self.window)
        # Lines
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        self.lines = element.Image(surface, x+4, y+4)
        self.renderables.append(self.lines)
        # Nodes
        self.nodes = []
        # Close Button
        self.close = element.Button("CLOSE", 32, 0, y+height+16, True)
        self.close.x = x+width//2-self.close.surface.get_width()//2
        self.close_zone = Zone(((x+width//2-self.close.surface.get_width()//2,
            y+height+16), self.close.surface.get_size()))
        self.close.bind(self.close_zone)
        self.zones.append(self.close_zone)
        self.renderables.append(self.close)

    def update(self, game):
        if self.dungeon != game.current_dungeon:
            self.path = []
            self.dungeon = game.current_dungeon
        if self.location != game.current_location:
            self.path.append(game.current_location)
            self.location = game.current_location
            self.update_window(self.path)

        super().update(game)

    def update_window(self, path):
        depth = self.dungeon.depth+3

        self.renderables = []
        self.renderables.append(self.window)
        self.renderables.append(self.lines)
        self.renderables.append(self.close)

        self.zones = []
        self.zones.append(self.close_zone)

        all_potential_nodes = set()
        for node in self.path:
            all_potential_nodes.add(node)
            all_potential_nodes |= set(node.get_neighbours())
        for i, frame in enumerate(self.dungeon.frame): # Redundant code
            width = len(frame)+1
            for j, node in enumerate(frame):
                if node in self.path[:-1]:
                    render_node = element.TravelNode("visited",
                        self.x+self.width//depth*(i+1)-10, self.y+\
                        self.height//width*(j+1)-10)
                elif node is self.path[-1]:
                    render_node = element.TravelNode("visited",
                        self.x+self.width//depth*(i+1)-10, self.y+\
                        self.height//width*(j+1)-10, True)
                elif node in self.path[-1].get_neighbours():
                    render_node = element.TravelNode("unknown",
                        self.x+self.width//depth*(i+1)-10, self.y+\
                        self.height//width*(j+1)-10, True)
                    on_click = partial(self.on_click, node)
                    zone = Zone(((self.x+self.width//depth*(i+1)-10, self.y+\
                        self.height//width*(j+1)-10),render_node.surface.get_size()), on_click)
                    render_node.bind(zone)
                    self.zones.append(zone)
                elif node in all_potential_nodes:
                    render_node = element.TravelNode("unknown",
                        self.x+self.width//depth*(i+1)-10, self.y+\
                        self.height//width*(j+1)-10)
                self.renderables.append(render_node)


        surface = self.lines.surface
        for i, node in enumerate(self.path):
            frame = self.dungeon.frame[i+1]
            width = len(frame)+1
            min_index = min(self.dungeon.frame[i+1].index(n) for n in node.get_neighbours())
            max_index = max(self.dungeon.frame[i+1].index(n) for n in node.get_neighbours())

            left = (self.width//depth*(i+1), self.height//(len(self.dungeon.frame[i])+1)*(self.dungeon.frame[i].index(node)+1))
            right = (self.width//depth*(i+1)+self.width//depth//2, self.height//(len(self.dungeon.frame[i])+1)*(self.dungeon.frame[i].index(node)+1))
            pygame.draw.line(surface, (255, 255, 255), left, right, 3)

            min_y = min((self.height//(len(self.dungeon.frame[i])+1)*(self.dungeon.frame[i].index(node)+1), self.height//width*(min_index+1)))
            max_y = max((self.height//(len(self.dungeon.frame[i])+1)*(self.dungeon.frame[i].index(node)+1), self.height//width*(max_index+1)))

            top = (self.width//depth*(i+1)-10+self.width//depth//2+10, min_y)
            bottom = (self.width//depth*(i+1)-10+self.width//depth//2+10, max_y)
            pygame.draw.line(surface, (255, 255, 255), top, bottom, 3)

            for neighbour in node.get_neighbours():
                left = (self.width//depth*(i+1)+self.width//depth//2, self.height//width*(frame.index(neighbour)+1))
                right = (self.width//depth*(i+2), self.height//width*(frame.index(neighbour)+1))
                pygame.draw.line(surface, (255, 255, 255), left, right, 3)

    @staticmethod
    def on_click(location, game):
        game.current_location = location