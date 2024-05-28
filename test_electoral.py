# test_electoral.@property
'''
A module to reproduce the results from the test electoral RTBF 2024

Module-level tests:

Get a Calculator with default question set (35 french questions)
>>> calc = Calculator()

Answer "agree" to all questions
>>> calc.set_answers('a' * 35)

See answers
>>> calc.answers
'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

Get ranked results
>>> calc.get_results(ranked=True)
{'MR': 66, 'Les Engagés': 66, 'Ecolo': 53, 'PTB': 48, 'PS': 48, 'Défi': 43}

Answer "disagree" to all questions
>>> calc.set_answers('d' * 35)

Get ranked results
>>> calc.get_results(ranked=True)
{'Défi': 57, 'PTB': 52, 'PS': 52, 'Ecolo': 47, 'MR': 30, 'Les Engagés': 29}

Change answer 5 (0-indexed), i.e. the 6th one in the list
to boosted 'Agree'. Note the capital 'A' to denote boosting
Note how changing one answer completely changes the rank of Défi
>>> calc.set_an_answer(5, 'A')
>>> calc.answers
'dddddAddddddddddddddddddddddddddddd'
>>> calc.get_results(ranked=True)
{'MR': 48, 'Les Engagés': 47, 'PTB': 38, 'PS': 37, 'Ecolo': 33, 'Défi': 33}

Answer 100% like a given party
>>> calc.answer_like('Ecolo')
>>> calc.get_results(ranked=True)
{'Ecolo': 100, 'PS': 84, 'PTB': 78, 'Défi': 68, 'Les Engagés': 40, 'MR': 24}

Answer like a random mixture of "left-wing" parties answers
>>> random.seed(111111)
>>> calc.answer_like(['Ecolo', 'PS', 'PTB'])
>>> calc.get_results(ranked=True)
{'PS': 92, 'Ecolo': 90, 'PTB': 85, 'Défi': 77, 'Les Engagés': 51, 'MR': 33}
'''

import json
import csv
import sys
import random
from collections import defaultdict, Counter

