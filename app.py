from flask import Flask, render_template, request, jsonify, flash, url_for, redirect, make_response
from chat import get_response, set_content # Funciones para la interacción del chatbot
from description import get_response_description # Descripcion de imagen con modelo preentrenado Hugging Face
from experiment import get_response_description_ex # Descripcion de imagen con modelo ajustado
from werkzeug.utils import secure_filename # Utilidad para el manejo seguro de nombres de archivos
from deep_translator import GoogleTranslator # Biblioteca para traducción de texto
import os # Para interacciones entre archivos y rutas
import deep_translator.exceptions  # Importar excepciones específicas para manejar errores de traducción
from gtts import gTTS # Biblioteca para generar audio de texto a voz

# Inicializar la aplicación Flask
app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # Tamaño máximo de carga

# Extensiones de archivos de imagen permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Plantilla de la página principal
@app.route("/")
def index():
    return render_template("base.html")

# Comprobar si el archivo cargado tiene una extensión válida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Traducir texto del idioma de origen al de destino usando Google Translator
def translate(source_language, target_language, text):
    try:
        translated = GoogleTranslator(source=source_language, target=target_language).translate(text=text)
    except deep_translator.exceptions.ElementNotFoundInGetRequest as e:
        # Manejar la excepción, por ejemplo, imprimirla o asignar un valor predeterminado
        print(f"Error en la traducción: {e}")
        translated = "Error en la traducción"
    
    return translated

# Procesar la imagen cargada, generar descripción, traducir y crear audio
@app.route('/', methods=['POST'])
def upload_image():
    global URL

    # Comprobar si se cargó un archivo
    if 'file' not in request.files:
        flash('Sin parte de archivo')
        return redirect(request.url)

    file = request.files['file']

    # Obtén el modelo seleccionado del formulario
    selected_method = request.form.get('method', 'description')

    # Asegúrese de que se haya seleccionado un archivo
    if file.filename == '':
        flash('No se ha seleccionado ninguna imagen para cargar')
        return redirect(request.url)

    # Validar tipo de archivo
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        URL = url

        # Usar al modelo seleccionado
        if selected_method == 'description':
            text = get_response_description("", url)
        elif selected_method == 'experiment':
            text = get_response_description_ex("", url)
        else:
            flash('Método no válido seleccionado')
            return redirect(request.url)

        # Traducir la descripción de inglés a español
        translated = translate('en', 'es', text)
        set_content(translated)

        # Generar audio en español a partir de la descripción traducida
        language = "es-us"
        speech = gTTS(text=translated, lang=language, slow=False)
        speech.save("static/images/description.mp3")

        # Mostrar mensaje de éxito y renderizar la página con imagen, descripción y audio. 
        flash('La imagen se ha cargado correctamente y se muestra a continuación - Modelo: '+selected_method)

        # Establecer la cookie
        response = make_response(render_template('base.html', filename=filename, descripcion=translated))
        response.set_cookie('selected_method', selected_method)
        return response
    else:
        flash('Los tipos de imagen permitidos son: png, jpg, jpeg')
        return redirect(request.url)

# Redirigir para mostrar la imagen cargada
@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

# Recibir texto del chatbot, procesarlo y devolver respuesta
@app.route("/predict", methods=["POST"])
def predict():
    text = request.get_json().get("message")
    response = get_response(text)
    message = {"answer": response}
    print(message)
    return jsonify(message)

# Recibir texto del chatbot, traducir al inglés, generar una descripción basada en el método seleccionado, 
# traducir nuevamente al español y devolver la respuesta
@app.route("/predict1", methods=["POST"])
def predict1():
    text = request.get_json().get("message")

    # Obtén el modelo seleccionado de la cookie
    selected_method = request.cookies.get('selected_method', 'description')

    # Usa el modelo correspondiente
    if selected_method == 'description':
        text_en = translate('es', 'en', text)
        response_en = get_response_description(text_en, URL)
    elif selected_method == 'experiment':
        text_en = translate('es', 'en', text)
        response_en = get_response_description_ex(text_en, URL)
    else:
        return jsonify({"answer": "Método no válido seleccionado"})

    # Traducir la respuesta nuevamente al español
    response_es = translate('en', 'es', response_en)

    message = {"answer": response_es}
    print(message)
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)