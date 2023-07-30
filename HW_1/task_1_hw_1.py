# 📌 Создать базовый шаблон для интернет-магазина,
# содержащий общие элементы дизайна (шапка, меню,
# подвал), и дочерние шаблоны для страниц категорий
# товаров и отдельных товаров.
# 📌 Например, создать страницы "Одежда", "Обувь" и "Куртка",
# используя базовый шаблон.

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def base():
    return render_template('base.html')


@app.route('/clothes/')
def clothes():
    _clothes = [{'name': 'блузка_1', 'file': 'b1.jpg',},
                {'name': 'блузка_2', 'file': 'b2.jpg',},
                {'name':' платье_1', 'file': 'dr1.jpg',},
                {'name': 'платье_2', 'file': 'dr2.jpg',},] 
    context = {'clothes': _clothes} 

    return render_template('clothes.html', **context)
    

@app.route('/shoes/')
def shoes():    
    return render_template('shoes.html')

@app.route('/jackets/')
def jackets():    
    return render_template('jackets.html')

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=True, port=5001)