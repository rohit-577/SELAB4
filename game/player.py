import pygame

SPEED = 4

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.vel_y = 0
        self.on_ground = False
        self.color = (60,160,220)
        self.standing_on = None

    def update(self, keys, platforms, width):
        dx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = SPEED
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = -13
            self.on_ground = False

        self.vel_y = min(self.vel_y + 0.55, 12)
        self.rect.x = max(0, min(width - self.rect.width, self.rect.x + dx))
        prev_bottom = self.rect.bottom
        self.rect.y += int(self.vel_y)
        self.on_ground = False
        self.standing_on = None
        for i, p in enumerate(platforms):
            # only land if we were above the platform last frame (one-way)
            if self.rect.colliderect(p) and self.vel_y > 0:
                if prev_bottom <= p.top + 10:
                    self.rect.bottom = p.top
                    self.vel_y = 0
                    self.on_ground = True
                    self.standing_on = i
                    break

    def draw(self, screen, cam_y):
        dr = self.rect.move(0, -int(cam_y))
        pygame.draw.rect(screen, self.color, dr, border_radius=6)
        pygame.draw.circle(screen,(255,220,180),(dr.centerx, dr.top+8),7)
