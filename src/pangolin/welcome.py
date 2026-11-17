from .art import ArtButton, ArtCanvas


class WelcomePage(ArtCanvas):
    def __init__(self):
        super().__init__('welcome.png')
        self.setupButton = ArtButton('Set Up', 'setup_button.png', self, click_effect=False)

    def layoutArt(self):
        self.place(self.setupButton, (263, 704, 696, 188))
