from flask import Flask, render_template, request
import sqlite3
import getjson

DATABASE = '/blog.db'
app = Flask(__name__)


@app.route('/')
def index():
    """ Открытие главной страницы """
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    """ Обработка запроса и вывод результата """
    if request.method == 'POST':
        search_query = request.form['search_query']
        if len(search_query) >= 3:  # Проверка на длинну полученных данных
            connection = sqlite3.connect('blog.db')
            cursor = connection.cursor()

            cursor.execute("""
                    SELECT Comments.*, Posts.title 
                    FROM Comments 
                    JOIN Posts ON Comments.post_id = Posts.post_id 
                    WHERE Comments.body LIKE ?
                """, ('%' + search_query + '%',))

            search_results = cursor.fetchall()

            connection.close()

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
