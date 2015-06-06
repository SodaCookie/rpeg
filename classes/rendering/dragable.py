import pygame

from classes.controller import MouseController
from classes.rendering.image import Image

class Dragable(Image, MouseController):

  NEUTRAL = 0
  HOVERED = 1
  PRESSED = 2
  DISABLED = 3

  def __init__(self, pos,
               width=None,
               height=None,
               h_anchor=0,
               v_anchor=0,
               surface=None,
               filename="",
               alpha=False,
               on_released=None):
      Image.__init__(self, pos, width, height, h_anchor,
                     v_anchor, surface, filename, alpha)
      MouseController.__init__(self)
      self.on_released = on_released
      self.mouse_x_offset = 0
      self.mouse_y_offset = 0
      self.state = Dragable.NEUTRAL

  def mouse_button_down(self, drag, pos):
      if not self.visible:
        return

      if self.state == Dragable.DISABLED:
          return

      if self.state == Dragable.HOVERED:
          self.state = Dragable.PRESSED
          self.mouse_x_offset = self.pos[0] - pygame.mouse.get_pos()[0]
          self.mouse_y_offset = self.pos[1] - pygame.mouse.get_pos()[1]

  def mouse_button_up(self, drag, pos):
      if not self.visible:
        return

      if self.state == Dragable.DISABLED:
          return

      if self.state == Dragable.PRESSED:
          self.state = Dragable.HOVERED
          if self.on_released:
            self.on_released(self)

  def mouse_motion(self, buttons, pos, rel):
      if not self.visible:
        return

      if self.state == Dragable.DISABLED:
          return

      if self.h_anchor < 0:
          x_offset = self.width / 2
      elif self.h_anchor > 0:
          x_offset = -self.width / 2
      else:
          x_offset = 0

      if self.v_anchor < 0:
          y_offset = self.height / 2
      elif self.v_anchor > 0:
          y_offset = -self.height / 2
      else:
          y_offset = 0

      if self.pos[0] - self.width / 2 <= pos[0] + x_offset <= self.pos[0] + self.width / 2 and\
         self.pos[1] - self.height / 2 <= pos[1] + y_offset <= self.pos[1] + self.height / 2:
          if self.state == Dragable.NEUTRAL:
              self.state = Dragable.HOVERED
      else:
          if self.state == Dragable.HOVERED:
              self.state = Dragable.NEUTRAL

      if self.state == Dragable.PRESSED:
          x, y = pygame.mouse.get_pos()
          self.pos = x + self.mouse_x_offset, y + self.mouse_y_offset