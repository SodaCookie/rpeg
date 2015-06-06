        # self.create_group("loot", (self.resolution[0]//2, 0))
        # self.create_group("shop", (self.resolution[0]//2, 10*GameMenu.SCALE),
        #     ImageCache.add("images/ui/shop_back.png", True),
        #     h_anchor=0, v_anchor=1)
        # self.create_group("monster", (6*GameMenu.SCALE, 10*GameMenu.SCALE))
        # self.create_group("battle_info", (6*GameMenu.SCALE, 5*GameMenu.SCALE),
        #     ImageCache.add("images/ui/battle_info.png", True),
        #     h_anchor=1, v_anchor=1)

    def render_shop(self, shop):
        # Clean up previous dialog if any
        if self.current_dialog is not Group.shop and\
                self.current_dialog is not None:
            return
        elif self.current_dialog is Group.shop:
            self.close_shop()
            return

        Group.shop.delete()
        button_position = (self.resolution[0]-7*GameMenu.SCALE,
                           (15+5)*GameMenu.SCALE)
        button_func = partial(self.render_shop, shop)

        if not self.single_renderables.get("shop"):
            self.single_renderables["shop"] = Button(button_position,
                on_pressed = button_func, t_info = self.option_style,
                b_info = self.option_button_style, text = "Shop")
            self.single_renderables["shop"].display()

        Group.shop.add(Text((0, 0), t_info=self.title_style, text=shop.name,
                             h_anchor=0))
        Group.shop.add(Button((0, 0*GameMenu.SCALE+Group.shop.back.height),
                             on_pressed=self.close_shop,
                             b_info=self.large_button_style,
                             t_info=self.title_style,
                             text="CLOSE",
                             h_anchor=0,
                             v_anchor=1,
                             text_h_anchor=0,
                             text_v_anchor=1))

        for i, pair in enumerate(shop.items):
            item, value = pair
            Group.shop.add(Dragable(
                (-73*GameMenu.SCALE, 4*GameMenu.SCALE+i*20*GameMenu.SCALE),
                filename="images/item/test_icon.png",
                alpha=True,
                h_anchor=1,
                v_anchor=1,
                on_released=self.move_item))
            Group.shop.add(Text(
                (-55*GameMenu.SCALE, 4*GameMenu.SCALE+i*20*GameMenu.SCALE),
                t_info=self.text_style,
                text=item.name))
            Group.shop.add(Text(
                (-55*GameMenu.SCALE, 8*GameMenu.SCALE+i*20*GameMenu.SCALE),
                t_info=self.text_style,
                text="Price: %d"%value,
                fontsize=18,
                fontcolor=(255, 255, 51)))