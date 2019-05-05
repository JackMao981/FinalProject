#testing if sounds work in bare minimum case
import pygame
import time

#from scikits.audiolab.pysndfile.matapi import oggread

pygame.init()
pygame.mixer.init(frequency=48000)


#size = 300, 500
#screen = pygame.display.set_mode(size)

time.sleep(1)

hit_sound = pygame.mixer.Sound("Sounds/checkpoint.wav")
hit_sound.play()

time.sleep(1)

pygame.mixer.quit()
