from game.snake import SnakeGame

if __name__ == "__main__":
    while True:
        snake_game = SnakeGame()
        snake_game.start_screen()
        if snake_game.start(framerate=60):
            snake_game.win_screen()
        else:
            snake_game.lose_screen()
