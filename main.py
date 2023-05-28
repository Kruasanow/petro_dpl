from flask import Flask, render_template, url_for, request, session
import requests
from tokens import token_buff
from read_csv import reload_csv, read_csv_file
from parse import potential

app = Flask(__name__)    

@app.route('/', methods = ['get','post'])
def index():
    print(url_for('index'))

    if request.method == "POST":
        file = request.files['file']
        filename = file.filename
        print(filename)
        if file:
            # Пример использования
            # file_path = file
            csv_data = reload_csv(read_csv_file(filename))
            print(csv_data)
            res = potential(csv_data)
            

        return render_template('index.html',
                               data = csv_data,
                               res = res
                               )

    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)


