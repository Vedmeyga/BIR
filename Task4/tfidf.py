import math
import os
import re

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pymorphy3 import MorphAnalyzer

nltk.download('punkt')
nltk.download('stopwords')

morph = MorphAnalyzer()

html_dir = '../Task1/html'
inverted_index_file = '../Task3/inverted_index.txt'
tfidf_tokens_dir = 'tfidf_tokens/'
tfidf_lemmas_dir = 'tfidf_lemmas/'

files = os.listdir(html_dir)

# Получаем инвертированный индекс токенов
def get_inverted_index_tokens(html_dir):
    index = {}
    for i, filename in enumerate(files):
        with open(os.path.join(html_dir, filename), 'r', encoding='utf-8') as file:
            text = file.read()
            tokens = tokenize(text, True)
            for token in tokens:
                if token in index:
                    index[token].add(i)
                else:
                    index[token] = {i}
    return index


# Извлекаем токены из списка
def get_tokens(tokens, is_set):
    result = []
    for token in tokens:
        if token.lower() not in stopwords.words("russian") and re.compile("[а-яА-ЯёЁ]+").match(token.lower()):
            result.append(token.lower())
    if is_set:
        return list(result)
    else:
        return list(result)


# Получаем токены из текста
def tokenize(text, is_set):
    tokens = word_tokenize(text.replace('.', ' '))
    return get_tokens(tokens, is_set)


def read_lemmas():
    lemmas = {}
    with open(inverted_index_file, 'r', encoding='utf-8') as file:
        for line in file:
            data = re.split(', ', line)
            token = data[0]
            pages = set()
            for i in range(1, len(data)):
                pages.add(int(data[i]))
            lemmas[token] = pages
    return lemmas


# Вычисляем tf
def get_tf(q, tokens):
    return tokens.count(q) / float(len(tokens))


# Вычисляем idf
def get_idf(q, index):
    return math.log(len(files) / float(len(index[q])))


# Вычисляем tf и idf токенов и лемм и записываем их в файлы
def get_tfidf(html_dir, tokens_index, lemmas_index):

    for filename in files:
        with open(os.path.join(html_dir, filename), 'r', encoding='utf-8') as file:
            text = file.read()
            tokens = tokenize(text, False)
            lemmas = list(map(lambda word: morph.parse(word.replace("\n", ""))[0].normal_form, tokens))

            result_tokens = []
            for token in set(tokens):
                if token in tokens_index:
                    tf = get_tf(token, tokens)
                    idf = get_idf(token, tokens_index)
                    result_tokens.append(f"{token} {idf} {tf * idf}")

            with open(f"{tfidf_tokens_dir}{filename.replace('.html', '')}.txt", "w", encoding='utf-8') as token_file:
                token_file.write("\n".join(result_tokens) + ',')

            result_lemmas = []
            for lemma in set(lemmas):
                if lemma in lemmas_index:
                    tf = get_tf(lemma, lemmas)
                    idf = get_idf(lemma, lemmas_index)
                    result_lemmas.append(f"{lemma} {idf} {tf * idf}")

            with open(f"{tfidf_lemmas_dir}{filename.replace('.html', '')}.txt", "w", encoding='utf-8') as lemma_file:
                lemma_file.write("\n".join(result_lemmas))


def main():
    inverted_index_tokens = get_inverted_index_tokens(html_dir)
    lemmas_index = read_lemmas()
    get_tfidf(html_dir, inverted_index_tokens, lemmas_index)


if __name__ == '__main__':
    main()
