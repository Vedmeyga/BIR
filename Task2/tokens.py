import os
import re
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pymorphy3

nltk.download('punkt')
nltk.download('stopwords')

# Объект для лемматизации
morph = pymorphy3.MorphAnalyzer()


# Обрабатываем html-файл для извлечения токенов
def get_tokens_from_html(file_path, tokens_set, lemmas_dict):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        # Извлекаем текст
        text = soup.get_text()
        # Токенизация
        tokens = word_tokenize(text)
        # Лемматизация токенов
        for token in tokens:
            token = token.lower()
            if check_token(token):
                tokens_set.add(token)
                lemma = morph.parse(token)[0].normal_form
                if lemma not in lemmas_dict:
                    lemmas_dict[lemma] = set()
                lemmas_dict[lemma].add(token)


# Фильтруем токены, оставляя только русские слова за исключением стоп-слов
def check_token(token):
    return (token.isalpha()
            and re.compile('[а-яА-ЯёЁ]+').fullmatch(token)
            and token not in stopwords.words('russian')
            and len(token) > 2)


# Структуры данных для записи
tokens_set = set()
lemmas_dict = {}

# Директория html-файлов
html_dir = '../Task1/html'

# Обрабатываем html-файлы из директории и получаем токены
for file_name in os.listdir(html_dir):
    if file_name.endswith('.html'):
        file_path = os.path.join(html_dir, file_name)
        get_tokens_from_html(file_path, tokens_set, lemmas_dict)

# Записываем токены в файл
with open('tokens.txt', 'w', encoding='utf-8') as tokens_file:
    for token in tokens_set:
        tokens_file.write(token + '\n')

# Записывем леммы в файл
with open('lemmas.txt', 'w', encoding='utf-8') as lemmas_file:
    for lemma, tokens in lemmas_dict.items():
        lemmas_file.write(lemma + ': ' + ' '.join(tokens) + '\n')