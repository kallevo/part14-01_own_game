# Complete your game here
import pygame
import random

class DodgeMonster:
    def __init__(self) -> None:
        ##Load images and game window
        pygame.init()
        self.window = pygame.display.set_mode((640, 480))
        self.robot = pygame.image.load("robot.png")
        self.monster = pygame.image.load("monster.png")
        self.coin = pygame.image.load("coin.png")

        ##Defining robot start position and setting max values for height and width
        self.max_height = 480
        self.max_width = 640
        self.robot_x = 10
        self.robot_y = (self.max_height / 2) - self.robot.get_height() / 2

        ##Defining monsters start position and starting game
        self.monster_x = self.max_width + self.monster.get_width()
        self.monster_y = random.randint(0, self.max_height - self.monster.get_height())
        
        ##Defining coins start x and y position
        self.coin_x = 10
        self.coin_y = self.monster_y
        self.coin_collected = False
        self.coin_storage = 0

        pygame.display.set_caption("Dodge monster")
        self.to_up = False
        self.to_down = False
        self.end = False
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.SysFont("Arial", 24)
        self.main_loop()

    def render_window(self):
        
        self.window.fill((0, 0, 200))

        ##Render robot
        self.window.blit(self.robot, (self.robot_x, self.robot_y))
        ##Render monster
        self.window.blit(self.monster, (self.monster_x, self.monster_y))
        ##Render coin if not collected
        if self.coin_collected == False:
            self.window.blit(self.coin, (self.coin_x, self.coin_y))
        ##Render current round in top left corner
        round_text = self.game_font.render("Coin storage: " + str(self.coin_storage), True, (255, 0, 0))
        self.window.blit(round_text, (0, 0))

        if self.end:
            end_font = pygame.font.SysFont("Arial", 24, True)
            end_text = end_font.render(f"The end. Coins collected: {self.coin_storage}", True, (255, 0, 0))
            self.window.blit(end_text, (((self.max_width / 2) - (end_text.get_width() / 2), (self.max_height / 2) - (end_text.get_height() / 2))))

        pygame.display.flip()
        

    def move_robot(self, amount: int):
        self.robot_y += amount
        ##Dont move robot if it is going over borders
        if self.robot_y + amount <= 0 or self.robot_y >= self.max_height - self.robot.get_height():
            self.robot_y -= amount
        self.render_window()

    def move_monster(self, amount: int):
        ##Spawn next monster and set the coin to same y position as the new monster
        if self.monster_x < 0 - self.monster.get_width():
            self.monster_x = self.max_width + self.monster.get_width()
            self.monster_y = random.randint(0, self.max_height - self.monster.get_height())
            self.coin_y = self.monster_y
            self.coin_collected = False

        self.monster_x += amount

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            ##Move robot when pressing arrow keys up or down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.to_up = True
                if event.key == pygame.K_DOWN:
                    self.to_down = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.to_up = False
                if event.key == pygame.K_DOWN:
                    self.to_down = False

        if self.to_up:
            self.move_robot(-7)

        if self.to_down:
            self.move_robot(7)

    ##Returns true if monster is collisioning with robot
    def check_for_collision(self) -> bool:
        return self.monster_x <= self.robot_x + self.robot.get_width() and self.monster_x + self.monster.get_width() >= self.robot_x and self.monster_y <= self.robot_y + self.robot.get_height() and self.monster_y + self.monster.get_width() >= self.robot_y
    
    def check_coin_collected(self) -> bool:
        if self.coin_collected == False:
            if self.coin_y <= self.robot_y + self.robot.get_height() and self.coin_y + self.coin.get_height() >= self.robot_y:
                self.coin_collected = True
                self.coin_storage += 1

    def end_loop(self):
        while True:
            self.render_window()
            self.check_events()
            
    def main_loop(self):
        while True:
            self.move_monster(-9)
            self.check_events()
            self.render_window()
            self.check_coin_collected()
            if self.check_for_collision():
                break
            self.clock.tick(60)
        self.end = True
        self.end_loop()

if __name__ == "__main__":
    DodgeMonster()