import pygame

from engine.ui.core.manager import Manager
import engine.ui.element as element

class TravelManager(Manager):
    """Deals with the travel UI when moving through the Dungeon"""

    def __init__(self, x, y, width, height):
        """Travel manager handles the movement"""
        super().__init__("travel", x, y)
        self.width = width
        self.height = height
        self.path = []
        self.node_elements = []
        self.dungeon = None
        self.location = None

        # Window
        self.add_renderable(element.Frame("frame", x, y, width,
            height))

        # Lines
        surface = pygame.Surface((width - 16, height - 16), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        self.lines = element.Image("lines", x + 8, y + 8, surface)
        self.add_renderable(self.lines)

        # Nodes
        self.nodes = []

    def update(self, game, system):
        if self.dungeon != game.current_dungeon:
            self.path = []
            self.dungeon = game.current_dungeon
            self.update_dungeon()
        if self.location != game.current_location:
            self.path.append(game.current_location)
            self.location = game.current_location
            self.update_window()

    def update_dungeon(self):
        """Update dungeon"""
        for elem in self.node_elements:
            self.remove_renderable(elem.name)

        depth = self.dungeon.depth + 3

        for i, frame in enumerate(self.dungeon.frame):
            width = len(frame)+1
            for j, location in enumerate(frame):
                x = self.x + self.width // depth * (i + 1) - 10
                y = self.y + self.height // width * (j + 1) - 4
                render_node = element.TravelButton("node-%d-%d" % (i, j),
                    x, y, "unknown", location)
                self.node_elements.append((location, render_node))
                self.add_renderable(render_node)

    def update_window(self):
        """Update the window after a travel call"""
        depth = self.dungeon.depth + 3
        # previous
        if len(self.path) > 1:
            prev_head = self.path[-2]
            self._get_node_by_location(prev_head).set_ntype("visited")
            self._get_node_by_location(prev_head).disable = True
            for location in prev_head.get_neighbours():
                self._get_node_by_location(location).set_ntype("unknown")
                self._get_node_by_location(location).disable = True

        # head
        head = self.path[-1]
        self._get_node_by_location(head).visible = True
        self._get_node_by_location(head).disable = True
        self._get_node_by_location(head).set_ntype("current")
        for location in head.get_neighbours():
            node = self._get_node_by_location(location)
            node.visible = True
            node.set_ntype("unknown")

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

    def _get_node_by_location(self, location):
        """Helper function to return node by location"""
        for location2, node in self.node_elements:
            if location is location2:
                return node
        return None