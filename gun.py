import pygame
from pygame.sprite import Sprite
class Gun(Sprite):
    def __init__(self,ai_settings,screen):
        super(Gun, self).__init__()
        self.screen=screen
        self.ai_settings = ai_settings
        self.image=pygame.image.load("gun.bmp")#加载图像
        self.image = pygame.transform.scale(self.image,(30,30)) 
        self.rect=self.image.get_rect()#将图像视作矩形处理
        self.screen_rect=screen.get_rect()
        self.rect.centerx=self.screen_rect.centerx
        self.rect.bottom=self.screen_rect.bottom#将飞船放置于底部中央
        self.center = float(self.rect.centerx)# 在飞船的属性center中存储小数值
        self.moving_right=False
        self.moving_left=False
    def blitme(self):
        self.screen.blit(self.image, self.rect)
    def update(self):#保证连续按键可以连续移动
        if self.moving_right and self.rect.right < self.screen_rect.right:#保证移动不超出屏幕
            self.center += self.ai_settings.gun_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.gun_speed_factor
        self.rect.centerx = self.center
    def center_gun(self):
        self.center = self.screen_rect.centerx

    
'''
属性初始化Python中 __init__的通俗解释是什么？ - 追远·J的回答 - 知乎
https://www.zhihu.com/question/46973549/answer/767530541
'''