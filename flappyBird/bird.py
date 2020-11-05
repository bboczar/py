import pygame


class Bird:
    def __init__(self):
        self.bird_movement = 0
        self.gravity = 0.25
        self.zero_position = (100, 512)
        self.upper_boundary = -50
        self.lower_boundary = 900
        self.flap_power = -8
        self.init_graphics()
        self.init_sounds()


    def init_graphics(self):
        self.bird_downflap = pygame.transform.scale2x(
            pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha())
        self.bird_midflap = pygame.transform.scale2x(
            pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha())
        self.bird_upflap = pygame.transform.scale2x(
            pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha())
        self.bird_frames = [self.bird_downflap, self.bird_midflap, self.bird_upflap, self.bird_midflap]
        self.bird_index = 0
        self.bird_surface = self.bird_frames[self.bird_index]
        self.rotated_bird_surface = self.bird_frames[self.bird_index]
        self.bird_rect = self.bird_surface.get_rect(center=self.zero_position)

    def init_sounds(self):
        self.flap_sound = pygame.mixer.Sound('assets/audio/wing.ogg')
        self.death_sound = pygame.mixer.Sound('assets/audio/hit.ogg')

    def tick(self):
        self.bird_movement += self.gravity
        self.bird_rect.centery += self.bird_movement

    def draw(self, screen):
        self.rotate_bird()
        screen.blit(self.rotated_bird_surface, self.bird_rect)

    def handle_input(self):
        self.bird_movement = self.flap_power
        self.flap_sound.play()

    def colided(self, pipes):
        for pipe in pipes:
            if self.bird_rect.colliderect(pipe):
                self.death_sound.play()
                return True
        if self.bird_rect.top <= self.upper_boundary or self.bird_rect.bottom >= self.lower_boundary:
            self.death_sound.play()
            return True
        return False

    def reset(self):
        self.bird_rect.center = self.zero_position
        self.bird_movement = 0

    def rotate_bird(self):
        self.rotated_bird_surface = pygame.transform.rotate(self.bird_surface, self.bird_movement * -3)

    def flap_wings(self):
        self.bird_surface = self.bird_frames[self.bird_index]
        self.bird_rect = self.bird_surface.get_rect(center=(self.zero_position[0], self.bird_rect.centery))
        self.bird_index += 1
        self.bird_index %= len(self.bird_frames)
