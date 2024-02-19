import requests
from bs4 import BeautifulSoup
import re
import os


# Получаем ссылки на странице
def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a', href=True)]
    return links


# Сохраняем html-файлы
def download_page(url, file_name):
    response = requests.get(url)
    folder_name = 'html'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    file_path = os.path.join(folder_name, file_name)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(response.text)


# Заполняем файл index ссылками на страницы
def write_to_file(num, url, file_name):
    with open(file_name, 'a', encoding='utf-8') as file:
        file.write(str(num) + '.html ' + ': ' + str(url) + '\n')


def main():
    base_url = 'https://azbyka.ru/otechnik/Sergej_Solovev/istorija-rossii-s-drevnejshih-vremen/'
    links = get_links(base_url)
    count = 1
    index_file = 'index.txt'
    for link in links:
        if re.match(r'./\d+_\d', link):
            if count < 101:
                link = base_url + link
                file_name = str(count) + '.html'
                download_page(link, file_name)
                write_to_file(count, link, index_file)
                count = count + 1
            else:
                break


if __name__ == "__main__":
    main()