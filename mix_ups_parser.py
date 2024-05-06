import json
with open('klever_dict.json', encoding='utf8') as f:
    dict_words = json.load(f)
    dict_words = dict_words.keys()

# считываю mix_ups/groups.json
# считываю mix_ups.csv
mix_ups = [
    (["э"], ["ы"]),
    (["н", "ҍ"], ["н", "ь"]),
    (["д", "т"], ["д"])
]

def __results_of_mixup(input_word: str, mix_up: tuple[list, list]) -> list[str]:
    list_of_mistakes = []
    length = len(mix_up[1])
    for index in range (len(input_word)):
        is_match = True
        for mix_up_index in range (length):
            if (index+mix_up_index)>=len(input_word) or input_word[index + mix_up_index] != mix_up[1][mix_up_index]:
                is_match = False
                break
        if not is_match:
            continue
        prefix = input_word[:index]
        suffix = input_word[index+length:]
        new_word = prefix + "".join(mix_up[0]) + suffix
        list_of_mistakes.append(new_word)
    return list_of_mistakes

def possible_words_from_input_word(input_word):
    list_of_possible_words = []
    for dict_word in dict_words:
        if input_word in dict_word:
            list_of_possible_words.append(dict_word)
    return list_of_possible_words

if __name__ == "__main__":
    print(__results_of_mixup("адыньны", mix_ups[0]))
    print(possible_words_from_input_word("хозь"))