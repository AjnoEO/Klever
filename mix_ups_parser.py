# считываю json
# считываю csv
#with open...
    
#скрытая функция: принимает строчку и константу, ограничиваем количество итераций
# кортеж из слова+вес_ош, если слово существует, если нет, всё равно применяем функцию
#groups = [в желаемом виде]
mix_ups = [
    (["э"], ["ы"]),
    (["н", "ҍ"], ["н", "ь"]),
    (["д", "т"], ["д"])
]

def results_of_mixup (input_word: str, mix_up: tuple[list, list]):
    wrong_str = ''
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
    return (list_of_mistakes)
print (results_of_mixup("адыньны", mix_ups[0]))