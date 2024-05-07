import requests
import psycopg2
import config


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
        connection = psycopg2.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        self.cur = connection.cursor()

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS Posts (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            user_id INTEGER NOT NULL);
        ''')
        # Создание таблицы для записей блога

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS Comments (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            body TEXT NOT NULL
        );
        ''')
        # Создание таблицы для комментариев к записям блога

        self.cur.execute('''
            SELECT EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_name = 'Comments' AND column_name = 'post_id'
            );
        ''')
        self.cur.execute('''
            SELECT post_id 
            FROM Comments
        ;
        ''')
        if not self.cur.fetchall():
            self.cur.execute('''
                ALTER TABLE Comments ADD post_id BIGINT REFERENCES Posts (id);
            ''')
        # Создание внешнего ключа

        x = y = 0

        for post in self.list_posts:
            try:
                self.cur.execute('''INSERT INTO Posts (id, title, body, user_id) VALUES (%s, %s, %s, %s)
                                    ON CONFLICT (id) DO UPDATE
                                    SET title = EXCLUDED.title,
                                        body = EXCLUDED.body,
                                        user_id = EXCLUDED.user_id;
                                    ''',
                                 (post['id'], post['title'], post['body'], post['userId']))
                x += 1
            except Exception as e:
                print(f"Error updating post {post['id']}: {e}")
        # Заполнение таблицы блогов

        for comment in self.list_comments:
            try:
                self.cur.execute('''INSERT INTO Comments (id, post_id, name, email, body) VALUES (%s, %s, %s, %s, %s)
                                    ON CONFLICT (id) DO UPDATE
                                    SET post_id = EXCLUDED.post_id,
                                    name = EXCLUDED.name,
                                    email = EXCLUDED.email,
                                    body = EXCLUDED.body;
                                ''',
                                 (comment['id'], comment['postId'], comment['name'], comment['email'], comment['body']))
                y += 1
            except Exception as e:
                print(f"Error updating comment {post['id']}: {e}")
        # Заполнение таблицы комментариев

        connection.commit()
        connection.close()

        print(f'Загружено {x} записей и {y} комментариев')


get_json = GetJSON()
