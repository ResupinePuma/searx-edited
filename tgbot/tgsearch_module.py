#Остановился на проблеме поиска последнего поста и проверки, есть ли содержимое на странице#
# Реализовано: работа через мой прокси (если в бане, ввод с клавиатуры), взятие списка каналов по ссылке с каталога),
#вытаскивание названия, преобразовывание в t.me/, решаю проблему поиска максимального поста

import requests
import socks    # для прокси
import socket   # для прокси
from bs4 import BeautifulSoup  # парсер

def get_html(url):
    response = requests.get(url)
    return response.text


def get_text(string):  # получаем текст поста (аргумент -- строка с мета из ассива content_text[5])
    s = string.replace('<meta content="','')
    s = s.replace('" property="og:description"/>', '')
    return s


def get_text_from_post(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    content_text = soup.find_all('meta')
    t = get_text(str(content_text[5]))
    return t

def get_channel_links(url): # получаю ссылки на каналы телеграм, сразу с t.me/
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    h3s = soup.find('div', class_='channel-cards-container').find_all('h3', class_='channel-card__title')
    links = []
    for h3 in h3s:
        a = h3.find('a').get('href')
        strCrop=a[len('https://tlgrm.ru/channels/@'):len(a)]
        strNew='https://t.me/'+strCrop+'/'
        links.append(strNew)
        print(strNew)
    return links

def search_last(channel, number, delta, channel_description):    # сам алгоритм поиска последнего поста
    delta = delta // 2
    if delta < 10:
        while get_text_from_post(channel+str(number)) != channel_description
            new_number
        return number
    elif get_text_from_post(channel+str(number))== channel_description:
        new_number = number - delta
        search_last(channel, new_number, delta, channel_description)
    else:    # указывает на то, что пост есть
        new_number=number+delta
        search_last(channel, new_number, delta, channel_description)



def define_last_post(channel):   # определяем последний пост
    channel_description = get_text_from_post(channel)   # описание канала
    max = 20000
    last = search_last(channel, max, max, channel_description)
    return last


def start_proxy(addr, port, username, password):
    socks.set_default_proxy(socks.HTTP, addr=addr, port=port, username=username, password=password)
    socket.socket = socks.socksocket
    try:    # проверяю, если запрос успешен, то работаем дальше, а, если нет, то меняем прокси до тех пор, пока не найдем рабочий
        html = get_html('https://t.me/')
    except:
        print('Указанный прокси в бане, нужно менять прокси')
        addr=str(input('Введите ip: '))
        port=int(input('Введите порт: '))
        socks.set_default_proxy(socks.HTTP, addr=addr, port=port, username='None', password='None')
        socket.socket = socks.socksocket


def main():

    url = 'https://tlgrm.ru/channels/news' #каталог новостных каналов Телеграм

    start_proxy(addr, port, username, password) #поднимаем единый прокси для всех запросов

    channels = get_channel_links(url)    #получить первые 25 каналов по ссылке из каталога каналов

    for channel in channels:
        if channel!='https://t.me//':
          try:
              get_html(channel)   #проверяю, все ли в порядке с каналом, иначе переход к следующему
              print('Захожу на: '+channel + ' и начинаю перебирать посты с начала с шагом 10...')
              define_last_post(channel)

          except:
              print('Ошибка при получении канала! Перехожу к следующему')





if __name__ == '__main__':
    main()