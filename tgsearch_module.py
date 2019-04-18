#Остановился на проблеме поиска последнего поста и проверки, есть ли содержимое на странице#
# Реализовано: работа через мой прокси (если в бане, ввод с клавиатуры), взятие списка каналов по ссылке с каталога),
#вытаскивание названия, преобразовывание в t.me/, решаю проблему поиска максимального поста

import requests
import socks    # для прокси
import socket   # для прокси
from bs4 import BeautifulSoup  #парсер

def get_html(url):
    response = requests.get(url)
    return response.text

def get_posts_html(url):
    max=find_max_post(url, 10000)

    return

def find_max_post(url, number):
    if check_post(url+str(number)):
        find_max_post(url, str(number + (number // 2)))

    else:
        find_max_post(url,str(number-(number//2)))



def check_post(url): #есть ли текст в посте? Да или нет
    response = requests.get(url + str(max))
    soup = BeautifulSoup(response, 'lxml')
    content_text = soup.find('div', class_='tgme_widget_message_text').get_text()
    print(content_text)
    if content_text != 'none':
        return True
    else:
        return False


def get_channel_links(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    h3s=soup.find('div', class_='channel-cards-container').find_all('h3', class_='channel-card__title')
    links = []
    for h3 in h3s:
        a = h3.find('a').get('href')
        strCrop=a[len('https://tlgrm.ru/channels/@'):len(a)]
        strNew='https://t.me/'+strCrop+'/'
        links.append(strNew)
        print(strNew)
    return links

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
        if channel=='t.me/':

        try:
            get_html(channel)   #проверяю, все ли в порядке с каналом, иначе переход к следующему
            print('Захожу на: '+channel + 'и начинаю перебирать посты с начала с шагом 10...')
            get_posts_html(channel)

        except:
            print('Ошибка при получении канала! Перехожу к следующему')





if __name__ == '__main__':
    main()