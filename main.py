import json

with open("converted_dict.json", encoding="utf-8") as f:
	full_dict = json.load(f)

def format_contents(contents: str) -> str: # форматировать содержание словарной статьи
	content_lines: list[str] = contents.split("\n")
	if content_lines[-1] == "": content_lines.pop() 
	content_lines = list(map(lambda s: s.lstrip(), content_lines))
	return "\n".join(content_lines)

def article_display(article: dict[str]) -> str: # отображение словарной статьи с источником
	assert set(article.keys()) == {"contents", "source"}, ValueError(f"Невалидная словарная статья: {article}")
	contents, source = article["contents"], article["source"]
	return format_contents(contents) + "\n    ~ " + source

text = input()
if text in full_dict:
	for article in full_dict[text]:
		print(article_display(article))
else:
	print(f"Нет результатов для слова «{text}»")