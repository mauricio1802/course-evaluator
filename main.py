from src.game_implementation import NumericGame, print_state, Student, Professor
from src.game.player import Play
from src.game_implementation.players import StudentHumanPlayer, ProfessorHumanPlayer

players = [
    StudentHumanPlayer(None, 0.5, 6),
    StudentHumanPlayer(None, 0.3, 3),
    ProfessorHumanPlayer(None)
]

match = NumericGame.get_match(players)

while True:
    state = match.get_state()
    print_state(state)
    match.move()

