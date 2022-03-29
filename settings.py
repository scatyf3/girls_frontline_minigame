class Settings():#用类建立基本设置
    def __init__(self):
        self.screen_width=1200
        self.screen_height=800
        self.bg_color=(230,230,230)
        self.gun_speed_factor = 1.5
        #控制游戏外观和枪械速度
        self.bullet_width = 3 
        self.bullet_height = 15 
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3#允许最大子弹数
        self.fleet_drop_speed = 10
        self.gun_limit = 3
        self.speedup_scale = 1.1 
        self.score_scale = 1.5
        self.initialize_dynamic_settings() 
    def initialize_dynamic_settings(self): 
        """初始化随游戏进行而变化的设置""" 
        self.gun_speed_factor = 1.5 
        self.bullet_speed_factor = 3 
        self.qwd_speed_factor = 1 
        # fleet_direction为1表示向右；为-1表示向左 
        self.fleet_direction = 1
        self.qwd_points = 50
    def increase_speed(self):
        self.gun_speed_factor *= self.speedup_scale 
        self.bullet_speed_factor *= self.speedup_scale 
        self.qwd_speed_factor *= self.speedup_scale
        self.qwd_points = int(self.qwd_points * self.score_scale)