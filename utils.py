from typing import Callable

def apply_arguments(func: Callable, *inserted_args, **inserted_kwargs) -> Callable:
	"""Создаёт функцию, которая работает аналогично функции `func` но с применением аргументов, указанных следом

	:param func: Функция, на основании которой нужно создать новую функцию
	:type func: Callable
	:return: Функция, работающая аналогично старой, но с применением введённых аргументов
	:rtype: Callable
	"""
	def new_func(*args, **kwargs):
		func(*inserted_args, *args, **inserted_kwargs, **kwargs)
	return new_func