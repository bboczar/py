import pygame
import random


class Pipes:
    def __init__(self):
        self.pipe_height = [400, 600, 800]
        self.pipe_list = []
        self.movement_rate = 5
        self.validity_limit = -50
        self.spawn_location = 700
        self.gap = 300
        self.score_bounds = (95, 105)
        self.can_score = True
        self.init_graphics()

    def init_graphics(self):
        self.pipe_surface = pygame.image.load('assets/sprites/pipe-green.png').convert()
        self.pipe_surface = pygame.transform.scale2x(self.pipe_surface)

    def reset(self):
        self.pipe_list.clear()
        self.can_score = True

    def create_pipe(self):
        random_pipe_pos = random.choice(self.pipe_height)
        bottom_pipe = self.pipe_surface.get_rect(midtop=(self.spawn_location, random_pipe_pos))
        top_pipe = self.pipe_surface.get_rect(midbottom=(self.spawn_location, random_pipe_pos - self.gap))
        self.pipe_list.append(bottom_pipe)
        self.pipe_list.append(top_pipe)

    def tick(self):
        for pipe in self.pipe_list:
            pipe.centerx -= self.movement_rate
        self.pipe_list = [pipe for pipe in self.pipe_list if pipe.right > self.validity_limit]

    def draw(self, screen):
        for pipe in self.pipe_list:
            if pipe.bottom >= 1024:
                screen.blit(self.pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
                screen.blit(flip_pipe, pipe)

    def scored(self):
        score = 0
        for pipe in self.pipe_list:
            if self.score_bounds[0] < pipe.centerx < self.score_bounds[1] and self.can_score:
                self.can_score = False
                score = 1
            if pipe.centerx < 0:
                self.can_score = True

        return score

    def get_list(self):
        return self.pipe_list
