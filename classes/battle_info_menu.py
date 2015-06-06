    def render_battle_info(self):
        Group.battle_info.delete()

        if self.current_battle and self.current_char:
            abilities = ImageCache.add("images/ui/abilities.png", True)
            abilities = scale(abilities, (abilities.get_width()*GameMenu.SCALE,
                abilities.get_height()*GameMenu.SCALE))
            portrait = ImageCache.add(self.current_char.portrait, True)
            portrait = scale(portrait, (portrait.get_width()*GameMenu.SCALE,
                portrait.get_height()*GameMenu.SCALE))

            Group.battle_info.add(Image((37*GameMenu.SCALE, 0),
                surface = portrait,
                h_anchor = 1,
                v_anchor = 1))

            Group.battle_info.add(Image((0, 0),
                surface = abilities,
                alpha = True,
                h_anchor = 1,
                v_anchor = 1))

            Group.battle_info.add(Text((3*GameMenu.SCALE, GameMenu.SCALE),
                         t_info = self.title_style,
                         v_anchor = 1,
                         text = self.current_char.name))

            Group.battle_info.add(Text((3*GameMenu.SCALE, 50*GameMenu.SCALE),
                         t_info = self.title_style,
                         v_anchor = 1,
                         text = "Skills"))

            for i, move in enumerate(self.current_char.moves):
                if isinstance(self.current_char, player.Player):
                    img = ImageCache.add(move.surface)
                    h_img = img.copy()
                    pygame.draw.rect(h_img, ((255, 255, 0)), h_img.get_rect(), 1)
                    p_img = img.copy()
                    pygame.draw.rect(h_img, (0, 128, 0), h_img.get_rect(), 1)
                    d_img = img.copy()
                    d_img.set_alpha(100)
                    enable = True if self.current_char.ready else False

                    Group.battle_info.add(Button(
                        (4*GameMenu.SCALE+i%3*20*GameMenu.SCALE,
                            60*GameMenu.SCALE+i//3*20*GameMenu.SCALE),
                        enabled = enable,
                        h_anchor = 1,
                        v_anchor = 1,
                        img = scale(img, (64, 64)),
                        hovered_img = scale(h_img, (64, 64)),
                        pressed_img = scale(p_img, (64, 64)),
                        disabled_img = scale(d_img, (64, 64)),
                        hover_img = scale(ImageCache.add(move.surface), (64, 64))))

        Group.battle_info.display()


        if self.current_char:
            Group.bars.add(Image((4*GameMenu.SCALE, 11*GameMenu.SCALE),
                surface = health,
                width = round(health.get_width()*
                    self.current_char.current_health/
                    self.current_char.health),
                h_anchor = 1,
                v_anchor = 1))

            Group.bars.add(Text((4*GameMenu.SCALE, 13*GameMenu.SCALE+2),
                         t_info = self.text_style,
                         v_anchor = 1,
                         text = "Health: %d/%d" % (self.current_char.get_cur_health(), self.current_char.get_max_health())))

            Group.bars.add(Image((4*GameMenu.SCALE, 19*GameMenu.SCALE),
                surface = speed,
                width = round(speed.get_width()*self.current_char.action/
                    self.current_char.action_max),
                h_anchor = 1,
                v_anchor = 1))

            Group.bars.add(Text((4*GameMenu.SCALE, 21*GameMenu.SCALE+2),
                         t_info = self.text_style,
                         v_anchor = 1,
                         text = "Action: %d/%d" % (self.current_char.action, self.current_char.action_max)))