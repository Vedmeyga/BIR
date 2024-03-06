import os
from nltk import word_tokenize
from bs4 import BeautifulSoup

new_index_file = 'inverted_index.txt'
lemmas_file = '../Task2/lemmas.txt'
html_dir = '../Task1/html'


# Получаем словарь лемм и токенов
def get_lemmas_from_file(file_path):
    lemmas_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            lemma, tokens_str = line.strip().split(': ')
            tokens = tokens_str.split()
            for token in tokens:
                lemmas_dict[token] = lemma
    return lemmas_dict


# Создаем обратный индекс из HTML-файлов
def create_inverted_html_index(html_files_dir, lemmas_dir):
    index = {}
    for page_i in range(1, 101):
        file_path = os.path.join(html_files_dir, f'{page_i}.html')
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            text = soup.get_text()
            words = [token.lower() for token in word_tokenize(text)]
            for word in words:
                lemma = lemmas_dir.get(word)
                if lemma:
                    if lemma not in index:
                        index[lemma] = set()
                    if page_i not in index[lemma]:
                        index[lemma].add(page_i)

    return index


# Записываем индекс в файл
def write_index_to_file(index, index_file_name):
    with open(index_file_name, 'w', encoding='utf-8') as file:
        for key, value in index.items():
            line = key + ', ' + str(value)[1:-1] + '\n'
            file.write(line)


# Создаем файл с индексом
def build_index(index_file_name, html_dir, lemma_file_name):
    lemmas_dir = get_lemmas_from_file(lemma_file_name)
    index = create_inverted_html_index(html_dir, lemmas_dir)
    write_index_to_file(index, index_file_name)


def main():
    build_index(new_index_file, html_dir, lemmas_file)

if __name__ == "__main__":
    main()