from flask import Flask, render_template, request
import psycopg2
import getjson

app = Flask(__name__)


@app.route('/')
def index():
    """ Открытие главной страницы """
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    """ Обработка запроса и вывод результата """
    if request.method == 'POST':
        search_query = request.form['search_query']  # Получение данных из input поля
        if len(search_query) >= 3:  # Проверка на длинну полученных данных
            connection = psycopg2.connect(  # Соединение с БД
                host='127.0.0.1',
                user='postgres',
                password='root',
                database='post_db'
            )
            cursor = connection.cursor()  # Установка курсора на нашу БД

            cursor.execute("""
                    SELECT Comments.body, Posts.title 
                    FROM Comments 
                    JOIN Posts ON Comments.post_id = Posts.id 
                    WHERE Comments.body LIKE %s
                """, ('%' + search_query + '%',))
            # #SQL
            # Выбор таблицы с коментариями и обращаемся к заголовкам постов.
            # Присоединяем данные из таблицы Posts.
            # Выбор записей, где содержание комментария содержит строку заданную переменной search_query.

            search_results = cursor.fetchall()  # Возврат результата
            connection.close()  # Закрытие БД

            if search_results:
                return render_template('search_results.html', search_results=search_results)
            else:
                return 'Ничего не найдено'
        else:
            return 'Поисковый запрос должен содержать как минимум 3 символа'
    else:
        render_template('index.html')

if __name__ == '__main__':
    getjson.get_json.get_json()
    getjson.get_json.create_db()
    app.run()
