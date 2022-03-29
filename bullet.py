import pygame 
from pygame.sprite import Sprite
#游戏里一切能感知时间流逝、具有坐标位置的，都是精灵。
class Bullet(Sprite):
    def __init__(self, ai_settings, screen, gun): 
        """在枪械所处的位置创建一个子弹对象""" 
        super(Bullet, self).__init__() #调用父类
        self.screen = screen
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = gun.rect.centerx
        self.rect.top = gun.rect.top
        #先创建子弹矩形，再设置正确位置
        self.y = float(self.rect.y)
        #储存子弹位置，小数表示
        self.color = ai_settings.bullet_color 
        self.speed_factor = ai_settings.bullet_speed_factor
    def update(self):
        self.y -= self.speed_factor#按子弹速度发出
        self.rect.y = self.y#更新自身位置
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)