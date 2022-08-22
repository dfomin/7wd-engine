from .agents import ConsoleAgent
from .game import Game


def play():
    game = Game()
    agent = ConsoleAgent()
    while not game.is_finished:
        actions = game.get_available_actions()
        # print(game.print(state)
        selected_action = agent.choose_action(game, actions)
        game.apply_action(selected_action)


if __name__ == "__main__":
    play()
