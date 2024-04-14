from Person import Person
import matplotlib.pyplot as plt
import networkx as nx

import random


class Simulation:
    def __init__(self, min_friends=3, max_friends=20, num_people=100, min_interactions=5, max_interactions=30):
        self.min_friends = min_friends
        self.max_friends = max_friends
        self.num_people = num_people

        self.min_interactions = min_interactions
        self.max_interactions = max_interactions

        self.people = [Person(random.randint(min_friends, max_friends), person) for person in range(num_people)]

        self.friendships = []

        # Create the like scores matrix
        self.like_scores = self.__calculate_like_scores()

    # Simulates a day of people meeting each other
    # Return - Number of new friendships made
    def simulate_day(self):
        num_new_friendships = 0
        leftover_people = []
        for person in range(self.num_people):
            if len(self.people[person].friends) < self.people[person].max_friends:
                leftover_people.append(person)

        random.shuffle(leftover_people)

        for person_idx in leftover_people:
            person = self.people[person_idx]
            # Skip this person if they've already met their max friends
            if len(person.friends) == person.max_friends:
                leftover_people.remove(person_idx)
                continue

            people_they_meet = random.sample(leftover_people, random.randint(min(self.min_interactions, len(leftover_people)),
                                                                             min(self.max_interactions, len(leftover_people))))
            # Loop through all people that they meet
            for friend_candidate_idx in people_they_meet:
                friend_candidate = self.people[friend_candidate_idx]

                # See if they like each other enough
                person_to_candidate_score = self.like_scores[person_idx][friend_candidate_idx]
                candidate_to_person_score = self.like_scores[friend_candidate_idx][person_idx]

                if person_to_candidate_score < person.friend_threshold:
                    continue

                if candidate_to_person_score < friend_candidate.friend_threshold:
                    continue

                # If we've made it here, they like each other enough to become friends
                person.friends.append(friend_candidate)
                friend_candidate.friends.append(person)

                self.friendships.append((person.id, friend_candidate.id))
                num_new_friendships += 1
                # TODO: We could add stuff here to boost the likelihood that a person either meets their friend's
                #    friends or that they end up liking them

        return num_new_friendships

    def __calculate_like_scores(self):
        # Initialize like score matrix
        like_scores = [[0 for _ in range(self.num_people)] for _ in range(self.num_people)]

        # Loop through every possible person_1 --> person_2 connection
        for person_1 in range(self.num_people):
            for person_2 in range(self.num_people):
                # A person will not become friends with themselves
                if person_1 == person_2:
                    continue

                # Get the actual Person objects
                person_1_obj = self.people[person_1]
                person_2_obj = self.people[person_2]

                # Start between 0 and 0.8 for how much person_1 likes person_2 (consider this the personality modifier)
                initial_score = random.random()

                # See how much person_1 prefers person_2's gender
                gender_modifier = person_1_obj.preferences["gender"][person_2_obj.characteristics["gender"]]

                # Subtract the age by 18 since the list index starts at 0
                age_modifier = person_1_obj.preferences["age"][person_2_obj.characteristics["age"] - 18]

                # See how much person_1 prefers person_2's race
                race_modifier = person_1_obj.preferences["race"][person_2_obj.characteristics["race"]]

                # See how much person_1 likes person_2's hobbies
                hobby_modifier = 0
                for hobby in person_2_obj.characteristics["hobbies"]:
                    hobby_modifier += person_1_obj.preferences["hobbies"][hobby]

                # The total score is the sum of the initial and all the modifiers
                total_like_score = initial_score + gender_modifier + age_modifier + race_modifier + hobby_modifier
                like_scores[person_1][person_2] = total_like_score

        return like_scores

    def visualize_curr_friendships(self):
        friendship_graph = nx.Graph()

        friendship_graph.add_edges_from(self.friendships)

        nx.draw(friendship_graph)
        plt.show()


if __name__ == "__main__":
    sim = Simulation(num_people=20)
    for day in range(100):
        new_friends = sim.simulate_day()
        print(f"Simulated day {day}. {new_friends} new friendships made")
        # for person in sim.people:
        #     print(f'\tD{day} person {person.id}: has num friends {len(person.friends)}')

    sim.visualize_curr_friendships()
