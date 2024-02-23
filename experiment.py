from PIL import Image
import io
import os
from transformers import AutoProcessor, BlipForConditionalGeneration

# Cargar el modelo y el procesador localmente
processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
#model = BlipForConditionalGeneration.from_pretrained("models/blip/")
model = BlipForConditionalGeneration.from_pretrained("models/Model_1/")

prompt = "a photography of"

def get_response_description_ex(consulta, url_img):
    try:
        # Obtener la ruta de la imagen.
        image_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), url_img)

        # Compruebe si el archivo existe antes de intentar abrirlo.
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Imagen no encontrada: {image_path}")

        # Imagen en modo binario
        with open(image_path, 'rb') as image_file:
            imagen = Image.open(io.BytesIO(image_file.read()))

        # Condición para la descripción
        if not consulta:
            text = prompt # Predeterminada
        else:
            text = consulta # Enviada por el usuario

        inputs = processor(imagen, text, return_tensors="pt")

        out = model.generate(**inputs, max_new_tokens=50)
        response = processor.decode(out[0], skip_special_tokens=True)
        return response

    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        return None