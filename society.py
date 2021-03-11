from collections import Counter
from helpers import flatten


class Society:
    def __init__(self, voting_method, config):
        self.voting_method = voting_method
        self.voting_methods = {
            "plurality_voting": self.plurality_vote,
            "cumulative_voting": self.cumulative_vote,
            "approval_voting": self.approval_vote,
            "plurality_with_elimination_voting": self.plurality_with_elimination_vote,
            "borda_voting": self.borda_vote
        }
        self.config = {
            **config,
            "allow_duplicates": voting_method != "approval_voting",
            "person_can_decide_k": voting_method == "approval_voting",
            "ranking": voting_method == "borda_voting"
        }
        self.people = []

    def add_person(self, person) -> None:
        self.people.append(person)

    def get_voting_method(self):
        return self.voting_methods[self.voting_method]

    def request_vote(self, choices) -> int:
        votes = {person: person.vote(choices, **self.config)
                 for person in self.people}
        return self.calculate_result(votes)

    def calculate_result(self, votes) -> int:
        voting_method = self.get_voting_method()
        return voting_method(votes)

    def plurality_vote(self, votes) -> int:
        votes = votes.values()
        total_count = Counter(votes)
        outcome = self.get_most_common_vote(total_count)

        if len(outcome) > 1:
            return self.request_vote(outcome)

        return outcome[0]

    @staticmethod
    def get_most_common_vote(total_count) -> list:
        most_common = total_count.most_common(1)[0]
        all_most_common = [most_common[0]]
        for option in total_count.keys():
            if total_count[option] == most_common[1] and option != most_common[0]:
                all_most_common.append(option)

        return all_most_common

    def cumulative_vote(self, votes) -> int:
        votes = votes.values()
        votes = flatten(votes)
        total_count = Counter(votes)
        outcome = self.get_most_common_vote(total_count)

        if len(outcome) > 1:
            return self.request_vote(outcome)

        return outcome[0]

    def approval_vote(self, votes) -> int:
        votes = votes.values()
        votes = flatten(votes)
        total_count = Counter(votes)
        outcome = self.get_most_common_vote(total_count)

        if len(outcome) > 1:
            return self.request_vote(outcome)

        return outcome[0]

    def plurality_with_elimination_vote(self, votes) -> int:
        vote_values = flatten(votes.values())
        total_count = Counter(vote_values)

        if len(total_count) == 1:
            return next(iter(total_count))

        eliminated = self.get_least_common_vote(total_count)
        choices = list(total_count.keys())
        if len(eliminated) > 1:
            return self.request_vote(choices)
        elif len(eliminated) == 1:
            existing_votes = {key: val for key,
                              val in votes.items() if val != eliminated[0]}
            new_choices = choices.pop(choices.index(eliminated[0]))
            people_who_voted_eliminated = self.get_voters(votes, eliminated)
            new_votes = {person: person.vote(
                new_choices, **self.config) for person in people_who_voted_eliminated}
            votes = {**existing_votes, **new_votes}
            return self.plurality_with_elimination_vote(votes)

    @staticmethod
    def get_voters(votes, eliminated):
        people = []
        for person, vote in votes.items():
            if vote == eliminated:
                people.append(person)

        return people

    @staticmethod
    def get_least_common_vote(total_count) -> list:
        least_common = total_count.most_common()[-1]
        all_least_common = [least_common[0]]
        for option in total_count.keys():
            if total_count[option] == least_common[1] and option != least_common[0]:
                all_least_common.append(option)

        return all_least_common

    def borda_vote(self, votes) -> int:
        points = Counter({})
        for vote in votes.values():
            earned_points = len(vote) - 1
            for candidate in vote:
                if candidate in points:
                    points[candidate] += earned_points
                else:
                    points[candidate] = earned_points
                earned_points -= 1

        outcome = self.get_most_common_vote(points)

        if len(outcome) > 1:
            return self.request_vote(outcome)

        return outcome[0]
