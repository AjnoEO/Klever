"""Конвертировать словари в json нужного формата"""

import json
import re

def convert(list_of_dictionaries: list[dict]) -> None:
	"""Конвертирует словари в формат словаря Klever и сохраняет в klever_dict.json"""
	dict_words = {}
	for dictionary in list_of_dictionaries:
		with open(dictionary, "r", encoding='utf-16') as f:
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
