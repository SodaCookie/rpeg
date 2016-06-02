from engine.system import System, Message

from pygame import mixer


class SoundSystem(System):
    """SystemSystem class responsible for dispatching audio.
    Message types:
    play - non-force play a sound
    force - force play a sound
    ui - reserved channel for playing ui sounds
    bg - Sets the background music"""

    def __init__(self, game):
        super().__init__(game, "sound")

    def init(self, game):
        mixer.init()
        mixer.set_num_channels(8)
        mixer.set_reserved(2)
        self.ui_channel = mixer.Channel(0)
        self.bg_channel = mixer.Channel(1)

    def update(self, delta, game):
        messages = self.flush_messages()
        for message in messages:
            self.dispatch(message)

    def dispatch(self, message):
        """Function for determining what action to call depending on the
        message"""
        sound = message.args[0]
        if message.mtype == "play":
            self.play_sound(sound)
        elif message.mtype == "force":
            self.force_sound(sound)
        elif message.mtype == "ui":
            self.play_ui(sound)
        elif message.mtype == "bg":
            self.set_bg(sound)

    def play_sound(self, sound):
        """Non forcefully play a sound"""
        channel = mixer.find_channel()
        if channel is not None:
            channel.play(sound)

    def force_sound(self, sound):
        """Forcefully play a sound"""
        channel = mixer.find_channel(force=True)
        if channel is not None:
            channel.play(sound)

    def play_ui(self, sound):
        """Add sound to the ui queue"""
        self.ui_channel.play(sound)

    def set_bg(self, sound):
        """Set music of background queue"""
        self.bg_channel.play(sound, loops=-1)