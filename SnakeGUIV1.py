import pygame
import SnakeV1

class SnakeGUI:
    def __init__(self, window_size:tuple[int,int]=(100,100)) -> None:
        self.window:pygame.Surface = pygame.display.set_mode(window_size)
    
    def draw_snake_game(self, snake_game:SnakeV1.SnakeGame, position:tuple[int,int]=(0,0)) -> None:                    
        self.draw_surface(snake_game.image, position)
        
        for snake_part in snake_game.snake.snake_body:
            self.draw_surface(snake_part.image, (((snake_part.x - 1) * snake_part.image.get_width()) + position[0], ((snake_part.y - 1) * snake_part.image.get_height()) + position[1]))
        
        self.draw_surface(snake_game.apple.image, (((snake_game.apple.x - 1) * snake_game.apple.image.get_width()) + position[0], ((snake_game.apple.y - 1) * snake_game.apple.image.get_height()) + position[1]))
        
    def draw_text(self, text:str, font:pygame.font.Font, font_color:tuple[int,int,int], position:tuple[int,int], background_color:tuple[int,int,int]=None) -> None:
        surface = font.render(text, 1, font_color)
        if background_color:
            pygame.draw.rect(self.window, background_color, pygame.Rect(position[0],position[1],surface.get_width(),surface.get_height()))
        self.window.blit(surface, position)
    
    def draw_surface(self, surface:pygame.Surface, position:tuple[int,int], background_color:tuple[int,int,int]=None) -> None:
        if background_color:
            pygame.draw.rect(self.window, background_color, pygame.Rect(position[0],position[1],surface.get_width(),surface.get_height()))
        self.window.blit(surface, position)
    
    def change_background_color(self, color:tuple[int,int,int]):
        self.window.fill(color)
    
    def clear_screen(self) -> None:
        self.window.fill((0,0,0))
    
    def update_screen(self) -> None:
        pygame.display.update()
    
    def update_window_size(self, window_size:tuple[int,int]=(100,100)) -> None:
        self.window = pygame.display.set_mode(window_size)
    
    def get_width(self) -> int:
        return self.window.get_width()
    
    def get_height(self) -> int:
        return self.window.get_height()  