class Database:
    
    party_names = {
        'french': {
            "Défi",
            "Ecolo",
            "Les Engagés",
            "MR",
            "PS",
            "PTB"
        },
        'flemish': {
            "CD&V",
            "NVA",
            "Open VLD",
            "PVDA",
            "Vlaams Belang",
            "Vooruit",
            "Groen"
        }
    }

    def __init__(self,
                 database_file='data/database.json',
                 levels=['base'],
                 language='french'):
        self.parties = self.party_names[language]
        self.data = json.load(open(database_file, 'r')) 
        self.data = [q for q in self.data
                   if any(level in levels for level in q['level']) and 
                   q['partyOpinions'][0]['party']['name'] in self.parties]
        self.num_questions = len(self.data)

    def variable_to_csv(self, variable, file=None, add_statement=False):
        '''
        Extract a single variable from party opinions to csv
        in a wide data format, i.e.
        question,id,short,party1_value,party2_value,party3_value,...
        '''
        possible_variables = (
                'opinion',
                'weight',
                'description')
        assert variable in possible_variables, 'Unrecognized variable'
        fields = ['question', 'id', 'short']
        if add_statement:
            fields.append('statement')
        fields.extend(self.parties)
        csvout = open(file, 'w') if file is not None else sys.stdout
        writer = csv.DictWriter(csvout, fieldnames=fields)
        writer.writeheader()
        for (i, q) in enumerate(self.data, start=1):
            row_dict = {
                'question': 'Q' + str(i),
                'id': q['id'],
                'short': q['short']
            }
            if add_statement:
                row_dict['statement'] = q['statement']
            for po in q["partyOpinions"]:
                party_name = po['party']['name']
                row_dict[party_name] = po[variable]
            writer.writerow(row_dict)

    def variables_to_csv(self, variables, file=None, add_statement=False):
        '''
        Extract one/multiple variables from party opinions to csv
        in a tidy/long format, i.e.
        question,id,short,variable1_name,party1_name,value
        question,id,short,variable1_name,party2_name,value
        etc
        '''
        possible_variables = (
                'opinion',
                'weight',
                'description')
        assert all([variable in possible_variables for variable in variables]), "Unrecognized variable"
        fields = ['question', 'id', 'short']
        if add_statement:
            fields.append('statement')
        fields.append('variable')
        fields.append('party')
        fields.append('value')
        csvout = open(file, 'w') if file is not None else sys.stdout
        writer = csv.DictWriter(csvout, fieldnames=fields)
        writer.writeheader()
        for (i, q) in enumerate(self.data, start=1):
            for variable in variables:
                for po in q['partyOpinions']:
                    row_dict = {
                        'question': 'Q' + str(i),
                        'id': q['id'],
                        'short': q['short']
                    }
                    if add_statement:
                        row_dict['statement'] = q['statement']
                    row_dict['variable'] = variable
                    row_dict['party'] = po['party']['name']
                    row_dict['value'] = po[variable]
                    writer.writerow(row_dict)

    def get_party_answers(self, party, format='string'):
        '''
        Get the list of agree/disagree answers for a party
        format == 'string' -> 'adddadaadddadaddaa...'
        format == 'dict' -> { 'Q1': 'agree',... }
        '''
        s = ''
        d = {}
        for (i, q) in enumerate(self.data, start=1):
            for po in q['partyOpinions']:
                if po['party']['name'] == party:
                    opinion = po['opinion']
                    if format == 'string':
                        s += opinion[0]
                    elif format == 'dict':
                        question = 'Q' + str(i)
                        d[question] = opinion
        if format == 'string':
            return(s)
        elif format == 'dict':
            return(d)

    def get_party_weights(self, party, format='array'):
        '''
        Get the weights for a party
        format == 'array' -> [3.444, 2.675, 2.878,...]
        format == 'dict' -> { 'Q1': 3.444,... }
        '''
        a = []
        d = {}
        for (i, q) in enumerate(self.data, start=1):
            for po in q['partyOpinions']:
                if po['party']['name'] == party:
                    weight = po['weight']
                    if format == 'array':
                        a.append(weight)
                    elif format == 'dict':
                        question = 'Q' + str(i)
                        d[question] = weight
        if format == 'array':
            return(a)
        elif format == 'dict':
            return(d)

