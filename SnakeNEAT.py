import Snake
import pygame
import neat
import os
import pickle
pygame.init()
pygame.font.init()

def flatten_list(l:list) -> tuple:
    new_list = []
    for item in l:
        new_list = new_list + item
    return (new_list.copy())                   

def save_pickle(object:object, file_name:str, path:str=None) -> None:
    if path:
        file_name = os.path.join(path, f"{file_name}.pkl")
        if not os.path.exists(path):
            os.mkdir(path)
    else:
        file_name = os.path.join(os.curdir, f"{file_name}.pkl")
    
    n = 1
    while os.path.exists(file_name):
        file_name = f"{file_name}_{n}"
        n += 1
    
    with open(file_name, "wb") as f:
        pickle.dump(object, f)
        f.close()

def load_pickle(file_name:str, path:str=None) -> object:
    if ".pkl" not in file_name:
        print(f"{file_name} is not a .pkl")
        return None
    
    if path:
        file_name = os.path.join(path, file_name)
    else:
        file_name = os.path.join(os.curdir, file_name)
        
    with open(file_name, "rb") as f:
        object = pickle.load(f)
        
    return object

def square_around_snake_head(size:int, snake_game:Snake.SnakeGame) -> list:
    # snake head has a full square vision around it
    snake_head_position = (snake_game.snake.snake_body[0]["x"], snake_game.snake.snake_body[0]["y"])
    square = []
    
    for y in reversed(range(1, size + 1)):
        if snake_head_position[1] - y >= 0:
            for x in reversed(range(1, size + 1)):
                if snake_head_position[0] - x >= 0:
                    square.append(snake_game.game_board[snake_head_position[1] - y][snake_head_position[0] - x])
                else:
                    square.append(-1)
            square.append(snake_game.game_board[snake_head_position[1] - y][snake_head_position[0]])
            for x in range(1, size + 1):
                if snake_head_position[0] + x < Snake.GAME_BOARD_SIZE:
                    square.append(snake_game.game_board[snake_head_position[1] - y][snake_head_position[0] + x])
                else:
                    square.append(-1)
        else:
            for x in range(size*2 + 1):
                square.append(-1)
    
    for x in reversed(range(1, size + 1)):
        if snake_head_position[0] - x >= 0:
            square.append(snake_game.game_board[snake_head_position[1]][snake_head_position[0] - x])
        else:
            square.append(-1) 
    for x in range(1, size + 1):
        if snake_head_position[0] + x < Snake.GAME_BOARD_SIZE:
            square.append(snake_game.game_board[snake_head_position[1]][snake_head_position[0] + x])
        else:
            square.append(-1)        
    
    for y in range(1, size + 1):
        if snake_head_position[1] + y < Snake.GAME_BOARD_SIZE:
            for x in reversed(range(1, size + 1)):
                if snake_head_position[0] - x >= 0:
                    square.append(snake_game.game_board[snake_head_position[1] + y][snake_head_position[0] - x])
                else:
                    square.append(-1)
            square.append(snake_game.game_board[snake_head_position[1] + y][snake_head_position[0]])    
            for x in range(1, size + 1):
                if snake_head_position[0] + x < Snake.GAME_BOARD_SIZE:
                    square.append(snake_game.game_board[snake_head_position[1] + y][snake_head_position[0] + x])
                else:
                    square.append(-1)
        else:
            for x in range(2*size + 1):
                square.append(-1)
                
    return square        

