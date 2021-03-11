"""
Voting methods:
    - Plurality Voting: plurality_voting
    Each voter casts a single vote. The candidate with the most votes is selected.

    - Cumulative Voting: cumulative_voting
    Each voter is given k votes, which can be
    cast arbitrarily (e.g., several votes could be cast for one candidate, with the remainder
    of the votes being distributed across other candidates). The candidate with the
    most votes is selected.

    - Approval Voting: approval_voting
    Each voter can cast a single vote for as many
    of the candidates as he wishes; the candidate with the most votes is selected.

    - Plurality With Elimination Voting: plurality_with_elimination_voting
    Each voter casts a single vote for their most-preferred candidate.
    The candidate with the fewest votes is eliminated.
    Each voter who cast a vote for the eliminated candidate casts a new vote for the
    candidate he most prefers among the candidates that have not been eliminated.
    This process is repeated until only one candidate remains.

    - Borda Voting: borda_voting
    Each voter submits a full ordering on the candidates.
    This ordering contributes points to each candidate; if there are n candidates,
    it contributes n−1 points to the highest ranked candidate, n−2 points to the second
    highest, and so on; it contributes no points to the lowest ranked candidate. The
    winners are those whose total sum of points from all the voters is maximal.
"""

from society import Society
from person import Person

VOTING_SYSTEMS = {
    'plurality_voting': {},
    'cumulative_voting': {"k": 3},
    'approval_voting': {},
    'plurality_with_elimination_voting': {},
    'borda_voting': {},
}

for voting_system, config in VOTING_SYSTEMS.items():
    society = Society(voting_system, config)

    for _ in range(3):
        society.add_person(Person())
    outcome = society.request_vote([0, 1, 2])
