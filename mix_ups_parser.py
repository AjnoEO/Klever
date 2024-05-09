import json

MAX_WEIGHT = 5

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

#для тестировки можно использовать test_dict_keys с посылкой "адынд"
test_dict_keys = ["адынд", "адындт", "адэнд", "адтэндт", "эдтынд", "адтынд", "адтындт" ]

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

def apply_mixups(input_word: str, weight: int=0) -> dict[str, int]:
    main_dict = {}
    if input_word in dict_words:
        main_dict[input_word] = weight
    if weight > MAX_WEIGHT:
        return main_dict
    for mix_up in mix_ups:
        list_of_mistakes = __results_of_mixup(input_word, mix_up)
        for mistaken_word in list_of_mistakes:
            aux_dict = apply_mixups(mistaken_word, weight+1)
            main_dict = aux_dict | main_dict
    return main_dict

def possible_words_from_input_word(input_word):
    main_dict = apply_mixups(input_word)
    sorted_main_dict = dict(sorted(main_dict.items(), key = lambda x:(x[1], x[0])))
    list_of_possible_words = list(sorted_main_dict.keys())
    return list_of_possible_words

if __name__ == "__main__":
    print (possible_words_from_input_word(input()))