def half_square_around_snake_head(size:int, snake_game:Snake.SnakeGame) -> list:
    # snake head has a half square vision in front of it based on the direction it is going
    snake_head_position = (snake_game.snake.snake_body[0]["x"], snake_game.snake.snake_body[0]["y"])
    snake_head_direction = snake_game.snake.snake_body[0]["direction"]
    half_square = []
    
    if snake_head_direction == "up":
        for y in reversed(range(1, size + 1)):
            if snake_head_position[1] - y >= 0:
                for x in reversed(range(1, size + 1)):
                    if snake_head_position[0] - x >= 0:
                        half_square.append(snake_game.game_board[snake_head_position[1] - y][snake_head_position[0] - x])
                    else:
                        half_square.append(-1)
                half_square.append(snake_game.game_board[snake_head_position[1] - y][snake_head_position[0]])    
                for x in range(1, size + 1):
                    if snake_head_position[0] + x < Snake.GAME_BOARD_SIZE:
                        half_square.append(snake_game.game_board[snake_head_position[1] - y][snake_head_position[0] + x])
                    else:
                        half_square.append(-1)
            else:
                for x in range(2*size + 1):
                    half_square.append(-1)
    
        for x in reversed(range(1, size + 1)):
            if snake_head_position[0] - x >= 0:
                half_square.append(snake_game.game_board[snake_head_position[1]][snake_head_position[0] - x])
            else:
                half_square.append(-1) 
        for x in range(1, size + 1):
            if snake_head_position[0] + x < Snake.GAME_BOARD_SIZE:
                half_square.append(snake_game.game_board[snake_head_position[1]][snake_head_position[0] + x])
            else:
                half_square.append(-1)
                    
    elif snake_head_direction == "down":
        for y in reversed(range(1, size + 1)):
            if snake_head_position[1] + y < Snake.GAME_BOARD_SIZE:
                for x in reversed(range(1, size + 1)):
                    if snake_head_position[0] + x < Snake.GAME_BOARD_SIZE:
                        half_square.append(snake_game.game_board[snake_head_position[1] + y][snake_head_position[0] + x])
                    else:
                        half_square.append(-1)
                half_square.append(snake_game.game_board[snake_head_position[1] + y][snake_head_position[0]])    
                for x in range(1, size + 1):
                    if snake_head_position[0] - x >= 0:
                        half_square.append(snake_game.game_board[snake_head_position[1] + y][snake_head_position[0] - x])
                    else:
                        half_square.append(-1)
            else:
                for x in range(2*size + 1):
                    half_square.append(-1)
    
        for x in reversed(range(1, size + 1)):
            if snake_head_position[0] + x < Snake.GAME_BOARD_SIZE:
                half_square.append(snake_game.game_board[snake_head_position[1]][snake_head_position[0] + x])
            else:
                half_square.append(-1) 
        for x in range(1, size + 1):
            if snake_head_position[0] - x >= 0:
                half_square.append(snake_game.game_board[snake_head_position[1]][snake_head_position[0] - x])
            else:
                half_square.append(-1)
                
    elif snake_head_direction == "left":
        for x in reversed(range(1, size + 1)):
            if snake_head_position[0] - x >= 0:
                for y in reversed(range(1, size + 1)):
                    if snake_head_position[1] + y < Snake.GAME_BOARD_SIZE:
                        half_square.append(snake_game.game_board[snake_head_position[1] + y][snake_head_position[0] - x])
                    else:
                        half_square.append(-1)
                half_square.append(snake_game.game_board[snake_head_position[1]][snake_head_position[0] - x])    
                for y in range(1, size + 1):
                    if snake_head_position[1] - y >= 0:
                        half_square.append(snake_game.game_board[snake_head_position[1] - y][snake_head_position[0] - x])
                    else:
                        half_square.append(-1)
            else:
                for y in range(2*size + 1):
                    half_square.append(-1)
    
        for y in reversed(range(1, size + 1)):
            if snake_head_position[1] + y < Snake.GAME_BOARD_SIZE:
                half_square.append(snake_game.game_board[snake_head_position[1] + y][snake_head_position[0]])
            else:
                half_square.append(-1) 
        for y in range(1, size + 1):
            if snake_head_position[1] - y >= 0:
                half_square.append(snake_game.game_board[snake_head_position[1] - y][snake_head_position[0]])
            else:
                half_square.append(-1)
                
    elif snake_head_direction == "right":
        for x in reversed(range(1, size + 1)):
            if snake_head_position[0] + x < Snake.GAME_BOARD_SIZE:
                for y in reversed(range(1, size + 1)):
                    if snake_head_position[1] - y >= 0:
                        half_square.append(snake_game.game_board[snake_head_position[1] - y][snake_head_position[0] + x])
                    else:
                        half_square.append(-1)
                half_square.append(snake_game.game_board[snake_head_position[1]][snake_head_position[0] + x])    
                for y in range(1, size + 1):
                    if snake_head_position[1] + y < Snake.GAME_BOARD_SIZE:
                        half_square.append(snake_game.game_board[snake_head_position[1] + y][snake_head_position[0] + x])
                    else:
                        half_square.append(-1)
            else:
                for y in range(2*size + 1):
                    half_square.append(-1)
    
        for y in reversed(range(1, size + 1)):
            if snake_head_position[1] - y >= 0:
                half_square.append(snake_game.game_board[snake_head_position[1] - y][snake_head_position[0]])
            else:
                half_square.append(-1) 
        for y in range(1, size + 1):
            if snake_head_position[1] + y < Snake.GAME_BOARD_SIZE:
                half_square.append(snake_game.game_board[snake_head_position[1] + y][snake_head_position[0]])
            else:
                half_square.append(-1)
        
    return half_square

