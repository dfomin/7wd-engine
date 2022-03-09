from .agents import ConsoleAgent
from .game import Game


def play():
    state = Game.create()
    agent = ConsoleAgent()
    while not Game.is_finished(state):
        actions = Game.get_available_actions(state)
        print(Game.print(state))
        selected_action = agent.choose_action(state, actions)
        Game.apply_action(state, selected_action)


if __name__ == "__main__":
    play()