class Calculator:

    def __init__(self,
                 database_file='data/database.json',
                 levels=['base'],
                 language='french'):
        self.db = Database(database_file, levels, language)
        self.answers = None
        self.party_answers = { party: self.db.get_party_answers(party)
                              for party in self.db.parties }
        self.party_weights = { party: self.db.get_party_weights(party)
                              for party in self.db.parties }

    def set_answers(self, answers):
        '''
        Set the full list of answers
        answers: string like 'dadaDDdauaaddadddddAadaaaaaadadaada'
        that has length equal to the number of questions in db
        characters are one of "a", "A", "d", "D", "o", "O" with
        "a": agree, no boost,
        "A": agree, boost,
        "d": disagree, no boost,
        "D": disagree, boost
        "u": undecided, no boost
        "U": undecided, boost
        '''
        assert len(answers) == self.db.num_questions, 'Length not matching # questions in DB'
        assert set(answers).issubset( { 'a', 'A', 'd', 'D', 'u', 'U'}), 'Unrecognized character'
        self.answers = answers

    def set_an_answer(self, i, answer):
        '''
        Set the answer to a single question
        i is the position of the answer, 0-indexed
        answer is one of "a", "A", "d", "D", "o", "O" with
        "a": agree, no boost,
        "A": agree, boost,
        "d": disagree, no boost,
        "D": disagree, boost
        "u": undecided, no boost
        "U": undecided, boost
        '''
        assert self.answers is not None, 'You must use .set_answers() first'
        assert answer in ( 'a', 'A', 'd', 'D', 'u', 'U'), 'Unrecognized character'
        assert i  < self.db.num_questions, 'Index out of bounds'
        self.answers = self.answers[:i] + answer + self.answers[i+1:]

    def random_change_answer(self,
                                i,
                                can_be_undecided=False,
                                can_change_boost=True):
        '''
        Change an answer to one of the other possible answers
        i is the position of the answer, 0-indexed

        If can_be_undecided is False then only agree/disagree
        are possible answers

        If can_change_boost is True the answer is chosen from
        all the other possible answers

        If can_change_boost is False the answer is chosen from
        the possible answers with same boost status
        '''
        assert self.answers is not None, 'You must use .set_answers() first'
        assert i  < self.db.num_questions, 'Index out of bounds'
        c = self.answers[i]
        match (can_be_undecided, can_change_boost):
            case (True, True):
                possible = {'a', 'A', 'd', 'D', 'u', 'U'}.difference(c)
            case (False, True):
                possible = {'a', 'A', 'd', 'D'}.difference(c)
            case (True, False):
                match c:
                    case 'a' | 'd' | 'u':
                        possible = {'a', 'd', 'u'}.difference(c)
                    case 'A' | 'D' | 'U':
                        possible = {'A', 'D', 'U'}.difference(c)
            case (False, False):
                match c:
                    case 'a' | 'd' | 'u':
                        possible = {'a', 'd'}.difference(c)
                    case 'A' | 'D' | 'U':
                        possible = {'A', 'D'}.difference(c)
        c_new = random.choice(list(possible))
        self.answers = self.answers[:i] + c_new + self.answers[i+1:]

    def answer_like(self, party_or_parties):
        '''
        Answer the questionnaire exactly like a party's answers
        or like a random mixture of several parties' answers
        '''
        num_questions = self.db.num_questions
        if isinstance(party_or_parties, str):
            party = party_or_parties
            assert party in self.db.parties, 'Unrecognized party name'
            answers = self.party_answers[party]
        if isinstance(party_or_parties, list):
            parties = party_or_parties
            assert all(party in self.db.parties for party in parties), 'Unrecognized party name'
            answers = ''
            for i in range(num_questions):
                party = random.choice(parties)
                answer = self.party_answers[party][i]
                answers += answer
        self.answers = answers

    def get_results(self, rounded=True, ranked=False):
        '''
        Get the percentages for all parties
        '''
        assert self.answers is not None, 'You must use .set_answers() first'
        answers = self.answers
        num_questions = self.db.num_questions
        my_counts = Counter(answers)
        num_my_non_undecided_boosted = my_counts['A'] + my_counts['D']
        # Three dicts indexed by party
        num_matches = defaultdict(int)
        num_matches_boosted = defaultdict(int)
        sum_matches_weights = defaultdict(int)
        for party in self.db.parties:
            party_answers = self.party_answers[party]
            party_weights = self.party_weights[party]
            num_matches[party] = sum([ x.lower() == y
                                     for (x, y) in zip(answers, party_answers) ])
            num_matches_boosted[party] = sum([ x.lower() == y
                                             for (x, y) in zip(answers, party_answers)
                                             if x in ('A', 'D', 'U')])
            for i in range(num_questions):
                if answers[i].lower() == party_answers[i]:
                    sum_matches_weights[party] += party_weights[i]
        results = {}
        for party, total_weight in sum_matches_weights.items():
            party_boost = num_matches_boosted[party]
            if num_my_non_undecided_boosted > 0:
                percentage = ( total_weight + (( party_boost / num_my_non_undecided_boosted ) * 20)) / 1.2
            else:
                percentage = total_weight
            results[party] = round(percentage) if rounded else percentage
        if ranked:
            # N.B. We sort by value then by party name for ex-aequos
            results = dict(sorted(list(results.items()),
                                  key=lambda x: (x[1], x[0]),
                                  reverse=True))
        return results

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python test_electoral.py "adaDddAaddadDaDddaaDaddaaaaddAaddaa"')
    else:
        calc = Calculator()
        calc.set_answers(sys.argv[1])
        results = calc.get_results(ranked=True)
        print(results)