def circle_around_snake_head(size:int, snake_game:Snake.SnakeGame) -> list:
    # snake head has a full circular vision around it
    snake_head_position = (snake_game.snake.snake_body[0]["x"], snake_game.snake.snake_body[0]["y"])
    circle = []
    
    # scans from left to right and from top to bottom, if vision is outside the playing area it gets a -1
    for y in reversed(range(1, size + 1)):
        if snake_head_position[1] - y >= 0:
            for x in reversed(range(1, (size - y) + 1)):
                if snake_head_position[0] - x >= 0:
                    circle.append(snake_game.game_board[snake_head_position[1] - y][snake_head_position[0] - x])
                else:
                    circle.append(-1)
            circle.append(snake_game.game_board[snake_head_position[1] - y][snake_head_position[0]])    
            for x in range(1, (size - y) + 1):
                if snake_head_position[0] + x < Snake.GAME_BOARD_SIZE:
                    circle.append(snake_game.game_board[snake_head_position[1] - y][snake_head_position[0] + x])
                else:
                    circle.append(-1)
        else:
            for x in range(2*(size - y) + 1):
                circle.append(-1)
    
    for x in reversed(range(1, size + 1)):
        if snake_head_position[0] - x >= 0:
            circle.append(snake_game.game_board[snake_head_position[1]][snake_head_position[0] - x])
        else:
            circle.append(-1) 
    for x in range(1, size + 1):
        if snake_head_position[0] + x < Snake.GAME_BOARD_SIZE:
            circle.append(snake_game.game_board[snake_head_position[1]][snake_head_position[0] + x])
        else:
            circle.append(-1)     
    
    for y in range(1, size + 1):
        if snake_head_position[1] + y < Snake.GAME_BOARD_SIZE:
            for x in reversed(range(1, (size - y) + 1)):
                if snake_head_position[0] - x >= 0:
                    circle.append(snake_game.game_board[snake_head_position[1] + y][snake_head_position[0] - x])
                else:
                    circle.append(-1)
            circle.append(snake_game.game_board[snake_head_position[1] + y][snake_head_position[0]])    
            for x in range(1, (size - y) + 1):
                if snake_head_position[0] + x < Snake.GAME_BOARD_SIZE:
                    circle.append(snake_game.game_board[snake_head_position[1] + y][snake_head_position[0] + x])
                else:
                    circle.append(-1)
        else:
            for x in range(2*(size - y) + 1):
                circle.append(-1)      

    return circle

