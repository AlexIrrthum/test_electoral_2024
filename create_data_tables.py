from test_electoral import Calculator, Database
from collections import Counter
import random

# change here for other levels or flemish
levels = ['base']
language = 'french'
db_type = '_'.join(levels) + '_' + language


# set seed to replicate analysis
random.seed(543210)

calc = Calculator(levels=levels, language=language)

num_questions = calc.db.num_questions

# create the answers matrix
filename = 'data/' + db_type + '_answers.csv'
calc.db.variable_to_csv('opinion', file=filename)

# create the weights matrix 
filename = 'data/' + db_type + '_weights.csv'
calc.db.variable_to_csv('weight', file=filename)

# create the party stability table
# 1. vote 100% like a party
# 2. change two answers at random
# 3. see if the party is still number one
# repeat 10000 times for each party
filename = 'data/' + db_type + '_party_stability.csv'
with open(filename, 'w') as f:
    print('from_party,to_party', file=f)
    num_changes = 2
    for from_party in calc.db.parties:
        for i in range(10000):
            calc.answer_like(from_party)
            steps = []
            for i in range(num_changes):
                j = random.randint(0, num_questions-1)
                calc.random_change_answer(j)
                steps.append(calc.answers)
            results = calc.get_results(ranked=True)
            to_party = list(results.keys())[0]
            print(','.join([from_party, to_party]), file=f)

# create the random answer winner party table
# generate a random vector of agree/disagree answers
# tabulate the winner
# repeat 10 x 10000 times
filename = 'data/' + db_type + '_random_winner.csv'
with open(filename, 'w') as f:
    print('party,fold,num_wins', file=f)
    for fold in range(10):
        win_counter = Counter()
        for i in range(10000):
            answers = ''.join(random.choices(['a', 'd'], k=num_questions))
            calc.set_answers(answers)
            results = calc.get_results(ranked=True)
            winner = list(results.keys())[0]
            win_counter[winner] += 1
        for party in win_counter:
            num_wins = win_counter[party]
            print(','.join([party, str(fold), str(num_wins)]), file=f)
        

