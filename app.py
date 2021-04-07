from flask import Flask, render_template, request, jsonify
import datetime
import pytz # $ pip install pytz
import json

from flask_mongoengine import MongoEngine
from src.application import get_result_from_model

app = Flask(__name__)

DB_URI = "mongodb+srv://iatosprueba:Iatosprueba@cluster0.bjihe.mongodb.net/iatosdata?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI

db= MongoEngine(app)


class User(db.Document):
    name = db.StringField()
    dni = db.IntField()
    b64_str = db.StringField()
    respuesta = db.StringField()
    hora_registro = db.DateTimeField()
    opcionSi1 = db.BooleanField()
    opcionSi2 = db.BooleanField()
    opcionSi3 = db.BooleanField()
    opcionSi4 = db.BooleanField()
    opcionSi5 = db.BooleanField()
    opcionSi6 = db.BooleanField()
    opcionSi7 = db.BooleanField()
    def to_json(self):
        return {"name":self.name,
                "b64_str":self.b64_str}

@app.route('/')
@app.route('/index')
def index():    
    return render_template('index.html', title='IATos', ims={})

@app.route('/enviar_tos/', methods=['POST','PUT'])
def get_result():
    print('Inicio para obtener resultados a partir de la tos: {}'.format(datetime.datetime.now()))
    try:
        # Transforma el contenido de bytes a diccionario
        dict_data = json.loads(request.data)
        # Recuperar sólo la cadena de la tos grabada
        #print(dict_data['tos_base64'])
        tos = dict_data['tos_base64'].split('base64,')[1]
        #print(tos)
        
        # Envío del bytecod64 de la tos grabada
        mensaje_respuesta = get_result_from_model(tos)
        #mensaje_respuesta = 'positivo'

        # Recuperar valores marcados en el formulario
        opcionSi1 = dict_data['opcionSi1']
        opcionSi2 = dict_data['opcionSi2']
        opcionSi3 = dict_data['opcionSi3']
        opcionSi4 = dict_data['opcionSi4']
        opcionSi5 = dict_data['opcionSi5']
        opcionSi6 = dict_data['opcionSi6']
        opcionSi7 = dict_data['opcionSi7']

        hora_registro = datetime.datetime.now(pytz.timezone("America/Argentina/Buenos_Aires"))

        user = User(name='NombrePrueba', dni=11111112, b64_str=tos, 
                    respuesta=mensaje_respuesta,
                    hora_registro=hora_registro,
                    opcionSi1=opcionSi1,
                    opcionSi2=opcionSi2,
                    opcionSi3=opcionSi3,
                    opcionSi4=opcionSi4,
                    opcionSi5=opcionSi5,
                    opcionSi6=opcionSi6,
                    opcionSi7=opcionSi7)
        user.save()
    except Exception as e:
        print('Hubo un error. {}'.format(e))
        return jsonify('Hubo un error. Volver a grabar la tos.')

    print('Fin para obtener resultados a partir de la tos: {}'.format(datetime.datetime.now()))
    return jsonify(f'Resultado: {mensaje_respuesta}')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