def half_circle_around_snake_head(size:int, snake_game:Snake.SnakeGame) -> list:
    # snake head has a half circle vision in front of it based on the direction it is going
    snake_head_position = (snake_game.snake.snake_body[0].x, snake_game.snake.snake_body[0].y)
    snake_head_direction = snake_game.snake.snake_body[0].direction
    half_circle = []
    
    if snake_head_direction == "up":
        for y in reversed(range(1, size + 1)):
            if snake_head_position[1] - y >= 0:
                for x in reversed(range(1, (size - y) + 1)):
                    if snake_head_position[0] - x >= 0:
                        half_circle.append(snake_game.game_board[snake_head_position[1] - y][snake_head_position[0] - x])
                    else:
                        half_circle.append(-1)
                half_circle.append(snake_game.game_board[snake_head_position[1] - y][snake_head_position[0]])    
                for x in range(1, (size - y) + 1):
                    if snake_head_position[0] + x < Snake.GAME_BOARD_SIZE:
                        half_circle.append(snake_game.game_board[snake_head_position[1] - y][snake_head_position[0] + x])
                    else:
                        half_circle.append(-1)
            else:
                for x in range((size - y) + 1):
                    half_circle.append(-1)
    
        for x in reversed(range(1, size + 1)):
            if snake_head_position[0] - x >= 0:
                half_circle.append(snake_game.game_board[snake_head_position[1]][snake_head_position[0] - x])
            else:
                half_circle.append(-1) 
        for x in range(1, size + 1):
            if snake_head_position[0] + x < Snake.GAME_BOARD_SIZE:
                half_circle.append(snake_game.game_board[snake_head_position[1]][snake_head_position[0] + x])
            else:
                half_circle.append(-1)
                    
    elif snake_head_direction == "down":
        for y in reversed(range(1, size + 1)):
            if snake_head_position[1] + y < Snake.GAME_BOARD_SIZE:
                for x in reversed(range(1, (size - y) + 1)):
                    if snake_head_position[0] + x < Snake.GAME_BOARD_SIZE:
                        half_circle.append(snake_game.game_board[snake_head_position[1] + y][snake_head_position[0] + x])
                    else:
                        half_circle.append(-1)
                half_circle.append(snake_game.game_board[snake_head_position[1] + y][snake_head_position[0]])    
                for x in range(1, (size - y) + 1):
                    if snake_head_position[0] - x >= 0:
                        half_circle.append(snake_game.game_board[snake_head_position[1] + y][snake_head_position[0] - x])
                    else:
                        half_circle.append(-1)
            else:
                for x in range((size - y) + 1):
                    half_circle.append(-1)
    
        for x in reversed(range(1, size + 1)):
            if snake_head_position[0] + x < Snake.GAME_BOARD_SIZE:
                half_circle.append(snake_game.game_board[snake_head_position[1]][snake_head_position[0] + x])
            else:
                half_circle.append(-1) 
        for x in range(1, size + 1):
            if snake_head_position[0] - x >= 0:
                half_circle.append(snake_game.game_board[snake_head_position[1]][snake_head_position[0] - x])
            else:
                half_circle.append(-1)
                
    elif snake_head_direction == "left":
        for x in reversed(range(1, size + 1)):
            if snake_head_position[0] - x >= 0:
                for y in reversed(range(1, (size - x) + 1)):
                    if snake_head_position[1] + y < Snake.GAME_BOARD_SIZE:
                        half_circle.append(snake_game.game_board[snake_head_position[1] + y][snake_head_position[0] - x])
                    else:
                        half_circle.append(-1)
                half_circle.append(snake_game.game_board[snake_head_position[1]][snake_head_position[0] - x])    
                for y in range(1, (size - x) + 1):
                    if snake_head_position[1] - y >= 0:
                        half_circle.append(snake_game.game_board[snake_head_position[1] - y][snake_head_position[0] - x])
                    else:
                        half_circle.append(-1)
            else:
                for y in range((size - x) + 1):
                    half_circle.append(-1)
    
        for y in reversed(range(1, size + 1)):
            if snake_head_position[1] + y < Snake.GAME_BOARD_SIZE:
                half_circle.append(snake_game.game_board[snake_head_position[1] + y][snake_head_position[0]])
            else:
                half_circle.append(-1) 
        for y in range(1, size + 1):
            if snake_head_position[1] - y >= 0:
                half_circle.append(snake_game.game_board[snake_head_position[1] - y][snake_head_position[0]])
            else:
                half_circle.append(-1)
                
    elif snake_head_direction == "right":
        for x in reversed(range(1, size + 1)):
            if snake_head_position[0] + x < Snake.GAME_BOARD_SIZE:
                for y in reversed(range(1, (size - x) + 1)):
                    if snake_head_position[1] - y >= 0:
                        half_circle.append(snake_game.game_board[snake_head_position[1] - y][snake_head_position[0] + x])
                    else:
                        half_circle.append(-1)
                half_circle.append(snake_game.game_board[snake_head_position[1]][snake_head_position[0] + x])    
                for y in range(1, (size - x) + 1):
                    if snake_head_position[1] + y < Snake.GAME_BOARD_SIZE:
                        half_circle.append(snake_game.game_board[snake_head_position[1] + y][snake_head_position[0] + x])
                    else:
                        half_circle.append(-1)
            else:
                for y in range((size - x) + 1):
                    half_circle.append(-1)
    
        for y in reversed(range(1, size + 1)):
            if snake_head_position[1] - y >= 0:
                half_circle.append(snake_game.game_board[snake_head_position[1] - y][snake_head_position[0]])
            else:
                half_circle.append(-1) 
        for y in range(1, size + 1):
            if snake_head_position[1] + y < Snake.GAME_BOARD_SIZE:
                half_circle.append(snake_game.game_board[snake_head_position[1] + y][snake_head_position[0]])
            else:
                half_circle.append(-1)
        
    return half_circle

def snake_head_direction(snake_game:Snake.SnakeGame) -> list:
    # the snake head's direction, 1 is the direction it is going and -1 is not the direction it is going
    snake_head_direction = snake_game.snake.snake_body[0].direction
    inputs = []
    
    if snake_head_direction == "up":
        inputs.append(1)    # North
        inputs.append(-1)   # East
        inputs.append(-1)   # South
        inputs.append(-1)   # West
    elif snake_head_direction == "right":
        inputs.append(-1)   # North
        inputs.append(1)    # East
        inputs.append(-1)   # South
        inputs.append(-1)   # West
    elif snake_head_direction == "down":
        inputs.append(-1)   # North
        inputs.append(-1)   # East
        inputs.append(1)    # South
        inputs.append(-1)   # West
    elif snake_head_direction == "left":
        inputs.append(-1)   # North
        inputs.append(-1)   # East
        inputs.append(-1)   # South
        inputs.append(1)    # West
    
    return inputs
    
