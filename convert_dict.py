import json
import re

dict_words = {}
list_of_dictionaries = ["dictionaries/sa-ru-antonova.dsl", "dictionaries/sa-ru-kert.dsl", "dictionaries/sa-ru-kuruch.dsl"]
for dictionary in list_of_dictionaries:
    with open(dictionary, "r", encoding='utf-16') as f:
        source_data = dictionary
        header = None
        contents = ""
        for line in f:
            if line[0] not in '\t #':
                if header:
                    dict_data = {
                        "contents": contents,
                        "source": dictionary
                    }
                    dict_words[header].append(dict_data)
                    contents = ''
                header = (line.replace('\n', '')).lower()
                header = re.sub(r' \d+$', '', header)
                header = re.sub(r' [ivx]+$', '', header)
                dict_words.setdefault(header, [])
            elif line[0] in '\t ':
                contents += line
with open ("klever_dict.json", "w", encoding='utf-8') as f:
    json.dump(dict_words, f, indent = '\t', ensure_ascii=False)
