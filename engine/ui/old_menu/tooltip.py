import engine.ui.core.renderable as Renderable
import engine.ui.core.bindable as Bindable

class Tooltip(Renderable):
    """Tooltips are surfaces that are rendered only when their zones are hovered over"""

    def ___init__(self, surface, zone):
        super().__init__()
