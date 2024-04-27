import json

dictionaries = [
	"sa-ru-antonova",
	"sa-ru-kert",
	"sa-ru-kuruch",
]

result = dict()

for d in dictionaries:
	with open(f"dictionaries/{d}.dsl", encoding="utf-16") as f:
		letters = set()
		words = list()
		for line in f:
			line = line.rstrip()
			if line[0] not in "\t #":
				words.append(line.lower())
				letters = letters | set(line.lower())
	result[d] = {"Words": words, "Letters": list(sorted(letters))}

with open("dict_info.json", mode="w", encoding="utf-8") as f:
	json.dump(result, f, indent=4, ensure_ascii=False)
