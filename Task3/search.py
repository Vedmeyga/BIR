import json
import re
from pymorphy3 import MorphAnalyzer
from pyparsing import Word, Suppress, Group, Forward, srange, CaselessLiteral, ZeroOrMore


new_index_file = 'inverted_index.txt'

# Осуществляем поиск
def search(index, query):
    AND, OR, NOT = map(CaselessLiteral, ["AND", "OR", "NOT"])
    term = Word(srange("[а-яА-ЯёЁ]"))

    expr = Forward()
    atom = (NOT + term | term | NOT + Group(Suppress("(") + expr + Suppress(")")) | Group(
        Suppress("(") + expr + Suppress(")")))
    clause = Group(atom + ZeroOrMore(AND + atom | OR + atom))
    expr <<= clause

    morph = MorphAnalyzer()

    # Обрабатываем выражение для получения конечного результата
    def evaluate_query(query, index):
        if isinstance(query, str):
            token = morph.parse(query.lower())[0].normal_form
            return index.get(token)
        elif query[0] == "NOT":
            pages_with_word = evaluate_query(query[1], index)
            all_pages = set(range(1, 101))
            return list(all_pages - set(pages_with_word))
        else:
            result = evaluate_query(query[0], index)
            for operator, word in zip(query[1::2], query[2::2]):
                pages = evaluate_query(word, index)
                if operator == "AND":
                    result = list(set(result) & set(pages))
                elif operator == "OR":
                    result = list(set(result) | set(pages))
            return result

    parsed_query = expr.parseString(query)[0]
    return evaluate_query(parsed_query, index)


# Получаем индекс из созданного файла
def get_index_from_file(index_file_name):
    index = {}
    with open(index_file_name, 'r', encoding='utf-8') as file:
        for line in file:
            data = re.split(', ', line)
            token = data[0]
            pages = set()
            for i in range(1, len(data)):
                pages.add(int(data[i]))
            index[token] = pages

    return index

def main():
    index = get_index_from_file(new_index_file)

    while True:
        query = input("Введите запрос: ")
        results = search(index, query)
        if results:
            print("Совпадения найдены на страницах:", str(results)[1: -1])
        else:
            print("Совпадения не найдены")

if __name__ == "__main__":
    main()