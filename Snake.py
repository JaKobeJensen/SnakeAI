import SnakeGUI
import pygame
import os
import random
pygame.init
pygame.font.init()

GAME_BOARD_SIZE = 18
GAME_BOARD_IMG = pygame.image.load(os.path.join("images", "game_board.png"))
SNAKE_IMGS = [pygame.image.load(os.path.join("images", "snake_head.png")), pygame.image.load(os.path.join("images", "snake_body_straight.png")), \
              pygame.image.load(os.path.join("images", "snake_body_turn.png")), pygame.image.load(os.path.join("images", "snake_tail.png"))]
APPLE_IMG = pygame.image.load(os.path.join("images", "apple.png"))

class Snake:
    # setting up the different snake parts for easy access
    SNAKE_HEAD_IMG = {"right":SNAKE_IMGS[0], "left":pygame.transform.flip(SNAKE_IMGS[0], True, False), "up":pygame.transform.rotate(SNAKE_IMGS[0], 90), "down":pygame.transform.rotate(SNAKE_IMGS[0], -90)}
    SNAKE_BODY_STRAIGHT_IMG = {"right":SNAKE_IMGS[1], "left":SNAKE_IMGS[1], "up":pygame.transform.rotate(SNAKE_IMGS[1], 90), "down":pygame.transform.rotate(SNAKE_IMGS[1], 90)}
    SNAKE_BODY_TURN_IMG = {"rightup":SNAKE_IMGS[2], "rightdown":pygame.transform.rotate(SNAKE_IMGS[2], 90), "leftup":pygame.transform.rotate(SNAKE_IMGS[2], -90), "leftdown":pygame.transform.rotate(SNAKE_IMGS[2], 180), \
                            "upright":pygame.transform.rotate(SNAKE_IMGS[2], 180), "upleft":pygame.transform.rotate(SNAKE_IMGS[2], 90), "downright":pygame.transform.rotate(SNAKE_IMGS[2], -90), "downleft":SNAKE_IMGS[2]}
    SNAKE_TAIL_IMG = {"right":pygame.transform.flip(SNAKE_IMGS[3], True, False), "left":SNAKE_IMGS[3], "up":pygame.transform.rotate(SNAKE_IMGS[3], -90), "down":pygame.transform.rotate(SNAKE_IMGS[3], 90)}
    
    # Snake Part structure
    class SnakePart:
        def __init__(self) -> None:
            self.x:int=0
            self.y:int=0
            self.direction:str="right"
            self.image:pygame.Surface=None
    
    def __init__(self, starting_size:int=3, starting_position:tuple[int, int]=(7,8)) -> None:
        # setting up the snake as a list of SNAKE_PARTs
        self.snake_body = [self.SnakePart() for _ in range(starting_size)]
        self.snake_body[0].x = starting_position[0]
        self.snake_body[0].y = starting_position[1]
        self.snake_body[0].direction = "right"
        self.snake_body[0].image = self.SNAKE_HEAD_IMG[self.snake_body[0].direction]
        for i in range(1, starting_size):
            self.snake_body[i].x = self.snake_body[i - 1].x - 1
            self.snake_body[i].y = self.snake_body[i - 1].y
            self.snake_body[i].image = self.SNAKE_BODY_STRAIGHT_IMG[self.snake_body[i].direction]
        self.snake_body[starting_size - 1].image = self.SNAKE_TAIL_IMG[self.snake_body[starting_size - 1].direction]
        
        # lets us know what the pervious direction was for the snake
        self.previous_direction = self.snake_body[0].direction
        
    def move(self) -> None:
        # starting from the back until we get to one before the head, the current SNAKE_PART changes its x, y, direction and image to the SNAKE_PART in front of it
        for i in reversed(range(1, self.size())):
            self.snake_body[i].x = self.snake_body[i - 1].x
            self.snake_body[i].y = self.snake_body[i - 1].y
            self.snake_body[i].direction = self.snake_body[i - 1].direction
            self.snake_body[i].image = self.snake_body[i - 1].image
        self.snake_body[self.size() - 1].image = self.SNAKE_TAIL_IMG[self.snake_body[self.size() - 1].direction]
        
        # the head changes its x or y based on its direction        
        if self.snake_body[0].direction == "right":
            self.snake_body[0].x = self.snake_body[0].x + 1    
        elif self.snake_body[0].direction == "left":
            self.snake_body[0].x = self.snake_body[0].x - 1
        elif self.snake_body[0].direction == "up":
            self.snake_body[0].y = self.snake_body[0].y - 1
        elif self.snake_body[0].direction == "down":
            self.snake_body[0].y = self.snake_body[0].y + 1
        # changing the head's image based on its direction
        self.snake_body[0].image = self.SNAKE_HEAD_IMG[self.snake_body[0].direction]
        
        # see if we have a turn in one of the snake parts
        if self.snake_body[1].direction != self.snake_body[2].direction and self.size() >= 3:
            self.snake_body[1].image = self.SNAKE_BODY_TURN_IMG[self.snake_body[2].direction+self.snake_body[1].direction]
        else:
            self.snake_body[1].image = self.SNAKE_BODY_STRAIGHT_IMG[self.snake_body[1].direction]
            
        self.previous_direction = self.snake_body[0].direction
             
    def right(self) -> None:
        if self.previous_direction == "left":
            return
        self.snake_body[0].direction = "right"
        
    def left(self) -> None:
        if self.previous_direction == "right":
            return
        self.snake_body[0].direction = "left"
        
    def up(self) -> None:
        if self.previous_direction == "down":
            return
        self.snake_body[0].direction = "up"
        
    def down(self) -> None:
        if self.previous_direction == "up":
            return
        self.snake_body[0].direction = "down"
    
    def grow(self) -> None:
        # add SNAKE_PART to the list and copy previous end of the snake to the new end of the snake
        self.snake_body.append(self.SnakePart())
        self.snake_body[self.size() - 1].x = self.snake_body[self.size() - 2].x
        self.snake_body[self.size() - 1].y = self.snake_body[self.size() - 2].y
        self.snake_body[self.size() - 1].direction = self.snake_body[self.size() - 2].direction
        self.snake_body[self.size() - 1].image = self.snake_body[self.size() - 2].image
       
    def size(self) -> int:
        return len(self.snake_body)
    
