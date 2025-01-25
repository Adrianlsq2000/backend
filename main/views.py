from django.shortcuts import render
# Importe el decorador login_required
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse
# Importe requests y json
import requests
import json
# Importe el decorador login_required
from django.contrib.auth.decorators import login_required, permission_required
# Restricción de acceso con @login_required
@login_required
@permission_required('main.index_viewer', raise_exception=True)
def index(request):
    #Arme el endpoint del REST API
    current_url = request.build_absolute_uri()
    url = current_url + '/api/v1/landing'

    # Petición al REST API
    response_http = requests.get(url)
    response_dict = json.loads(response_http.content)

    print("Endpoint ", url)
    print("Response ", response_dict)

    # Respuestas totales
    total_responses = len(response_dict.keys())
    # Valores de la respuesta
    responses = response_dict.values()
    # Primera y ultima respuesta
    if isinstance(response_dict, list) and len(response_dict) > 0:
        first_response = response_dict[0]  # Primera respuesta
        last_response = response_dict[-1]  # Última respuesta
    elif isinstance(response_dict, dict) and response_dict:
        # Obtenemos del diccionario  la primera y última respuesta de las claves
        first_response = next(iter(response_dict.values()))  # Primera respuesta
        last_response = next(reversed(list(response_dict.values())))  # Última respuesta
    else:
        first_response = last_response = None
    #Prueba que imprimen 
    #print("Primera respuesta: ", first_response)
    #print("Última respuesta: ", last_response)
    #Dia con mas interacciones 
    days_responses = {}
    for response in response_dict.values():
        if 'saved' in response:
            saved_date = response['saved'].split(',')[0].strip()  # Extraer solo la fecha (d/m/Y)
            days_responses[saved_date] = days_responses.get(saved_date, 0) + 1

    # Día con más respuestas
    high_rate_responses_day = max(days_responses, key=days_responses.get, default=None)
    

    # Objeto con los datos a renderizar
    data = {
        'title': 'Landing - Dashboard',
        'total_responses': total_responses,
        'responses': responses,
        'first_responses': first_response['saved'] if first_response else 'N/A',
        'last_responses': last_response['saved'] if last_response else 'N/A', 
        'high_rate_responses': high_rate_responses_day if high_rate_responses_day else 'N/A', 
    }
    #return HttpResponse("Hello, World!")
    return render(request, 'main/index.html', data)