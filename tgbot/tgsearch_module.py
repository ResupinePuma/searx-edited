#Остановился на проблеме поиска последнего поста и проверки, есть ли содержимое на странице#
# Реализовано: работа через мой прокси (если в бане, ввод с клавиатуры), взятие списка каналов по ссылке с каталога),
#вытаскивание названия, преобразовывание в t.me/, экспорт в .csv

import requests
import socks    # для прокси
import socket   # для прокси
import csv
from bs4 import BeautifulSoup  # парсер


def get_html(url):
    response = requests.get(url)
    return response.text


def get_text(string):  # получаем текст поста (аргумент -- строка с мета из ассива content_text[5])
    s = string.replace('<meta content="','')
    s = s.replace('" property="og:description"/>', '')
    return s


def get_text_from_post(url): # основная подпрограмма получения текста их поста, выше -- его подпрограмма
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

# надо поработать над рекурсией (как сделать моментальную передачу значения и выход из рекурсии? #
def search_last(channel, number, delta, channel_description):    # сам алгоритм поиска последнего поста
    delta = delta // 2
    a = 0
    if (delta < 10) and (get_text_from_post(channel+str(number)) != channel_description):
        new_number=number+1
        return search_last(channel, new_number, delta, channel_description)

    elif (delta < 10) and (get_text_from_post(channel + str(number)) == channel_description):
        return (number-1)

    elif (delta>10) and (get_text_from_post(channel+str(number))== channel_description):
        new_number = number - delta
        return search_last(channel, new_number, delta, channel_description)
    elif (delta >10) and (get_text_from_post(channel+str(number))!= channel_description):    # указывает на то, что пост есть
        new_number=number+delta
        return search_last(channel, new_number, delta, channel_description)



def define_last_post(channel):   # определяем последний пост
    channel_description = get_text_from_post(channel)   # описание канала
    max = 20000
    last = search_last(channel, max, max, channel_description)
    return last


def write_csv(content): #пишем в .csv
    with open('tgcontent.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([content])

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
                #print('Захожу на: '+channel + ' и начинаю искать последний пост...')
                #define_last_post(channel) #поиск последнего поста
                print('Начинаю выгружать посты с канала '+channel+ ' в .csv, пока они есть')
                number = 80
                a = get_text_from_post(channel+str(number))
                b = get_text_from_post(channel)
                while (get_text_from_post(channel+str(number)) != (get_text_from_post(channel))): # сравниваю содержимое главное и постов
                    content = get_text_from_post(channel+str(number))
                    url = channel+str(number)
                    write_csv(content)
                    number=number+1

            except:
                print('Ошибка при получении канала! Перехожу к следующему')





if __name__ == '__main__':
    main()