from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from main_form import Ui_MainWindow as main_form
from quiz_form import Ui_quiz as quiz_form
from loading_form import Ui_gif_form as load_form
from films_form import Ui_Form as films_form
from bs4 import BeautifulSoup
from threading import Thread
import requests
import urllib.request
import time
import sqlite3
import copy
import sys
import random


def load_db():
    global all_actors, f, cinema_films
    url = 'https://www.afisha.ru/samara/schedule_cinema'
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    a = []
    for i in soup.find_all('a'):
        if i.get('href'):
            if 'movie/' in i.get('href') and len(i.get('href').split('/')) == 4:
                x = i.get('href').split('/')
                if x[1] == 'movie':
                    f2 = True
                    for j in x[2]:
                        if j not in '0123456789':
                            f2 = False
                            break
                    if f2:
                        a.append(i.get('href'))
    id = 0
    con = sqlite3.connect('data/database.db')
    cursor = con.cursor()
    cursor.execute('DELETE FROM films')
    con.commit()
    films = []
    for i in set(a):
        url = 'https://www.afisha.ru' + i
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        name = soup.find('span', {'class': 'name___15--1'}).find('span').getText()
        try:
            rating = float(soup.find('span', {'class': 'meta___3TQLR'}).getText().split()[-1])
        except:
            pass
        try:
            title = soup.find('h2', {'class': 'title___c6HeZ'}).getText()
        except:
            print(url)
        try:
            about = soup.find('p').getText()
        except:
            print(url)
        director = soup.find('a', {'class': 'director___L1WtG'}).getText()
        age = soup.find_all('div', {'class': 'fieldLabel___5UPR7'})[0].getText()[:-1]
        genres = ' '.join([i.getText() for i in soup.find_all('a', {'class': 'link-list__item-link'})])
        time = soup.find_all('div', {'class': 'field___1t8kE'})[3].getText()
        cinemas_names = [i.getText() for i in soup.find_all('a', {'class': 'unit__movie-name__link'})]
        cinemas_loc = [i.getText() for i in soup.find_all('div', {'class': 'unit__movie-location'})]
        actors = ','.join([i.getText() for i in soup.find_all('span', {'itemprop': 'name'})])
        cinemas = []
        for i in range(len(cinemas_names)):
            cinemas.append(cinemas_names[i])
            cinemas.append(cinemas_loc[i])
        cinemas = ';'.join(cinemas)
        img = soup.find_all('img')
        for j in img:
            if 'img' in j.get('src'):
                urllib.request.urlretrieve(j.get('src'), 'data/' + 'image' + str(id) + '.jpg')
                break

        id += 1
        try:
            films.append((id, name, title, about, director, rating, genres, time, age, cinemas, actors))
        except:
            pass
        all_actors += actors.split(',')
        cinema_films += [name]
    cursor.executemany('INSERT INTO films VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', films)
    con.commit()
    f = True


