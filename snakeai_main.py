from game.snake_neat_training import SnakeNEAT

if __name__ == "__main__":
    SnakeTraining = SnakeNEAT(config_path="game/neat_config.txt")
    SnakeTraining.train(
        generations=50,
        population=100,
        show_replays=True,
        hidden_layers=0,
        vision_mode="half_circle",
        vision_length=1,
        direction_knowleadge=True,
        apple_position_knowleadge=True,
        output_mode="regular",
    )
