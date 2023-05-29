from flask import Flask, render_template, url_for, request, session
import requests
from tokens import token_buff
from read_csv import reload_csv, read_csv_file
from parse import potential, find_bad_words, naebalovo, get_count_posts

app = Flask(__name__)    

@app.route('/', methods = ['get','post'])
def index():
    print(url_for('index'))

    if request.method == "POST":
        file = request.files['file']
        filename = file.filename
        print(filename)
        if file:
            csv_data = reload_csv(read_csv_file(filename))
            print(csv_data)
            danger_domains = list(naebalovo(potential(csv_data))[0].keys())
            ret_bad_w = {}
            for i in danger_domains:
                ret_bad_w[f"badwords-{i}"] = find_bad_words(i)
                ret_bad_w[f"count-posts-{i}"] = get_count_posts(i)
                ret_bad_w[f"procent-{i}"] = len(ret_bad_w[f"badwords-{i}"][f"{i}"]) / ret_bad_w[f"count-posts-{i}"]

            for j in danger_domains:
                if ret_bad_w[f'procent-{j}'] <= 0.05:
                    ret_bad_w[f'raport-{j}'] = 'запустить чат ботов, которые создадут позитивный шум, создадут альтернативную точку зрения'
                elif ret_bad_w[f'procent-{j}'] > 0.05 and ret_bad_w[f'procent-{j}'] <= 0.15:
                    ret_bad_w[f'raport-{j}'] = 'заблокировать посты'  
                else:
                    ret_bad_w[f'raport-{j}'] = 'заблокировать источник'
        
            # c2 = [{'a4': [1668298, 1664557, 1661945, 1659315]}, 30, 0.13333333333333333, 'запустить чат ботов, которые создадут позитивный шум, создадут альтернативную точку зрения']
            # c = ['badwords-a4', 'count-posts-a4', 'procent-a4', 'raport-a4']
            c= ret_bad_w.keys()
            c2= ret_bad_w.values()


        return render_template('index.html',
                               data = csv_data,
                               c = c,
                               c2 = c2
                               )

    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)