class Apple:
    def __init__(self, position:tuple[int, int]=(0,0)) -> None:
        self.x = position[0]
        self.y = position[1]
        self.image = APPLE_IMG
        
    def new_position(self, position:tuple[int, int]) -> None:
        self.x = position[0]
        self.y = position[1]           

class SnakeGame:
    ANINATION_TIME = 10
    FONT = pygame.font.SysFont("comicsans", 32)
    
    def __init__(self, snake_starting_size:int=3, snake_starting_position:tuple[int,int]=(7,8), show_window=True) -> None:
        # initalize game board and file in the borders; -1 = wall or body, 0 = free space, 1 = head of snake, 2 = apple
        self.game_board = [[0 for x in range(GAME_BOARD_SIZE)] for y in range(GAME_BOARD_SIZE)]
        for i in range(GAME_BOARD_SIZE):
            self.game_board[i][0] = -1
            self.game_board[0][i] = -1
            self.game_board[i][GAME_BOARD_SIZE - 1] = -1
            self.game_board[GAME_BOARD_SIZE - 1][i] = -1
        
        # setting up the snake for our game   
        self.snake = Snake(snake_starting_size, snake_starting_position)
        
        # making a new apple with a random position on the game board that isn't occupied
        self.apple = Apple()
        self.new_apple()   

        self.update_game_board()
        
        self.score = 0
        self.image = GAME_BOARD_IMG
        
        if show_window:
            self.gui = SnakeGUI.SnakeGUI((self.image.get_width(), self.image.get_height() + 48))
        else:
            self.gui = None
            
        self.clock = pygame.time.Clock()
        # keeps track of each frame of the game
        self.game_ticks = 0
    
    def start(self, framerate:int=60) -> bool:
        if self.gui:
            self.draw()
        self.game_ticks = 0
        while True:
            self.clock.tick(framerate)
            self.game_ticks += 1
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.snake.right()
                    elif event.key == pygame.K_LEFT:
                        self.snake.left()
                    elif event.key == pygame.K_UP:
                        self.snake.up()
                    elif event.key == pygame.K_DOWN:
                        self.snake.down()  
            
            # updates the snake every 6 frames
            if self.game_ticks % (framerate/self.ANINATION_TIME) == 0:
                self.snake.move()
                
                # if head collides with wall or its body, player loses
                if self.collided_with_wall():
                    return False
                
                # increase the score and size of snake if the head collides with an apple
                if self.collided_with_apple():
                    self.score += 1
                    self.snake.grow()
                    # if the snake size becomes the size of the game_board then the player wins
                    if self.win():
                        return True
                    self.new_apple()
                    
                self.update_game_board()
                
                if self.gui:
                    self.draw()
    
    def update_game_board(self) -> None:
        for y in range(1, GAME_BOARD_SIZE - 1):
            for x in range(1, GAME_BOARD_SIZE - 1):
                self.game_board[y][x] = 0
        
        for i, snake_part in enumerate(self.snake.snake_body):
            if i == 0:
                self.game_board[snake_part.y][snake_part.x] = 1
                continue
            self.game_board[snake_part.y][snake_part.x] = -1
            
        self.game_board[self.apple.y][self.apple.x] = 2        
    
    def collided_with_wall(self) -> bool:
        if self.game_board[self.snake.snake_body[0].y][self.snake.snake_body[0].x] == -1:
            return True
        return False
    
    def collided_with_apple(self) -> bool:
        if self.game_board[self.snake.snake_body[0].y][self.snake.snake_body[0].x] == 2:
            return True
        return False
        
    def new_apple(self) -> None:
        while True:
            x = random.randint(1, 16)
            y = random.randint(1, 16)
            valid_position = True
            for snake_part in self.snake.snake_body:
                if x == snake_part.x and y == snake_part.y:
                    valid_position = False
                    break
            if valid_position:
                self.apple.new_position((x, y))
                return  
        
    def win(self) -> bool:
        if self.snake.size() >= 256:
            return True
        return False
    
    def get_game_board(self) -> list[list[int]]:
        return self.game_board
    
    def get_score(self) -> int:
        return self.score
    
    def draw(self) -> None:
        self.gui.clear_screen()
        self.gui.draw_snake_game(self, (0,48))
        self.gui.draw_text(f"Score: {self.score}", self.FONT, (255,255,255), (8,0))
        self.gui.update_screen()
    
    def win_screen(self) -> None:
        text = self.FONT.render("Congratulations, You Win!", 1, (255,255,255))
        self.gui.draw_surface(text, (self.image.get_width()/2 - text.get_width()/2, self.image.get_height()/2 - 4*text.get_height()))
        text = self.FONT.render("Press Space To Continue", 1, (255,255,255))
        self.gui.draw_surface(text, (self.image.get_width()/2 - text.get_width()/2, self.image.get_height()/2 - 3*text.get_height()))
        self.gui.update_screen()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return 
    
    def lose_screen(self) -> None:
        text = self.FONT.render("Game Over", 1, (255,255,255))
        self.gui.draw_surface(text, (self.image.get_width()/2 - text.get_width()/2, self.image.get_height()/2 - 4*text.get_height()))
        text = self.FONT.render("Press Space To Continue", 1, (255,255,255))
        self.gui.draw_surface(text, (self.image.get_width()/2 - text.get_width()/2, self.image.get_height()/2 - 3*text.get_height()))
        self.gui.update_screen()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return 
    
    def start_screen(self) -> None:
        self.draw()
        text = self.FONT.render("Press The Arrow Key To Start", 1, (255,255,255))
        self.gui.draw_surface(text, (self.image.get_width()/2 - text.get_width()/2, self.image.get_height()/2 - 4*text.get_height()))
        self.gui.update_screen()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.snake.right()
                        return
                    elif event.key == pygame.K_LEFT:
                        self.snake.left()
                        return
                    elif event.key == pygame.K_UP:
                        self.snake.up()
                        return
                    elif event.key == pygame.K_DOWN:
                        self.snake.down()  
                        return                        
          
if __name__ == "__main__":
    while True:
        snake_game = SnakeGame()
        snake_game.start_screen()
        if snake_game.start(framerate=60):
            snake_game.win_screen()
        else:
            snake_game.lose_screen()