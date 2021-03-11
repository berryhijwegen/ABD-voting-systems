import random


class Person:
    """ 
    A person can vote, it doesn't know anything about the society and what voting system it uses.
    The society asks the people to vote their choice, with some parameters depending
    on the voting system. 
    """
    @staticmethod
    def generate_vote(choices, k, allow_duplicates, person_can_decide_k, ranking):
        if ranking:
            return random.sample(choices, k=len(choices))

        if person_can_decide_k:
            k = random.randint(1, len(choices))

        if k == 1:
            return random.choice(choices)

        if allow_duplicates:
            return random.choices(choices, k=k)

        return random.sample(choices, k=k)

    def vote(self, choices, k=1, allow_duplicates=True, person_can_decide_k=False, ranking=False):
        vote = self.generate_vote(
            choices, k, allow_duplicates, person_can_decide_k, ranking)
        return vote
