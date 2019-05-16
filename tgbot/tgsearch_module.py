import requests
import socks    # для прокси
import socket   # для прокси
import csv
from bs4 import BeautifulSoup  # парсер


def get_html(url):
    response = requests.get(url)
    return response.text

def get_content_from_post(url): # получаю из поста: автора, текст, дату
    html = get_html(url+'?embed=1') #?embed=1 -- позволяет открыть адекватный кода страницы в html для парсинга
    soup = BeautifulSoup(html, 'lxml')
    if(soup.find('div', class_='tgme_widget_message_error')== None and soup.find('div', class_='message_media_not_supported_label')== None): #пока не появляется класс ошибки, выполняется тело, иначе возвращает 0

        channel = soup.find('div', class_='tgme_widget_message_author').get_text()  # название канала
        text = soup.find('div', class_='tgme_widget_message_text').get_text()  # текст поста
        date = soup.find('time', class_='datetime').get_text()  # дата
        content = [channel, text, date]
        return content
    elif(soup.find('div', class_='tgme_widget_message_error')!= None or soup.find('div', class_='message_media_not_supported_label')!= None):
        return 1 #нужно перейти к следующему
    else:
        return 0

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


def write_csv(content): #пишем в .csv
    with open('tgcontent.csv', 'a', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(content)

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
    #addr
    #port
    #username
    #password

    url = 'https://tlgrm.ru/channels/news' #каталог новостных каналов Телеграм

    start_proxy(addr, port, username, password) #поднимаем единый прокси для всех запросов

    channels = get_channel_links(url)    #получить первые 25 каналов по ссылке из каталога каналов

    for channel in channels:
        if channel!='https://t.me//':
            try:
                print('Начинаю выгружать посты с канала '+channel+ ' в .csv, пока они есть')
                number = 1
                content = get_content_from_post(channel + str(number))
                while (content!=0): #пока не появляется класса ошибки, пишем посты, иначе не пишем и переходим к +1 посту
                    if (content != 1):
                        write_csv(content) #пишется сразу массив по строкам: канал+текст+дата
                        print(str(content[0]) + ' ' + str(content[1]) + ' ' + str(content[2]))
                    number = number+1
                    content = get_content_from_post(channel+str(number))

            except:
                print('Ошибка при получении поста! Перехожу к следующему каналу')





if __name__ == '__main__':
    main()