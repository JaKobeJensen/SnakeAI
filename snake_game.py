from snake import SnakeGame  
        
def main() -> None:
    while True:
        snake_game = SnakeGame()
        snake_game.start_screen()
        if snake_game.start(framerate=60):
            snake_game.win_screen()
        else:
            snake_game.lose_screen()
          
if __name__ == "__main__":
    main()