class MainForm(QMainWindow, main_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.start.clicked.connect(self.push)
        self.start.installEventFilter(self)
        self.label_4.setPixmap(QPixmap('data/logo_titul.jpg'))

    def eventFilter(self, obj, event):
        # обработка наведения курсора мыши на кнопку
        if event.type() == QEvent.Enter and obj.isEnabled():
            # изменение стиля на выделенный
            obj.setStyleSheet('''border-radius: 50px;
                            background-color: #0fa3e3;
                            border: 5px solid #0091fa;
                            ''')
            # изменение стиля на невыделенный
        elif event.type() == QEvent.Leave:
            obj.setStyleSheet('''border-radius: 50px;
                                background-color: white;
                                border: 5px solid #0091fa;
                            ''')
        return QWidget.eventFilter(self, obj, event)

    def push(self):
        quiz_wnd.show()
        self.close()


class QuizForm(QWidget, quiz_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.set_compl)
        self.timer.start(10)
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.enable_ch_q)
        self.timer2.start(1)
        con = sqlite3.connect('data/big_data_films.db')
        cursor = con.cursor()
        films = [i[0] for i in cursor.execute('SELECT title FROM Films') if '&quot;' not in i[0]] + [i[0].lower() for i in cursor.execute('SELECT title FROM Films') if '&quot;' not in i[0]]
        film_completer = QCompleter(films, self.last_film)
        self.last_film.setCompleter(film_completer)
        self.back.clicked.connect(self.back_to_start)
        self.next.clicked.connect(self.push)
        self.back.installEventFilter(self)
        self.next.installEventFilter(self)

    def eventFilter(self, obj, event):
        # обработка наведения курсора мыши на кнопку
        if event.type() == QEvent.Enter and obj.isEnabled():
            # изменение стиля на выделенный
            obj.setStyleSheet('''border-radius: 20px;
background-color: #0fa3e3;
border: 5px solid #0091fa;
                            ''')
            # изменение стиля на невыделенный
        elif event.type() == QEvent.Leave:
            obj.setStyleSheet('''border-radius: 20px;
background-color: white;
border: 5px solid #0091fa;
                            ''')
        return QWidget.eventFilter(self, obj, event)

    def back_to_start(self):
        global wnd
        wnd.show()
        self.close()

    def enable_ch_q(self):
        if self.search.text() != '':
            self.genre.setEnabled(False)
            self.children.setEnabled(False)
            self.child_age.setEnabled(False)
            self.last_film.setEnabled(False)
            self.duration.setEnabled(False)
            self.fav_actor.setEnabled(False)
        else:
            self.genre.setEnabled(True)
            self.children.setEnabled(True)
            if self.children.currentText() != 'Нет':
                self.child_age.setEnabled(True)
            else:
                self.child_age.setEnabled(False)
            self.last_film.setEnabled(True)
            self.duration.setEnabled(True)
            self.fav_actor.setEnabled(True)


    def set_compl(self):
        global all_actors, f, cinema_films, films_wnd
        if f:
            actors_completer = QCompleter(all_actors, self.fav_actor)
            self.fav_actor.setCompleter(actors_completer)
            cinema_films_completer = QCompleter(cinema_films, self.search)
            self.search.setCompleter(cinema_films_completer)
            self.timer.stop()

    def push(self):
        global f, result, loading_wnd, f1
        if self.search.text() != '':
            result = [self.search.text(), self.state.currentText()]
        else:
            genre = self.genre.currentText()
            film = self.last_film.text()
            new = ''
            for i in film:
                if i not in ':;,."!?№':
                    new += i
            film = new.lower()
            if self.children.currentText() == 'Да':
                if self.child_age.currentText() == '--Не задано--':
                    self.child_age.setCurrentIndex(1)
                age = self.child_age.currentText()
            else:
                age = '--'
            time = self.duration.currentText()
            actor = self.fav_actor.text()
            state = self.state.currentText()
            result = [genre, time, age, state, actor, film, set(film.split())]
        if not f:
            self.timer.stop()
            loading_wnd = LoadingForm()
            loading_wnd.show()
            self.close()
        else:
            f1 = True
            self.timer.stop()
            films_wnd.show()
            self.close()


