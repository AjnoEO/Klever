import json

MAX_WEIGHT = 5

with open('klever_dict.json', encoding='utf8') as f:
    dict_words = json.load(f)
    dict_words = dict_words.keys()

groups = {
	"гласный": [
		"а",
		"э",
		"я",
		"е",
		"ӓ",
		"ӭ",
		"ы",
        "о",
        "и"
	],
	"согласный": [
		"п",
		"б",
		"м",
		"т",
		"д",
		"н"
	],
	"парный по звонкости": [
		{
			"глухой": "п",
			"звонкий": "б"
		},
		{
			"глухой": "т",
			"звонкий": "д"
		}
	],
	"тройственный по йотированности": [
		{
			"не йотированный": "а",
			"полуйотированный": "ӓ",
			"йотированный": "я"
		},
		{
			"не йотированный": "э",
			"полуйотированный": "ӭ",
			"йотированный": "е"
		}
	],
	"знак": [
		"ъ",
		"ь",
		"ҍ"
	]
}

class Slot:
    def __init__(self, type: str, id: int|None = None):
        self.type = type
        self.id = id

    def check_letter(self, letter):
        if letter in groups[self.type]:
            return True
        else: 
            return False
        
    def segment_alternations(self):
        
        return group
# считываю mix_ups/groups.json
# считываю mix_ups.csv
mix_ups = [
    (["э"], ["ы"]),
    (["н", "ҍ"], ["н", "ь"]),
    (["д", "т"], ["д"]),
    (["ы"], [Slot("гласный")]),
    ([Slot("гласный")], ["ы"])
    #([согласный 1][1],[1])

]

#для тестировки можно использовать test_dict_keys с посылкой "адынд"
test_dict_keys = ["адынд", "адындт", "адэнд", "адтэндт", "эдтынд", "адтынд", "адтындт" ]

def __generate_possible_cores(segment_list) -> list[str]:
    possible_cores = []
    if segment_list == []:
        return [""]
    aux_list = __generate_possible_cores (possible_cores[1:])
    

print (__generate_possible_cores())

def __results_of_mixup(input_word: str, mix_up: tuple[list, list]) -> list[str]:
    list_of_mistakes = []
    length = len(mix_up[1])
    for index in range (len(input_word)):
        is_match = True
        for mix_up_index in range (length):
            if (index+mix_up_index)>=len(input_word) or \
                isinstance(mix_up[1][mix_up_index], str) and input_word[index + mix_up_index] != mix_up[1][mix_up_index] or \
                isinstance(mix_up[1][mix_up_index], Slot) and  not mix_up[1][mix_up_index].check_letter(input_word[index + mix_up_index]):
                    is_match = False
                    break
        if not is_match:
            continue
        prefix = input_word[:index]
        suffix = input_word[index+length:]
        possible_cores = __generate_possible_cores(mix_up[0])
        for core in possible_cores:    
            new_word = prefix + core + suffix
            list_of_mistakes.append(new_word)
    return list_of_mistakes

def __apply_mixups(input_word: str, weight: int=0) -> dict[str, int]:
    main_dict = {}
    if input_word in dict_words:
        main_dict[input_word] = weight
    if weight > MAX_WEIGHT:
        return main_dict
    for mix_up in mix_ups:
        list_of_mistakes = __results_of_mixup(input_word, mix_up)
        for mistaken_word in list_of_mistakes:
            aux_dict = __apply_mixups(mistaken_word, weight+1)
            main_dict = aux_dict | main_dict
    return main_dict

def possible_words_from_input_word(input_word):
    main_dict = __apply_mixups(input_word)
    sorted_main_dict = dict(sorted(main_dict.items(), key = lambda x:(x[1], x[0])))
    list_of_possible_words = list(sorted_main_dict.keys())
    return list_of_possible_words

if __name__ == "__main__":
    print (possible_words_from_input_word(input()))