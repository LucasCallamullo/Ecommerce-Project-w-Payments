

def valid_id_or_None(id_value):
    """
    Valida que un ID sea positivo y numérico.
    Returns:
        - int: El ID convertido a entero si es válido
        - None: Si el ID es inválido
        
    #### forma acotada para un futuro puede ahorrar milesimas..
    return int(value_id) if value_id and value_id.isdigit() and int(value_id) > 0 else None
    """
    try:
        id_int = int(id_value)
        return id_int if id_int > 0 else None
    except (TypeError, ValueError):
        return None


import json
import requests
from django.conf import settings
from requests.exceptions import RequestException
def get_url_from_imgbb(image_file):
    """Sube imagen a ImgBB con manejo robusto de errores"""
    api_key = settings.IMGBB_KEY
    
    # 1. Generar nombre único preservando extensión
    unique_name = generate_unique_name(image_file.name)
    
    try:
        # 2. Subida a ImgBB y manejo de errores
        response = requests.post(
            "https://api.imgbb.com/1/upload",    # endpoint de guardado siempre es el mismo
            params={"key": api_key},    # apikey sacada de imgBB
            files={"image": (unique_name, image_file)},    # pasameos el nuevo nombre y el archivo
            timeout=10  # Timeout en segundos para reintentar
        )
        response.raise_for_status()  # Lanza error para códigos HTTP 4XX/5XX

        # 3. Procesar respuesta, manejo error o obtengo la url 
        data = response.json()
        
        if not data.get("success"):
            error_msg = data.get("error", {}).get("message", "Error desconocido en ImgBB")
            raise ValueError(f"Error en ImgBB: {error_msg}")

        return data["data"]["url"]

    # 4. Respuesta distintos errores
    except RequestException as e:
        raise ValueError("Error de conexión con el servicio de imágenes")
    except json.JSONDecodeError:
        raise ValueError("Respuesta inválida del servicio")
    except Exception as e:
        raise ValueError("Error al procesar la imagen")
    
    
import os
import uuid
def generate_unique_name(original_filename, uuid_length=13):
    """ Genera un uuid unico de 13 caracteres ( "550e8400e29b4.jpg" )"""
    ext = os.path.splitext(original_filename)[1].lower()
    truncated_uuid = uuid.uuid4().hex[:uuid_length]
    return f"{truncated_uuid}{ext}"


def validate_image_file(img):
    """Validaciones basicas a el archivo antes de subirlo"""
    if not img.name:
        raise ValueError("El archivo no tiene nombre")
    
    if img.size == 0:
        raise ValueError("El archivo está vacío")
    
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
    extension = img.name.lower().split('.')[-1]
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Formato {extension} no soportado")

    max_size = 32 * 1024 * 1024  # 32MB
    if img.size > max_size:
        raise ValueError(f"Tamaño excede {max_size/1024/1024}MB")
    

from rest_framework import serializers
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
def parse_number(value, field_name, allow_zero=True):
    """
    Convierte y valida un número recibido como string, float o int.

    - Para campos de tipo precio (Decimal): se espera precisión de 2 decimales.
    - Para campos enteros (stock, descuento): convierte a entero.
    - Si el valor es negativo o inválido, lanza un ValidationError.

    Parámetros:
    - value: el valor recibido del frontend.
    - field_name: nombre del campo para construir el mensaje de error.
    - allow_zero: si se permite que el valor sea igual a 0.

    Returns:
        - Decimal para precios.
        - int para stock o descuento.
    """
    if isinstance(value, str):
        # Formatos como "30.000,50" => "30000.50"
        value = value.replace(".", "").replace(",", ".")

    if field_name.lower() in ('precio', 'precio de lista'):
        try:
            value = Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        except (InvalidOperation, ValueError):
            raise serializers.ValidationError(f"El {field_name} debe ser un número válido con hasta 2 decimales.")
    elif field_name.lower() in ('stock', 'descuento'):
        try:
            value = int(value)
        except (TypeError, ValueError):
            raise serializers.ValidationError(f"El {field_name} debe ser un número entero válido.")
    else:
        raise serializers.ValidationError(f"Campo '{field_name}' no reconocido para validación.")

    if (allow_zero and value < 0) or (not allow_zero and value <= 0):
        condicion = "mayor o igual a 0" if allow_zero else "mayor que 0"
        raise serializers.ValidationError(f"El {field_name} debe ser {condicion}.")

    return value


import bleach
def sanitize_html(value, allowed_tags=None):
    """
    Limpia contenido HTML, permitiendo solo las etiquetas especificadas.

    Args:
        value (str): HTML de entrada.
        allowed_tags (list): Lista de etiquetas HTML permitidas. Por defecto, solo 'p' y 'strong'.

    Returns:
        str: HTML limpio.
    """
    if allowed_tags is None:
        allowed_tags = ['p', 'strong']

    return bleach.clean(
        value,
        tags=allowed_tags,
        attributes={},
        strip=True
    )
    

import unicodedata
import re
def normalize_or_None(text):
    # Check if the text is None or empty
    if not text:
        return None
    
    # Replace plus signs '+' with spaces
    text = text.replace('+', ' ')
    
    # Remove accents
    text_without_accents = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

    # Remove special characters
    text_normalized = re.sub(r'[^\w\s]', '', text_without_accents).strip()

    # Reduce multiple spaces to a single one
    text_normalized = re.sub(r'\s+', ' ', text_normalized)

    return text_normalized
