
from flask import Flask, render_template, url_for, request, session

app = Flask(__name__)    

@app.route('/', methods = ['get','post'])
def index():
    print(url_for('index'))
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
