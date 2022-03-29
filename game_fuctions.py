import sys
import pygame
from bullet import Bullet
from QWD import QWD
from gun import Gun
from time import sleep
from game_stats import GameStats
def check_events(ai_settings, screen,stats,sb, play_button,gun,qwds,bullets):
    for event in pygame.event.get():#监测事件
            if event.type == pygame.QUIT:
                sys.exit()#退出游戏
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_play_button(ai_settings, screen, stats,sb, play_button, gun, qwds, bullets, mouse_x, mouse_y)
            elif event.type==pygame.KEYDOWN:
                check_keydown_events(event, ai_settings, screen, gun, bullets)
            elif event.type==pygame.KEYUP:
                check_keyup_events(event, gun)
def check_keydown_events(event, ai_settings, screen, gun, bullets):#响应按键，保证按下后连续移动
    if event.key==pygame.K_RIGHT:
        gun.moving_right=True
    if event.key==pygame.K_LEFT:
        gun.moving_left=True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, gun, bullets)
    elif event.key == pygame.K_q: 
        sys.exit()
def check_keyup_events(event, gun):#检测按键松开
    if event.key==pygame.K_RIGHT:
        gun.moving_right=False
    elif event.key == pygame.K_LEFT: 
        gun.moving_left = False
def update_screen(ai_settings,screen,stats,sb,gun,bullets,qwds,play_button):
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites(): 
        bullet.draw_bullet()
    gun.blitme()
    qwds.draw(screen)
    sb.show_score()
    if not stats.game_active: 
        play_button.draw_button()
    pygame.display.flip()
def update_bullets(ai_settings, screen,stats, sb, gun,qwds,bullets):
    bullets.update()
    for bullet in bullets.copy():#遍历bullets编组的副本
        if bullet.rect.bottom<=0:
            bullets.remove(bullet)
    check_bullet_qwd_collisions(ai_settings, screen,stats, sb, gun,qwds, bullets)
def fire_bullet(ai_settings, screen, gun, bullets):
    if len(bullets) < ai_settings.bullets_allowed: 
        # 创建一颗子弹，并将其加入到编组bullets中 
        new_bullet = Bullet(ai_settings, screen, gun) 
        bullets.add(new_bullet)
def get_number_qwds_x(ai_settings, qwd_width):
    available_space_x = ai_settings.screen_width - 2 * qwd_width
    number_qwds_x = int(available_space_x / (2 * qwd_width))#隔一个生成
    return number_qwds_x
def get_number_rows(ai_settings, gun_height, qwd_height):
    available_space_y = (ai_settings.screen_height - (3 * qwd_height) - gun_height)
    number_rows = int(available_space_y / (2 * qwd_height))
    return number_rows
def create_qwd(ai_settings, screen, qwds, qwd_number,row_number):
    qwd=QWD(ai_settings,screen)
    qwd_width = qwd.rect.width
    qwd.x = qwd_width + 2 * qwd_width * qwd_number
    qwd.rect.x=qwd.x
    qwd.rect.y = qwd.rect.height + 2 * qwd.rect.height * row_number
    qwds.add(qwd)
def create_fleet(ai_settings, screen,gun,qwds):
    qwd=QWD(ai_settings,screen)
    number_qwds_x = get_number_qwds_x(ai_settings, qwd.rect.width)
    number_rows = get_number_rows(ai_settings, gun.rect.height, qwd.rect.height)
    for row_number in range(number_rows):
        for qwd_number in range(number_qwds_x):
            create_qwd(ai_settings, screen, qwds, qwd_number, row_number)
def update_qwds(ai_settings, screen, stats, sb, gun, qwds, bullets):
    check_fleet_edges(ai_settings,gun,qwds)
    qwds.update()
    if pygame.sprite.spritecollideany(gun, qwds): 
        gun_hit(ai_settings, screen, stats, sb, gun, qwds, bullets)
    check_qwds_bottom(ai_settings,  screen,stats,sb, gun, qwds, bullets)
def check_fleet_edges(ai_settings,gun,qwds):
    for qwd in qwds.sprites():
        if qwd.check_edges():
            change_fleet_direction(ai_settings, qwds) 
            break
def change_fleet_direction(ai_settings,qwds):
    for qwd in qwds.sprites():
        qwd.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
def check_bullet_qwd_collisions(ai_settings, screen,stats,sb, gun,qwds, bullets):
    collisions = pygame.sprite.groupcollide(bullets, qwds, True, True)
    if collisions: 
        for qwds in collisions.values(): 
            stats.score += ai_settings.qwd_points * len(qwds)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(qwds) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, gun, qwds)
def gun_hit(ai_settings, screen,stats,sb ,gun, qwds, bullets):
    if stats.guns_left > 0:
        stats.guns_left -= 1#减一命
        sb.prep_guns()
        qwds.empty() 
        bullets.empty()#清空
        create_fleet(ai_settings, screen, gun, qwds) 
        gun.center_gun()#重开
        sleep(0.5)#暂停
    else: 
        stats.game_active = False
        pygame.mouse.set_visible(True)
def check_qwds_bottom(ai_settings,  screen,stats,sb, gun, qwds, bullets):
    screen_rect = screen.get_rect()
    for qwd in qwds.sprites():
       if qwd.rect.bottom >= screen_rect.bottom: 
            gun_hit(ai_settings,  screen,stats,sb, gun, qwds, bullets) 
            break
def check_play_button(ai_settings, screen,stats,sb, play_button,gun,qwds,bullets,mouse_x, mouse_y): 
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)#隐藏光标
        stats.reset_stats()#重置游戏统计信息
        stats.game_active = True
        sb.prep_score() 
        sb.prep_high_score() 
        sb.prep_level()#重置记分牌图像
        sb.prep_guns()
        qwds.empty() 
        bullets.empty()#清空列表
        create_fleet(ai_settings, screen, gun, qwds) 
        gun.center_gun()
def check_high_score(stats, sb): 
    """检查是否诞生了新的最高得分""" 
    if stats.score > stats.high_score: 
        stats.high_score = stats.score 
        sb.prep_high_score()