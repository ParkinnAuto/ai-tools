import pygame

# Load sound whtn the program starts
class AlertPlayer:
    def __init__(self, sound_path:str):
        # Start pygame mixer for playing sound
        pygame.mixer.init()

        # Load sound file
        self.sound = pygame.mixer.Sound(sound_path)
    
    # Play alert sound
    def play(self):
        self.sound.play()
