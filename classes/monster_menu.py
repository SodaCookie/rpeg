from pygame.transform import scale
from pygame import Surface, SRCALPHA

from classes import controller
from classes.rendering.menu import Menu
from classes.rendering.button import Button, ButtonInfo
from classes.rendering.image import Image
from classes.rendering.text import Text, TextInfo
from classes.image_cache import ImageCache
import classes.rendering.view as view

class MonsterRenderInfo(object):

    def __init__(self, monster):
        self.monster = monster
        self.health = None
        self.speed = None
        self.highlight = False
        self.display = True


class MonsterImage(Image):

    def __init__(self, pos, monster, width=None, height=None, h_anchor=0, v_anchor=0, filename="", alpha=False):
        super().__init__(pos, width, height, h_anchor, v_anchor, monster.surface, filename, alpha)
        self.render_hover = False
        self.monster = monster

    def draw(self, screen):
        if self.render_hover:
            self.img = self.monster.hover_surface
        else:
            self.img = self.monster.surface
        super().draw(screen)


class MonsterMenu(Menu, controller.MouseController, controller.BattleController):

    def __init__(self, game, render_info):
        Menu.__init__(self, "monster", (0, 0), game, render_info)
        controller.MouseController.__init__(self)
        controller.BattleController.__init__(self)

        self.health = scale(ImageCache.add("images/ui/health.png"), (128, 8))
        self.speed = scale(ImageCache.add("images/ui/speed.png"), (128, 8))
        self.text_style = TextInfo(fontcolor=(255,255,255),
                                   fontsize=16,
                                   alignment=-1,
                                   h_anchor=1,
                                   v_anchor=1,
                                   wrap=True,
                                   width=149*view.SCALE)

        self.monster_infos = []
        self.rendering_monsters = [] # for convenience

    def delete(self):
        Menu.delete(self)
        controller.MouseController.delete()
        controller.BattleController.delete()

    def handle_start_battle(self):
        assert self.game.monsters, "No monsters were made during battlestart"
        assert self.game.battle, "No battle was made during battlestart"

        self.monster_infos = [MonsterRenderInfo(m) for m in self.game.monsters]
        self.render()

    def handle_end_battle(self):
        pass

    def mouse_motion(self, buttons, pos, rel):
        for m in self.rendering_monsters:
            monster_pos = view.get_abs_pos(m)
            width, height = m.width, m.height
            if monster_pos[0]-width//2 <= pos[0] <= monster_pos[0]+width//2 \
                    and monster_pos[1]-height <= pos[1] <= monster_pos[1]:
                self.game.hover_character = m.monster
                break

    def draw_before(self, screen):
        if not self.render_info.display_monster:
            self.hide()
            return Menu.BREAK
        self.show()

        for monster, info in zip(self.game.monsters, self.monster_infos):
            info.health.width = round(self.health.get_width()*\
                monster.current_health/monster.health)
            info.speed.width = round(self.speed.get_width()*monster.action/
                monster.action_max)

        self.dehighlight_all()
        # Monster highlighting
        if self.game.current_move and self.game.hover_character in \
                [m.monster for m in self.rendering_monsters]:
            if self.game.current_move.cast_type in ["single"]:
                self.highlight_monster(self.game.hover_character)
            elif self.game.current_move.cast_type in ["group"]:
                self.highlight_all()
            else: # Defaults to one
                self.highlight_monster(self.game.hover_character)

    def dehighlight_all(self):
        for m in self.rendering_monsters:
            m.render_hover = False

    def highlight_monster(self, monster):
        for m in self.rendering_monsters:
            if m.monster == monster:
                m.render_hover = True
                break

    def highlight_all(self):
        for m in self.rendering_monsters:
            m.render_hover = True

    def render(self):
        self.clear()

        self.rendering_monsters = []
        for i, monster in enumerate(self.game.monsters):
            x = view.get_resolution()[0]/4+(view.get_resolution()[0]*3/4)/\
                len(self.game.monsters)/2+\
                (view.get_resolution()[0]*3/4)/len(self.game.monsters)*i
            y = view.get_resolution()[1]/4*3-view.SCALE*5

            self.monster_infos[i].health = self.add(Image(
                (round(x-self.health.get_width()/2), round(y-monster.surface.get_height())-6*view.SCALE),
                width = round(self.health.get_width()*monster.current_health/
                    monster.health),
                h_anchor = 1,
                v_anchor = -1,
                surface = self.health,
                alpha = True))

            self.monster_infos[i].speed = self.add(Image(
                (round(x-self.speed.get_width()/2), round(y-monster.surface.get_height())-2*view.SCALE),
                width = round(self.speed.get_width()*monster.action/
                    monster.action_max),
                h_anchor = 1,
                v_anchor = -1,
                surface = self.speed,
                alpha = True))

            self.add(Text(
                (round(x), round(y-monster.surface.get_height())-10*view.SCALE),
                t_info = self.text_style,
                fontsize = 18,
                h_anchor = 0,
                v_anchor = -1,
                text=monster.name))

            self.rendering_monsters.append(self.add(MonsterImage(
                (round(x), round(y)-view.SCALE),
                monster = monster,
                h_anchor = 0,
                v_anchor = -1,
                alpha = True)))