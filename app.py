from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():    
    return render_template('index.html', title='IATos',ims={})

@app.route('/echo', methods=['GET','POST'])
def get_result():
    print('Obtener resultados a partir de la tos')
    print('\n')
    data = request.json['data']
    print(data)
    

