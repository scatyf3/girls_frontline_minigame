import sys#用于退出游戏
import pygame
from pygame.sprite import Group
#导入已有现成模块
from settings import Settings
from game_stats import GameStats
from gun import Gun
import game_fuctions as gf
from QWD import QWD
from button import Button
from scoreboard import Scoreboard
#与其他附属模块建立关系
def run_game():
    pygame.init()
    ai_settings=Settings()#为类创建实例，直接从settings文件取得数据
    screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption('极简版少女前线')
    play_button = Button(ai_settings, screen, "Play")
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    gun=Gun(ai_settings,screen)#调用速度
    bullets = Group()
    qwds = Group()
    qwd=QWD(ai_settings, screen)
    gf.create_fleet(ai_settings,screen, gun,qwds)
    while True:
        gf.check_events(ai_settings, screen,stats,sb, play_button, gun,qwds,bullets)
        if stats.game_active:
            gun.update()
            gf.update_bullets(ai_settings, screen,stats, sb, gun,qwds,bullets)
            gf.update_qwds(ai_settings, screen,stats, sb,gun, qwds, bullets)
        gf.update_screen(ai_settings,screen,stats,sb,gun,bullets,qwds,play_button)        
run_game()