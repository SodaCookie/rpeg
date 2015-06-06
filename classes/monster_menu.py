        health = scale(ImageCache.add("images/ui/health.png"), (128, 8))
        speed = scale(ImageCache.add("images/ui/speed.png"), (128, 8))

        for i, monster in enumerate(self.current_battle.monsters):

            x = self.resolution[0]/4+(self.resolution[0]*3/4)/\
                len(self.current_battle.monsters)/2+\
                (self.resolution[0]*3/4)/len(self.current_battle.monsters)*i
            y = self.resolution[1]/3*2-GameMenu.SCALE*5

            Group.bars.add(Text(
                (round(x), round(y-monster.surface.get_height()*GameMenu.SCALE)-10*GameMenu.SCALE),
                t_info = self.text_style,
                fontsize = 18,
                h_anchor = 0,
                v_anchor = -1,
                text=monster.name))

            Group.bars.add(Image(
                (round(x-health.get_width()/2), round(y-monster.surface.get_height()*GameMenu.SCALE)-6*GameMenu.SCALE),
                width = round(health.get_width()*monster.current_health/
                    monster.health),
                h_anchor = 1,
                v_anchor = -1,
                surface = health,
                alpha = True))

            Group.bars.add(Image(
                (round(x-speed.get_width()/2), round(y-monster.surface.get_height()*GameMenu.SCALE)-2*GameMenu.SCALE),
                width = round(speed.get_width()*monster.action/
                    monster.action_max),
                h_anchor = 1,
                v_anchor = -1,
                surface = speed,
                alpha = True))

        for i, monster in enumerate(self.current_battle.monsters):
            x = self.resolution[0]/4+(self.resolution[0]*3/4)/\
                len(self.current_battle.monsters)/2+\
                (self.resolution[0]*3/4)/len(self.current_battle.monsters)*i
            y = self.resolution[1]/3*2-GameMenu.SCALE*5

            Group.monster.add(Image(
                (round(x), round(y)-GameMenu.SCALE),
                h_anchor = 0,
                v_anchor = -1,
                surface = scale(monster.surface,
                    (monster.surface.get_width()*GameMenu.SCALE,
                     monster.surface.get_height()*GameMenu.SCALE)),
                alpha = True))