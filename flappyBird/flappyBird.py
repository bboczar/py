import bird
import pipes
import pygame
import sys


class Game:
    def __init__(self):
        self.setup_pygame()
        self.game_active = False
        self.score = 0
        self.high_score = 0
        self.bird = bird.Bird()
        self.pipes = pipes.Pipes()
        self.floor_x_pos = 0

    def setup_pygame(self):
        pygame.mixer.pre_init(buffer=512)
        pygame.init()
        self.SPAWNPIPE = pygame.USEREVENT
        self.BIRDFLAP = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWNPIPE, 1200)
        pygame.time.set_timer(self.BIRDFLAP, 200)
        self.screen = pygame.display.set_mode((576, 1024))
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.Font('04B_19.ttf', 40)
        self.bg_surface = pygame.image.load('assets/sprites/background-day.png').convert()
        self.bg_surface = pygame.transform.scale2x(self.bg_surface)
        self.floor_surface = pygame.image.load('assets/sprites/base.png').convert()
        self.floor_surface = pygame.transform.scale2x(self.floor_surface)
        self.game_over_surface = pygame.image.load('assets/sprites/message.png').convert_alpha()
        self.game_over_surface = pygame.transform.scale2x(self.game_over_surface)
        self.game_over_rect = self.game_over_surface.get_rect(center=(288, 512))

    def run(self):
        while True:
            self.handle_events()
            self.tick()
            self.draw()
            self.clock.tick(100)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bird.handle_input()
                    if not self.game_active:
                        self.reset()
            if event.type == self.SPAWNPIPE:
                self.pipes.create_pipe()
            if event.type == self.BIRDFLAP:
                self.bird.flap_wings()

    def tick(self):
        if self.game_active:
            self.bird.tick()
            self.game_active = not self.bird.colided(self.pipes.get_list())
            self.pipes.tick()
            self.score += self.pipes.scored()
        else:
            if self.score > self.high_score:
                self.high_score = self.score

        self.floor_x_pos -= 1
        if self.floor_x_pos <= -576:
            self.floor_x_pos = 0

    def draw(self):
        self.screen.blit(self.bg_surface, (0, 0))
        if self.game_active:
            self.bird.draw(self.screen)
            self.pipes.draw(self.screen)
        else:
            self.screen.blit(self.game_over_surface, self.game_over_rect)

        self.score_display()
        self.draw_floor()

        pygame.display.update()

    def reset(self):
        self.game_active = True
        self.bird.reset()
        self.pipes.reset()
        self.score = 0

    def draw_floor(self):
        self.screen.blit(self.floor_surface, (self.floor_x_pos, 900))
        self.screen.blit(self.floor_surface, (self.floor_x_pos + 576, 900))

    def score_display(self):
        score_surface = self.game_font.render(f'Score: {int(self.score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(110, 100))
        self.screen.blit(score_surface, score_rect)

        high_score_surface = self.game_font.render(f'High score: {int(self.high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(416, 100))
        self.screen.blit(high_score_surface, high_score_rect)


game = Game()
game.run()
