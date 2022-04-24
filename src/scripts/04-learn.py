import sys
sys.path.append("../modules/spaced_learning")
from modules.spaced_learning.review_manager import ReviewManager
rm = None
card_dict = {}

def build_new_cards_if_there_is():
    # If new data are added to tsv file
    # Firstly, load log
    global rm
    # Global card_dict
    global card_dict
    # Secondly, load tsv list
    with open(f'../../data/tsv/to_learn.tsv', 'r', encoding='utf8') as f:
        vocabulary_list = f.read().split('\n')
        vocabulary_list = [c.split('\t') for c in vocabulary_list]
        vocabulary_list = [c for c in vocabulary_list if len(c) == 3]
        print(f'{len(vocabulary_list)} vocabularies fetched from tsv file')
    card_name_list = [v[1] for v in vocabulary_list]
    card_dict = {v[1]:(v[0],v[2]) for v in vocabulary_list}

    added = 0
    for card_name in card_name_list:
        if not rm.card_by_name(card_name):
            rm.new_card(card_name)
            added += 1

    rm.flush()
    print(f'{added} cards added')

if __name__ == '__main__':
    rm = ReviewManager("../../data/review.log")
    build_new_cards_if_there_is()
    rm.add_review_list(card_dict.keys())

    # Fetch stat
    # Late/Advanced
    total = len(rm.card_list())
    late = len(rm.late_list())
    print(f'{late} / {total} to be reviewed')

    # Fetch next review
    counter = 0
    while True:
        next_review_name = rm.next_review()
        if next_review_name is None:
            break

        # print('\033[H')
        print(f'{next_review_name} : {card_dict[next_review_name][0]}')
        i = input('a/e/h ').lower()
        if i == 'a':
            print(card_dict[next_review_name][1])
            i = input('e/h ')

        if i == 'e' or i == 'h':
            r = 1 if i == 'e' else -1
            rm.reschedule(next_review_name, r)
        elif i == 'q':
            print("Good Bye")
            break
        else:
            print('Should type A, E or H, Q')
            continue

        counter += 1
        rm.flush()
    rm.flush()