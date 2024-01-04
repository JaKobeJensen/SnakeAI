from SnakeNEAT import SnakeNEAT
import os

def train(config_path:str, generation:int, population:int, vision_mode:str, vision_length:int, direction_knowleadge:bool, apple_position_knowleadge:bool) -> None:
    snake_training = SnakeNEAT(config_path)
    snake_training.train(generation, population, False, 0, vision_mode, vision_length, direction_knowleadge, apple_position_knowleadge, "regular")
    print("\n")
    snake_training.save_report(file_name=f"SnakeNEAT_report_{vision_mode}{vision_length}_{generation}gen_{population}pop", path="SnakeNEAT\\reports")
    snake_training.save_population(file_name=f"SnakeNEAT_population_{vision_mode}{vision_length}_{generation}gen_{population}pop", path="SnakeNEAT\\populations")
    
def replay(population_file:str, population_path:str) -> None:
    snake_training = None
    snake_training = SnakeNEAT()
    snake_training.restore_population(population_file, population_path)
    snake_training.report()
    snake_training.replay(genome=snake_training.population.best_genome, config=snake_training.config, replay_speed=10)

if __name__ == "__main__":
    populations = os.listdir("SnakeNEAT\\populations")
    for population in populations:
        replay(population, "SnakeNEAT\\populations")
    quit()