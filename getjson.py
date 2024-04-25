import requests
import sqlite3


class GetJSON:
    """ Получение списка словарей из Json и преобразование их в таблицу SQL """
    def __init__(self):
        """ init """
        self.POSTS_URL = 'https://jsonplaceholder.typicode.com/posts'
        self.COMMENTS_URL = 'https://jsonplaceholder.typicode.com/comments'
        self.cur = None
        self.list_posts = None
        self.list_comments = None

    def get_json(self):
        """ Получение списков словарей из Json """
        response_posts = requests.get(self.POSTS_URL)
        response_comments = requests.get(self.COMMENTS_URL)

        self.list_posts = response_posts.json()
        self.list_comments = response_comments.json()

    def create_db(self):
        """ Соединение с базой данных """
        connection = sqlite3.connect('blog.db')
        self.cur = connection.cursor()

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS Posts (
        post_id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        body TEXT NOT NULL,
        user_id INTEGER NOT NULL)
        ''')
        # Создание таблицы для записей блога

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS Comments (
        comment_id INTEGER PRIMARY KEY,
        post_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        body TEXT NOT NULL
        )
        ''')
        # Создание таблицы для комментариев к записям блога

        x = y = 0
        for post in self.list_posts:
            try:
                self.cur.execute("INSERT INTO Posts (post_id, title, body, user_id) VALUES (?, ?, ?, ?)",
                                 (post['id'], post['title'], post['body'], post['userId']))
                x += 1
            except sqlite3.IntegrityError:
                self.cur.execute("UPDATE Posts SET title=?, body=?, user_id=? WHERE post_id=?",
                                 (post['title'], post['body'], post['userId'], post['id']))
                x += 1
        # Заполнение таблицы блогов

        for comment in self.list_comments:
            try:
                self.cur.execute("INSERT INTO Comments (comment_id, post_id, name, email, body) VALUES (?, ?, ?, ?, ?)",
                                 (comment['id'], comment['postId'], comment['name'], comment['email'], comment['body']))
                y += 1
            except sqlite3.IntegrityError:
                self.cur.execute("UPDATE Comments SET post_id=?, name=?, email=?, body=? WHERE comment_id=?",
                                 (comment['postId'], comment['name'], comment['email'], comment['body'], comment['id']))
                y += 1
        # Заполнение таблицы комментариев

        connection.commit()
        connection.close()

        print(f'Загружено {x} записей и {y} комментариев')


get_json = GetJSON()
