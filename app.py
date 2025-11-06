from flask import Flask, render_template, request
from markupsafe import Markup
import re


app = Flask(__name__)

# Aquí se crean las expresiones regulares
REGEX_CORREO = re.compile(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,})')
REGEX_TELEFONO = re.compile(r'\b\d{10}\b')
REGEX_FECHA = re.compile(r'\b(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[0-2])/\d{4}\b')

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = ""
    texto = ""

    if request.method == 'POST':
        texto = request.form['texto']

        # Reemplazos con span para resaltar
        resaltado = texto
        resaltado = REGEX_CORREO.sub(r'<span class="correo">\1</span>', resaltado)
        resaltado = REGEX_TELEFONO.sub(r'<span class="telefono">\g<0></span>', resaltado)
        resaltado = REGEX_FECHA.sub(r'<span class="fecha">\g<0></span>', resaltado)

        # Permitir HTML seguro en la plantilla, hace que Flask no lo muestre como texto plano
        resultado = Markup(resaltado)

    return render_template('index.html', resultado=resultado, texto=texto)

if __name__ == '__main__':
    app.run(debug=True)
