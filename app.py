from flask import Flask, render_template, request
import datetime
import json


app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():    
    return render_template('index.html', title='IATos', ims={})

@app.route('/enviar_tos/', methods=['POST'])
def get_result():
    print('Inicio para obtener resultados a partir de la tos: {}'.format(datetime.datetime.now()))
    
    try:
        # Transforma el contenido de bytes a diccionario
        dict_data = json.loads(request.data)
        # Recuperar sólo la cadena de la tos grabada
        #print(dict_data['tos_base64'])
        tos = dict_data['tos_base64'].split('base64,')[1]
        print(tos)
        # Envío del bytecod64 de la tos grabada
        #application.get_result(tos)
    except Exception as e:
        print('Hubo un error. {}'.format(e))
        return 'Hubo un error. Volver a grabar la tos.'

    print('Fin para obtener resultados a partir de la tos: {}'.format(datetime.datetime.now()))
    return 'La persona tiene positivo para COVID-19.'
    

if __name__ == '__main__':
    app.run(debug=True)