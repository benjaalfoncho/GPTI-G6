import requests
import os

def obtener_ubicacion(localidad, codigo_estado, codigo_pais, limite):
    # api_key from .env
    api_key = os.environ['API_KEY']
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={localidad},{codigo_estado},{codigo_pais}&limit={limite}&appid={api_key}'

    try:
        response = requests.get(url)
        data = response.json()

        if data:
            # Selecciona la primera ubicación encontrada
            ubicacion = data[0]
            latitud = ubicacion['lat']
            longitud = ubicacion['lon']

            return latitud, longitud
        else:
            return None, None
    except requests.exceptions.RequestException as e:
        # Manejo de errores de conexión
        print(f'Error al obtener la ubicación: {e}')
        return None, None

def lambda_handler(event, context):
    intent_name = event['request']['intent']['name']

    if intent_name == 'ObtenerUbicacion':
        localidad = event['request']['intent']['slots']['Localidad']['value']
        codigo_estado = event['request']['intent']['slots']['CodigoEstado']['value']
        codigo_pais = event['request']['intent']['slots']['CodigoPais']['value']
        limite = 1

        latitud, longitud = obtener_ubicacion(localidad, codigo_estado, codigo_pais, limite)

        if latitud is not None and longitud is not None:
            response = {
                'version': '1.0',
                'response': {
                    'outputSpeech': {
                        'type': 'PlainText',
                        'text': f'La ubicación de {localidad} es: Latitud {latitud} y Longitud {longitud}.'
                    }
                }
            }
        else:
            response = {
                'version': '1.0',
                'response': {
                    'outputSpeech': {
                        'type': 'PlainText',
                        'text': 'No se pudo obtener la ubicación.'
                    }
                }
            }
    else:
        # Manejo de otras intenciones
        response = {
            'version': '1.0',
            'response': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': 'No entiendo esa solicitud.'
                }
            }
        }

    return response
