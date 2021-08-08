from json import load
from ....game import Player, Play
from ...game import AddChallengePayload, RemoveChallengePayload
from ...state import ChallengeDefinition, Challenge, Professor, Student

class ProfessorChallengesFromJsonPlayer(Professor, Player):
    def __init__(self, id, json_file):
        Professor.__init__(self, id)
        self._challenges = []
        with open(json_file, 'r') as f:
            self._challenges = load(f)
        self._plays_per_round = None 
        self._last_challenge_id = 0
        
    
    def set_id(self, id):
        self.player_id = id
    
    def _get_challenge_id(self):
        self._last_challenge_id += 1
        return self._last_challenge_id
    
    def _generate_for_all_players(self, challenge, number_of_students):
        challenges = []
        challenge_definition = ChallengeDefinition(challenge['interest'], challenge['cost'], challenge['reward'])
        for student_id in range(2, 2 + number_of_students):
            challenges.append(Challenge(self._get_challenge_id(), challenge_definition, student_id))
        return challenges
    
    def _generate_plays_per_round(self, number_of_students):
        for challenge in self._challenges:
            challenges = self._generate_for_all_players(challenge, number_of_students)
            round = challenge['orientation_round'] + 1
            add_plays = list(map(lambda c: Play('set_challenge', AddChallengePayload(c)), challenges))
            try:
                self._plays_per_round[round].extend(add_plays)
            except:
                self._plays_per_round[round] = add_plays
            remove_plays = list(map(lambda c: Play('remove_challenge', RemoveChallengePayload(c.get_id())), challenges))
            try:
                self._plays_per_round[round + 1].extend(remove_plays)
            except:
                self._plays_per_round[round + 1] = remove_plays
        for round in self._plays_per_round.keys():
            self._plays_per_round[round].append(Play('finish_turn', None))

    def play(self, states):
        if self._plays_per_round is None:
            self._plays_per_round = {}
            number_of_students = len(list(filter(lambda p: isinstance(p, Student), states[-1].players)))
            self._generate_plays_per_round(number_of_students)

        actual_round = states[-1].round
        return self._plays_per_round[actual_round].pop(0)
    
    def get_id(self):
        return self.player_id