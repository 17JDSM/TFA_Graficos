from transformers import pipeline

# Cargar el modelo y el procesador desde Hugging Face
# nlp = pipeline("question-answering", model="timpal0l/mdeberta-v3-base-squad2") # Consumir modelo de Hugging Face
nlp = pipeline("question-answering", model="models/mdeberta-v3-base-squad2/") # Consumir localment


contexto = r""" 
La aplicación tiene como objetivo proporcionar descripciones en lenguaje natural de imágenes estadísticas que contienen representaciones visuales de datos numéricos, como gráficos y diagramas. 
Se enfoca específicamente en gráficos de barras y gráficos de pastel. 
La aplicación utiliza modelos preentrenados y redes neuronales transformer para extraer características visuales de las imágenes y decodificar su significado, generando descripciones coherentes en formato de texto.
Estas descripciones pueden ser reproducidas para facilitar la comprensión de la información visual. 
La aplicación está diseñada para ayudar a las personas que tienen dificultades para interpretar este tipo de información.
"""

# Función para devolver la respuesta del modelo
def get_response(msg):
    pregunta = msg

    respuesta = nlp({'question': pregunta, 'context': contexto})
    answer = respuesta['answer']
    score = respuesta['score']

    # Se puede agregar un valor más alto, pero al ser impreciso todavía lo haremos con un valor bajo
    if score > 0.001: 
        return answer
    
    return "Me apena reconocer que lo que expone supera mi comprensión actual."

def set_content(text):
    new_contexto = text

if __name__ == "__main__":
    print("\n\nDescripción de Imagenes Estadísticas - Asistente por Chat")
    print("\n¡Vamos a chatear! (escribe 'X' para salir)")
    while True:
        sentence = input("Tu: ")
        if sentence == "X":
            break
        print("David:", get_response(sentence), "\n")