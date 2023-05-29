from flask import Flask, render_template, url_for, request, session
import requests
from tokens import token_buff
from read_csv import reload_csv, read_csv_file
from parse import potential, find_bad_words

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
            res = potential(csv_data)[3]
            compare = dict(zip(csv_data,res))
            a = list(compare.values())
            sum = 0
            new_arr = []
            for i in a:
               sum+=i
            avg = sum/len(a)
            for j in a:
                if j<avg:
                    pass
                else:
                    new_arr.append(j)
            print(new_arr)
            result = [key for key, value in compare.items() if value in new_arr]
            for i in result:
                final_res = find_bad_words(i)

        return render_template('index.html',
                               data = csv_data,
                               res = res,
                               final = final_res
                               )

    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)


