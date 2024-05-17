"""Разбирается в путаницах"""

import json
import csv
import re
from convert_dict import convert

MAX_WEIGHT = 4

list_of_dictionaries = [
    "dictionaries/sa-ru-antonova.dsl",
    "dictionaries/sa-ru-kert.dsl",
    "dictionaries/sa-ru-kuruch.dsl",
]
convert(list_of_dictionaries)

with open("klever_dict.json", encoding="utf8") as f:
    dict_words = json.load(f)
    dict_words = set(dict_words.keys())

with open('mix_ups/groups.json', encoding='utf8') as f:
    groups = json.load(f)
    for type_gr in groups:
        if isinstance(groups[type_gr][0], str):
            groups[type_gr] = set(groups[type_gr])

with open('mix_ups/banned_sequences.json', encoding='utf8') as f:
    banned_sequences = json.load(f)
    NO_DOUBLE = banned_sequences["Не удваивать"]
    if NO_DOUBLE == -1:
        NO_DOUBLE = r"."
    NO_TRIPLE = banned_sequences["Не утраивать"]
    if NO_TRIPLE == -1:
        NO_TRIPLE = r"."

class Slot:
    """класс для слотов в путаницах"""
    def __init__(self, letter_type: str, segment_id: int | None = None, feature: str | None = None):
        self.type = letter_type
        self.id = segment_id
        self.feature = feature

    def check_letter(self, letter):
        """проверка буквы на соответствие группе по типу"""
        if self.feature is None:
            return letter in groups[self.type]
        for feature_dict in groups[self.type]:
            if feature_dict[self.feature] == letter:
                return True
        return False

    def segment_alternation(self):
        """получаем список букв внутри группы"""
        list_of_segments = groups[self.type]
        if isinstance(list_of_segments, list):
            aux_set = set()
            for segment_dict in list_of_segments:
                for segment in segment_dict.values():
                    aux_set.add(segment)
            list_of_segments = list(aux_set)
        if (self.id is not None) and (self.feature is not None):
            list_of_segments = [global_mixup_dict[self.id][self.feature]]
        elif self.id is not None:
            list_of_segments = [global_mixup_dict[self.id]]
        return list_of_segments

    def __repr__(self) -> str:
        return "Slot(" + str(self.type) + ")"

mix_ups = []

def __mixup_parser(string):
    list_str = []
    while string != "":
        if string[0] != "[":
            list_str.append(string[0])
            string = string[1:]
        elif type_feature_string:= re.match(r"^\[([^\]]*?) (\d) : ([^\]]*?)\]", string):
            type_str, id_str, feature_str = type_feature_string.groups()
            list_str.append(Slot(type_str, id_str, feature_str))
            x = len(type_feature_string.group())
            string = string[x:]
        elif type_feature_string:= re.match(r"^\[([^\]]*?) (\d)\]", string):
            type_str, id_str = type_feature_string.groups()
            list_str.append(Slot(type_str, id_str))
            x = len(type_feature_string.group())
            string = string[x:]
        elif type_feature_string:= re.match(r"^\[([^\]]*?)\]", string):
            type_str = type_feature_string.group(1)
            list_str.append(Slot(type_str))
            x = len(type_feature_string.group())
            string = string[x:]
    return list_str

with open('mix_ups/mix_ups.csv', encoding='utf8', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row_dict in reader:
        left_part = row_dict["Реальный"]
        right_part = row_dict["Ложный"]
        final_tuple = (__mixup_parser(left_part), __mixup_parser(right_part))
        mix_ups.append(final_tuple)
        if row_dict["Обратимо"] == "да":
            final_tuple = (__mixup_parser(right_part), __mixup_parser(left_part))
            mix_ups.append(final_tuple)

def __generate_possible_cores(segment_list: list[str | Slot]) -> list[str]:
    # итоговый список ядер
    possible_cores = []
    if segment_list == []:
        return [""]
    possible_second_parts = __generate_possible_cores(segment_list[1:])
    if isinstance(segment_list[0], Slot):
        possible_first_parts = segment_list[0].segment_alternation()
    elif isinstance(segment_list[0], str):
        possible_first_parts = [segment_list[0]]
    for first_part in possible_first_parts:
        for second_part in possible_second_parts:
            possible_core = first_part + second_part
            possible_cores.append(possible_core)
    return possible_cores


global_mixup_dict = {}


def __results_of_mixup(input_word: str, mix_up: tuple[list, list]) -> list[str]:
    list_of_mistakes = []
    length = len(mix_up[1])
    for index in range(len(input_word)):
        global_mixup_dict.clear()
        is_match = True
        for mix_up_index in range(length):
            if (index + mix_up_index) >= len(input_word):
                is_match = False
                break
            current_letter = input_word[index + mix_up_index]
            current_segment = mix_up[1][mix_up_index]
            if (
                isinstance(current_segment, str)
                and current_letter != current_segment
                or isinstance(current_segment, Slot)
                and not current_segment.check_letter(current_letter)
            ):
                is_match = False
                break
            if isinstance(current_segment, Slot) and current_segment.id is not None:
                if current_segment.feature is not None:
                    if current_segment.id not in global_mixup_dict:
                        for feat_type_dict in groups[current_segment.type]:
                            if feat_type_dict[current_segment.feature] == current_letter:
                                global_mixup_dict[current_segment.id] = feat_type_dict
                    elif global_mixup_dict[current_segment.id] != feat_type_dict:
                        is_match = False
                        break
                elif current_segment.id not in global_mixup_dict:
                    global_mixup_dict[current_segment.id] = current_letter
                elif current_letter != global_mixup_dict[current_segment.id]:
                    is_match = False
                    break
        if not is_match:
            continue
        prefix = input_word[:index]
        suffix = input_word[index + length :]
        possible_cores = __generate_possible_cores(mix_up[0])
        for core in possible_cores:
            new_word = prefix + core + suffix
            list_of_mistakes.append(new_word)
    return list_of_mistakes

checked_words_dict = {} # словарь проверенных строк и веса, с которыми они были проверены

def __apply_mixups(input_word: str, weight: int = 0) -> dict[str, int]:
    if weight == 0:
        checked_words_dict.clear()
    if input_word in checked_words_dict and weight >= checked_words_dict[input_word]:
        return {}
    checked_words_dict[input_word] = weight
    if re.search(r"(" + NO_DOUBLE + r")\1", input_word):
        return {}
    if re.search(r"(" + NO_TRIPLE + r")\1\1", input_word):
        return {}
    main_dict = {}
    if input_word in dict_words:
        main_dict[input_word] = weight
    if weight > MAX_WEIGHT:
        return main_dict
    for mix_up in mix_ups:
        list_of_mistakes = __results_of_mixup(input_word, mix_up)
        for mistaken_word in list_of_mistakes:
            aux_dict = __apply_mixups(mistaken_word, weight + 1)
            main_dict = aux_dict | main_dict
    return main_dict


def possible_words_from_input_word(input_word):
    """ Возвращает список потенциально искомых слов из словарей"""
    main_dict = __apply_mixups(input_word)
    sorted_main_dict = dict(sorted(main_dict.items(), key=lambda x: (x[1], x[0])))
    list_of_possible_words = list(sorted_main_dict.keys())
    return list_of_possible_words


if __name__ == "__main__":
    print(__apply_mixups(input()))