def apple_position_to_snake_head(snake_game:Snake.SnakeGame) -> list:
    snake_head_position = (snake_game.snake.snake_body[0].x, snake_game.snake.snake_body[0].y)
    apple_position = (snake_game.apple.x, snake_game.apple.y)
    inputs = []
    
    # the snake knows if the apple is North, East, South or West from the head of the snake
    if apple_position[1] < snake_head_position[1]:
        inputs.append(1) # North
        if apple_position[0] > snake_head_position[0]:
            inputs.append(1)  # East
            inputs.append(-1) # South
            inputs.append(-1) # West
        elif apple_position[0] < snake_head_position[0]:
            inputs.append(-1) # East
            inputs.append(-1) # South
            inputs.append(1)  # West
        else:
            inputs.append(-1) # East
            inputs.append(-1) # South
            inputs.append(-1) # West
    elif apple_position[1] > snake_head_position[1]:
        inputs.append(-1) # North
        if apple_position[0] > snake_head_position[0]:
            inputs.append(1)  # East
            inputs.append(1)  # South
            inputs.append(-1) # West
        elif apple_position[0] < snake_head_position[0]:
            inputs.append(-1) # East
            inputs.append(1)  # South
            inputs.append(1)  # West
        else:
            inputs.append(-1) # East
            inputs.append(1) # South
            inputs.append(-1) # West
    else:
        inputs.append(-1) # North
        if apple_position[0] > snake_head_position[0]:
            inputs.append(1)  # East
            inputs.append(-1) # South
            inputs.append(-1) # West
        elif apple_position[0] < snake_head_position[0]:
            inputs.append(-1) # East
            inputs.append(-1) # South
            inputs.append(1)  # West
        else:
            inputs.append(-1) # East
            inputs.append(-1) # South
            inputs.append(-1) # West
    
    return inputs  

class SnakeGenome:
    def __init__(self):
       self.genome:neat.DefaultGenome = None
       self.network:neat.nn.FeedForwardNetwork = None
       self.snake_game:Snake.SnakeGame = None
       self.apples_position_history:list[tuple[int,int]] = []
       self.timeout_timer:int = 0