class LoadingForm(QWidget, load_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        n = random.randint(1, 6)
        self.l_timer = QTimer()
        self.l_timer.timeout.connect(self.push_rec)
        self.l_timer.start(10)
        movie = QMovie('gifs/' + str(n) + '.gif')
        self.label.setMovie(movie)
        movie.start()

    def push_rec(self):
        global f, films_wnd, f1
        if f:
            f1 = True
            self.l_timer.stop()
            films_wnd.show()
            self.close()


class FilmsForm(QWidget, films_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.data_to_sort = []
        self.previous.setEnabled(False)
        self.timer = QTimer()
        self.timer.timeout.connect(self.recomendation)
        self.pointer = 0
        self.clicker = QTimer()
        self.clicker.timeout.connect(self.change_page)
        self.timer.start(1)
        self.clicker.start(10)
        self.following.clicked.connect(self.next_page)
        self.previous.clicked.connect(self.previous_page)
        self.following.installEventFilter(self)
        self.previous.installEventFilter(self)

    def update_page(self):
        self.image.setPixmap(QPixmap('data/image' + str(int(self.data_to_sort[self.pointer][1][0]) - 1)))
        self.rating.setText(str(self.data_to_sort[self.pointer][1][5]))
        if len(self.data_to_sort[self.pointer][1][7]) < 15:
            self.time.setText(self.data_to_sort[self.pointer][1][7])
        else:
            self.time.setText('')
        self.label_3.setText(self.data_to_sort[self.pointer][1][4])
        self.actors.setPlainText(self.data_to_sort[self.pointer][1][10])
        self.about.setPlainText(self.data_to_sort[self.pointer][1][3])
        b = list(set(self.data_to_sort[self.pointer][1][9].split(';')))
        self.cinemas.clear()
        for i in range(0, len(b), 2):
            self.cinemas.addItem(b[i] + ' ' + b[i + 1])
        self.name.setText(self.data_to_sort[self.pointer][1][1])

    def eventFilter(self, obj, event):
        # обработка наведения курсора мыши на кнопку
        if event.type() == QEvent.Enter and obj.isEnabled():
            # изменение стиля на выделенный
            obj.setStyleSheet('''border-radius: 10px;
background-color: #0fa3e3;
border: 5px solid #0091fa;
                            ''')
            # изменение стиля на невыделенный
        elif event.type() == QEvent.Leave:
            obj.setStyleSheet('''border-radius: 10px;
background-color: white;
border: 5px solid #0091fa;
                            ''')
        return QWidget.eventFilter(self, obj, event)

    def next_page(self):
        self.pointer += 1
        self.update_page()

    def previous_page(self):
        self.pointer -= 1
        self.update_page()

    def change_page(self):
        global f1
        if f1:
            self.update_page()
            if self.pointer + 1 == len(self.data_to_sort):
                self.following.setEnabled(False)
            else:
                self.following.setEnabled(True)
            if self.pointer - 1 < 0:
                self.previous.setEnabled(False)
            else:
                self.previous.setEnabled(True)

    def recomendation(self):
        global result, f1
        if f1:
            self.timer.stop()
            con = sqlite3.connect('data/database.db')
            cursor = con.cursor()
            data = list(cursor.execute('SELECT * FROM films'))
            data_to_sort = []
            if len(result) == 2:
                for i in data:
                    a = [[]]
                    new1 = ''
                    for j in i[1]:
                        if j not in ':;,."!?№':
                            new1 += j
                    new2 = ''
                    for j in result[0]:
                        if j not in ':;,."!?№':
                            new2 += j
                    a[0].append(len(set(new1.lower().split()) & set(new2.lower().split())))
                    if result[1] != '--Не задано--':
                        a[0].append(1)
                    else:
                        a[0].append(0)
                    a[0].append(i[0])
                    a.append(i)
                    data_to_sort.append(a)
            else:
                for i in data:
                    a = [[]]
                    if result[0] in i[6].split() and result[0] != '--Не задано--':
                        a[0].append(1)
                    else:
                        a[0].append(0)
                    if len(i[7]) <= 15:
                        try:
                            time1 = int(i[7].split()[0]) * 60 + int(i[7].split()[2])
                        except:
                            time1 = int(i[7].split()[0]) * 60
                        if result[1] == '< 1 часа':
                            if time1 < 60:
                                a[0].append(1)
                        elif result[1] == '1-1.5 часа':
                            if time1 >= 60 and time1 < 90:
                                a[0].append(1)
                        elif result[1] == '1.5-2 часа':
                            if time1 >= 90 and time1 < 120:
                                a[0].append(1)
                        elif result[1] == '> 2 часов':
                            if time1 >= 120:
                                a[0].append(1)
                        else:
                            a[0].append(0)
                    if result[2] != '--':
                        if result[2] == '0-5':
                            if int(i[8]) <= 5:
                                a[0].append(1)
                            else:
                                a[0].append(0)
                        elif result[2] == '6-11':
                            if int(i[8]) <= 11:
                                a[0].append(1)
                            else:
                                a[0].append(0)
                        elif result[2] == '12-15':
                            if int(i[8]) <= 15:
                                a[0].append(1)
                            else:
                                a[0].append(0)
                        elif result[2] == '16-17':
                            if int(i[8]) <= 17:
                                a[0].append(1)
                            else:
                                a[0].append(0)
                    else:
                        a[0].append(0)
                    dc = {'Железнодорожный': ['Гудок'], 'Октябрьский': ['Киномост Мега Сити', 'Вертикаль', 'Синема Парк Парк-хаус'], 'Советский': ['Киномост Космопорт', 'Киномакс'],
                        'Красноглинский': ['Каро 8 Московский'], 'Промышленный': ['Самара'], 'Ленинский': ['5D', 'Киноклуб "Кадр"', 'Художественный', 'Киноклуб "Ракурс"'],
                        'Кировский': ['5 звезд Самара']}
                    if result[3] != '--Не задано--':
                        if dc[result[3]] in i[9].split(';'):
                            a[0].append(1)
                        else:
                            a[0].append(0)
                    else:
                        a[0].append(0)
                    if result[4] != '':
                        if result[4] in i[10].split(','):
                            a[0].append(1)
                        else:
                            a[0].append(0)
                    else:
                        a[0].append(0)
                    if result[5] != '':
                        d = {1:'комедия', 2:'драма', 3:'мелодрама', 4:'детектив', 5:'документальный', 6:'ужасы',
                             7:'музыка', 8:'фантастика', 9:'анимация', 10:'биография', 11:'боевик', 13:'приключения',
                             15:'война', 16:'семейный', 17:'триллер', 18:'фэнтези', 19:'вестерн',
                             20:'мистика', 21:'короткометражный', 22:'мюзикл', 23:'исторический', 24:'нуар'}
                        con = sqlite3.connect('data/big_data_films.db')
                        cursor = con.cursor()
                        films = list(cursor.execute('SELECT title, genre FROM Films'))
                        k = False
                        for j in films:
                            if j[0].lower() == result[5].lower():
                                if d[j[1]].lower() in [c.lower() for c in i[6].split()]:
                                    a[0].append(1)
                                    k = True
                                    break
                                else:
                                    a[0].append(0)
                                    break
                        if not k:
                            a[0].append(0)
                        news = ''
                        for o in i[1]:
                            if o not in ':;,."!?№':
                                news += o
                        a[0].append(len(set(news.lower().split()) & result[6]))
                    a.append(i)
                    data_to_sort.append(a)
            new = []
            for i in data_to_sort:
                if sum(i[0]) != 0:
                    new.append(i)
            if new:
                self.data_to_sort = copy.copy(new)
            else:
                self.data_to_sort = copy.copy(data_to_sort)
            if len(data_to_sort[0]) == 2:
                self.data_to_sort.sort(key = lambda x: (x[0][0], x[0][1]), reverse=True)
            else:
                self.data_to_sort.sort(key = lambda x: (x[0][0], x[0][-1], x[0][-2], x[0][-3], x[0][3], x[0][1], x[0][2]), reverse=True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    parser = Thread(target=load_db, daemon=True)
    all_actors = []
    cinema_films = []
    result = []
    loading_wnd = None
    f = False
    f1 = False
    wnd = MainForm()
    quiz_wnd = QuizForm()
    films_wnd = FilmsForm()
    parser.start()
    wnd.show()
    sys.exit(app.exec())
