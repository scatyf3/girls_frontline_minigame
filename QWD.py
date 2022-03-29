import pygame 
from pygame.sprite import Sprite
class QWD(Sprite):
    def __init__(self, ai_settings, screen):  
        super(QWD, self).__init__() 
        self.screen = screen 
        self.ai_settings = ai_settings
        # 加载图像，并设置其rect属性 
        self.image = pygame.image.load('Pic_Manticore_LL.bmp')
        self.image = pygame.transform.scale(self.image,(60,60)) 
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width 
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
    def blitme(self): 
        self.screen.blit(self.image, self.rect)
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        #如果qwd位于屏幕边缘，就返回true
    def update(self):
        self.x += (self.ai_settings.qwd_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
   