class SnakeNEAT:
    # Frames per second for training
    TRAINING_FRAMERATE = 240
    # Frames per second for the replays
    REPLAY_FRAMERATE = 20
    # Fitness per apple
    SCORE_FITNESS = 1
    # Fitness when losing, colliding into the wall or body
    COLLIDE_FITNESS = -1
    # The amount of time, in seconds, before a genome's game ends if they do not collect an apple in that time
    FITNESS_TIMEOUT = 10

    def __init__(self, config_path:str=None, config:neat.Config=None) -> None:
        self.new_config(config_path, config)
        self.clock = pygame.time.Clock()
        self.show_replays:bool = False
        self.best_fitness_history:list[int] = []
        self.best_fitness = -100

    def train(self, generations:int=50, population:int=100, show_replays:bool=True, hidden_layers:int=0, vision_mode:str="half_circle", vision_length:int=1, direction_knowleadge:bool=True, apple_position_knowleadge:bool=True, output_mode:str="regular") -> neat.DefaultGenome:
        if not self.config:
            print(f"No Config")
            return None
        self.update_config(population, hidden_layers, vision_mode, vision_length, direction_knowleadge, apple_position_knowleadge, output_mode)
        self.show_replays = show_replays
        self.input_config = [vision_mode, vision_length, direction_knowleadge, apple_position_knowleadge]
        self.output_config = output_mode
        winner = self.population.run(self.fitness_function, generations)
        self.population.best_genome.fitness = self.best_fitness 
        return winner       
            
    def fitness_function(self, incoming_genomes:list[tuple[int, neat.DefaultGenome]], config:neat.Config) -> None:
        # place to store all of the genomes for this generation
        snake_genomes:list[SnakeGenome] = []
        total_population_size = len(self.population.population)
        # if there are replays, draw the loading screen
        if self.show_replays:
            loading_screen = Snake.SnakeGame(show_window=True)
            self.draw_loading(loading_screen, total_population_size, 0)
        else:
            loading_screen = Snake.SnakeGame(show_window=False)
            
        # set up all of the genomes, neural networks and birds
        for genome_id, genome in incoming_genomes:
            snake_genomes.append(SnakeGenome())
            genome.fitness = 0
            snake_genomes[-1].genome = genome
            snake_genomes[-1].network = neat.nn.FeedForwardNetwork.create(genome, config)
            snake_genomes[-1].snake_game = Snake.SnakeGame(show_window=False)
            snake_genomes[-1].snake_game.apple.new_position((loading_screen.apple.x, loading_screen.apple.y))
            snake_genomes[-1].apples_position_history.append((loading_screen.apple.x, loading_screen.apple.y))
        
        # keeping track of the best genome in this generation
        best_genome:SnakeGenome = None
        
        # running the games of snake 
        while True:
            # how fast the game runs
            self.clock.tick(self.TRAINING_FRAMERATE)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
            
            # going through each snake game and letting the AI move
            for idx, snake_genome in enumerate(snake_genomes):
                # count each tick of the game
                snake_genome.snake_game.game_ticks += 1
                snake_genome.timeout_timer += 1
                
                # predicting the next move based on the game state  
                self.predict(snake_genome.network, snake_genome.snake_game)
                
                # moving the snake
                snake_genome.snake_game.snake.move()
                
                # increase the score, the fitness score and size of snake if the head collides with an apple
                if snake_genome.snake_game.collided_with_apple():
                    # increase the score and fitness score
                    snake_genome.snake_game.score += 1
                    snake_genome.genome.fitness += self.SCORE_FITNESS
                    # reset the timeout timer because the snake ate an apple 
                    snake_genome.timeout_timer = 0
                    # increase the snake's size
                    snake_genome.snake_game.snake.grow()
                    # if the snake did not win set a new apple on the game board
                    if not snake_genome.snake_game.win():
                        snake_genome.snake_game.new_apple()
                        snake_genome.apples_position_history.append((snake_genome.snake_game.apple.x, snake_genome.snake_game.apple.y))
                
                # if head collides with wall or its body, player loses 
                # checks to see if the snake is in an infinte loop, ends their game if they are
                # if the snake size becomes the size of the game_board then the player wins
                if snake_genome.snake_game.collided_with_wall() or snake_genome.snake_game.win() or snake_genome.timeout_timer > self.REPLAY_FRAMERATE*(self.FITNESS_TIMEOUT):
                    # decrease the genome's fitness a little to decentivize running into the wall or body
                    #if snake_genome.snake_game.collided_with_wall():
                        #snake_genome.genome.fitness += self.COLLIDE_FITNESS
                        
                    # saving the best genome of this population 
                    if not best_genome or snake_genome.genome.fitness > best_genome.genome.fitness:
                        best_genome = snake_genome
                        
                    # pop the genome out of the list because their game is done
                    snake_genomes.pop(idx)
                    
                    # draw the loading screen if the user wants replays
                    if self.show_replays:
                        self.draw_loading(loading_screen, total_population_size, total_population_size - len(snake_genomes))
                        
                    continue
                
                # updates the snake game's game board    
                snake_genome.snake_game.update_game_board()          
            
            # if there are no more snake genomes we are done with this generation 
            if len(snake_genomes) == 0:
                break
        
        #self.average_fitness = round((self.average_fitness + best_genome.genome.fitness) / self.population.generation)
        self.best_fitness_history.append(best_genome.genome.fitness)
        # keep track of the best fitness
        if best_genome.genome.fitness > self.best_fitness:
            self.best_fitness = best_genome.genome.fitness
        # shows the best snake from the population on screen if their are replays for the user to see
        if self.show_replays:     
            self.replay(best_genome.genome, self.config, best_genome.apples_position_history)              
    
    def replay(self, genome:neat.DefaultGenome, config:neat.Config, apples_position_history:list[tuple[int, int]]=None, replay_speed=20) -> None:
        self.REPLAY_FRAMERATE = replay_speed
        snake_game = Snake.SnakeGame()
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        fitness = 0
        timeout_timer = 0
        
        if apples_position_history:
            snake_game.apple.new_position(apples_position_history.pop(0))
        
        self.draw_window(snake_game, fitness)
        snake_game.game_ticks = 0
        while True:
            snake_game.clock.tick(self.REPLAY_FRAMERATE)
            snake_game.game_ticks += 1
            timeout_timer += 1
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
            
            # based on the game board, the AI chooses either right, left, up or down
            self.predict(network, snake_game)
             
            snake_game.snake.move()
                
            # if head collides with wall or its body, player loses
            if snake_game.collided_with_wall():
                #fitness += self.COLLIDE_FITNESS
                self.draw_window(snake_game, fitness)
                return
            
            # increase the score and size of snake if the head collides with an apple
            if snake_game.collided_with_apple():
                snake_game.score += 1
                fitness += self.SCORE_FITNESS
                timeout_timer = 0
                snake_game.snake.grow()
                # if the snake size becomes the size of the game_board then the player wins
                if snake_game.win():
                    self.draw_window(snake_game, fitness)
                    return
                if apples_position_history or len(apples_position_history) > 0:
                    snake_game.apple.new_position(apples_position_history.pop(0))
                else:
                    snake_game.new_apple()
            
            if timeout_timer > self.REPLAY_FRAMERATE*self.FITNESS_TIMEOUT:
                return 
                
            snake_game.update_game_board()
            self.draw_window(snake_game, fitness)
    
    def predict(self, network:neat.nn.FeedForwardNetwork, snake_game:Snake.SnakeGame) -> None:
        # based on the game board, the AI chooses either right, left, up or down
        outputs = network.activate(self.inputs(snake_game))
        best_output = (0, 0)
        for i, output in enumerate(outputs):
            if output > best_output[1]:
                best_output = (i, output)
        
        if self.output_config == "regular":
            # changes the direction of the snake (up, right, down, left)
            if best_output[0] == 0:
                snake_game.snake.up()
            elif best_output[0] == 1:
                snake_game.snake.right()
            elif best_output[0] == 2:
                snake_game.snake.down()
            elif best_output[0] == 3:
                snake_game.snake.left()
        else: # mode == "directional"    
            # changes the direction of the snake, (left, straight, right) based on the direction of the snake head
            snake_head_direction = snake_game.snake.snake_body[0]["direction"]
            if snake_head_direction == "up":
                if best_output[0] == 0:
                    snake_game.snake.left()
                elif best_output[0] == 1:
                    snake_game.snake.up()
                elif best_output[0] == 2:
                    snake_game.snake.right()
            if snake_head_direction == "right":
                if best_output[0] == 0:
                    snake_game.snake.up()
                elif best_output[0] == 1:
                    snake_game.snake.right()
                elif best_output[0] == 2:
                    snake_game.snake.down()
            if snake_head_direction == "down":
                if best_output[0] == 0:
                    snake_game.snake.right()
                elif best_output[0] == 1:
                    snake_game.snake.down()
                elif best_output[0] == 2:
                    snake_game.snake.left()
            if snake_head_direction == "left":
                if best_output[0] == 0:
                    snake_game.snake.down()
                elif best_output[0] == 1:
                    snake_game.snake.left()
                elif best_output[0] == 2:
                    snake_game.snake.up()      
        
    def inputs(self, snake_game:Snake.SnakeGame) -> tuple:
        # whole view of the game board; vision_mode="whole_board"
        if self.input_config[0] == "whole_board":
            inputs = flatten_list(snake_game.game_board)
        # circle vision around head of snake; vision_mode="circle"
        elif self.input_config[0] == "circle":
            inputs = circle_around_snake_head(self.input_config[1], snake_game)
        # half circle vision around head of snake; vision_mode="half_circle"
        elif self.input_config[0] == "half_circle":
            inputs = half_circle_around_snake_head(self.input_config[1], snake_game)
        # square vision around head of snake, vision_mode="square"
        elif self.input_config[0] == "square":
            inputs = square_around_snake_head(self.input_config[1], snake_game)
        # half square vision around head of snake; vision_mode="half_square"
        elif self.input_config[0] == "half_square":
            inputs = half_square_around_snake_head(self.input_config[1], snake_game)
        # if no mode then the snake has no vision; vision="none"
        else:
            inputs = []
           
        # the snake head direction; direction_knowledge=True
        if self.input_config[2]:
            inputs = inputs + snake_head_direction(snake_game)
        
        # the snake knows if the apple is North, East, South or West from the head of the snake; apple_position_knowleadge
        if self.input_config[3]:
            inputs = inputs + apple_position_to_snake_head(snake_game)
        
        return tuple(inputs)   
    
    def draw_window(self, snake_game:Snake.SnakeGame, fitness_score:int) -> None:
        snake_game.draw()
        gen_text = pygame.font.SysFont("comicsans", 32).render(f"Gen: {str(self.population.generation)}", 1, (255,255,255))
        snake_game.gui.window.blit(gen_text, (snake_game.gui.get_width() - gen_text.get_width(), 0))
        fitness_text = pygame.font.SysFont("comicsans", 16).render(f"Fitness Score: {round(fitness_score, 2)}", 1, (255,255,255))
        snake_game.gui.window.blit(fitness_text, (snake_game.gui.get_width()/2 - fitness_text.get_width()/2, 0))
        best_fitness_text = pygame.font.SysFont("comicsans", 16).render(f"Best Fitness: {round(self.best_fitness, 3)}", 1, (255,255,255))
        snake_game.gui.window.blit(best_fitness_text, (snake_game.gui.get_width()/2 - best_fitness_text.get_width()/2, fitness_text.get_height()))
        pygame.display.update()
    
    def draw_loading(self, snake_game:Snake.SnakeGame, total_population_size:int, remaining_population_size:int) -> None:
        self.draw_window(snake_game, 0)
        loading_text = pygame.font.SysFont("comicsans", 32).render(f"Loading... ({remaining_population_size}/{total_population_size})", 1, (255,255,255))
        snake_game.gui.window.blit(loading_text, (snake_game.gui.get_width()/2 - loading_text.get_width()/2, snake_game.gui.get_height()/2 - loading_text.get_height()/2))
        pygame.display.update()
    
    def update_config(self, population:int, hidden_layers:int, vision_mode:str, vision_length:int, direction_knowleadge:bool, apple_position_knowleadge:bool, output_mode:int) -> None:
        if vision_mode == "whole_board":
            self.config.genome_config.num_inputs = 324
        elif vision_mode == "circle":
            self.config.genome_config.num_inputs = 4 * sum([x for x in range(1, vision_length + 1)])
        elif vision_mode == "half_circle":
            self.config.genome_config.num_inputs = (3 * vision_length) + (2 * sum([x for x in range(1, vision_length)]))
        elif vision_mode == "square":
            self.config.genome_config.num_inputs = (vision_length*2 + 1)**2 - 1
        elif vision_mode == "half_square":
            self.config.genome_config.num_inputs = ((vision_length*2 + 1) * (vision_length + 1)) - 1
        else: # vision_mode == "none"
            self.config.genome_config.num_inputs = 0
        
        if direction_knowleadge:
            self.config.genome_config.num_inputs += 4
            
        if apple_position_knowleadge:
            self.config.genome_config.num_inputs += 4
        
        if output_mode == "regular":
            self.config.genome_config.num_outputs = 4
        else:
            self.config.genome_config.num_outputs = 3
            
        self.config.genome_config.num_hidden = hidden_layers
        self.config.pop_size = population
        
        self.new_population()
    
    def new_config(self, config_path:str=None, config:neat.Config=None) -> None:
        if config:
            self.config = config
            self.new_population()   
        elif config_path:
            self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
            self.new_population()   
        else:
            self.config:neat.Config = None
            self.population:neat.Population = None
    
    def new_population(self, config:neat.Config=None) -> None:
        self.population = None
        if config:
            self.population = neat.Population(config)
            self.config = config
        elif self.config:
            self.population = neat.Population(self.config)
        else:
            print("No Config")
            return
        self.population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        self.population.add_reporter(stats)
        self.best_fitness = -100
        self.show_replays = False
        self.input_config = [None, None, None, None]
    
    def get_best_genome(self) -> neat.DefaultGenome:
        return self.population.best_genome
    
    def report(self) -> None:
        print(f"REPORT:")
        print(f"Best Fitness: {self.best_fitness}\nAverage Fitness: {self.average_fitness}\nGeneration: {self.population.generation}\nPopulation Size: {len(self.population.population)}") 
        print(f"Vision Mode: {self.input_config[0]}\nVision Length: {self.input_config[1]}\nDirection Knowleadge: {self.input_config[2]}\nApple Position Knowleadge: {self.input_config[3]}\n")
    
    def save_report(self, file_name:str=None, path:str=None) -> None:
        if not file_name:
            file_name = f"SnakeNEAT_report_{self.population.generation}generations"
        
        if path:
            file_name = os.path.join(path, f"{file_name}.txt")
            if not os.path.exists(path):
                os.mkdir(path)
        else:
            file_name = os.path.join(os.curdir, f"{file_name}.txt")
        
        n = 1
        while os.path.exists(file_name):
            file_name = f"{file_name}_{n}"
            n += 1
        
        with open(file_name, "w") as f:
            f.write(f"Best Fitness: {self.best_fitness}\nAverage Fitness: {self.average_fitness}\nGeneration: {self.population.generation}\nPopulation Size: {len(self.population.population)}\n")
            f.write(f"Vision Mode: {self.input_config[0]}\nVision Length: {self.input_config[1]}\nDirection Knowleadge: {self.input_config[2]}\nApple Position Knowleadge: {self.input_config[3]}\n")
            f.close()
    
    def speed_up_replay(self, speed_up_by:int=5) -> None:
        self.REPLAY_FRAMERATE += speed_up_by
    
    def slow_down_replay(self, slow_down_by:int=5) -> None:
        self.REPLAY_FRAMERATE -= slow_down_by
    
    def set_replay_speed(self, speed:int) -> None:
        self.REPLAY_FRAMERATE = speed
    
    def speed_up_training(self, speed_up_by:int=5) -> None:
        self.TRAINING_FRAMERATE += speed_up_by
        
    def slow_down_training(self, slow_down_by:int=5) -> None:
        self.TRAINING_FRAMERATE += slow_down_by
    
    def set_training_speed(self, speed:int) -> None:
        self.TRAINING_FRAMERATE = speed
    
    def quit(self) -> None:
        #self.save_population()
        pygame.quit()
        quit()
    
    
if __name__ == "__main__":
    SnakeTraining = SnakeNEAT(config_path="neat_config.txt")
    SnakeTraining.train(generations=5000)
    quit()