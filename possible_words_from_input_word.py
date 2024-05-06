import json

def possible_words_from_input_word (input_word):
    with open('klever_dict.json', encoding='utf8') as f:
        dict_words = json.load(f)
    list_of_possible_words = []
    for dict_word in dict_words:
        if input_word in dict_word:
            list_of_possible_words.append(dict_word)
    return (list_of_possible_words)

print (possible_words_from_input_word ("хозь"))