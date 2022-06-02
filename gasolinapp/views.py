import json
import os
import re
from cgitb import handler
from unicodedata import name

import ipinfo
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from pyrsistent import field
from tqdm import tqdm
from .scraping import scraper
from django.db.models import Q

from gasolinapp.forms import *
from gasolinapp.models import *

# Create your views here.


# def loginPage(request):
#     if request.user.is_authenticated:
#         return redirect('index')
#     else:
#         if request.method == 'POST':
#             username = request.POST.get('username')
#             password = request.POST.get('password')

#             user = authenticate(request, username=username, password=password)

#             if user is not None:
#                 login(request, user)
#                 return redirect('index')
#             else:
#                 messages.info(request, 'Username o Contraseña es incorrecta.')

#         context = {}
#         return render(request, 'login.html', context)

# def registerPage(request):
#     if request.user.is_authenticated:
#         return redirect('index')
#     else:
#         form = FormularioRegistro()

#         if request.method == 'POST':
#             form = FormularioRegistro(request.POST)
#             if form.is_valid():
#                 form.save()

#                 user = form.cleaned_data.get('username')
#                 messages.success(request, "La cuenta fue creada para " + user)

#                 return redirect('loginPage')

#         context = {'form': form}
#         return render(request, 'registro.html', context)

# @login_required(login_url='loginPage')
# def logoutUser(request):
#     logout(request)
#     return redirect('loginPage')

# @login_required(login_url='loginPage')
def index(request):
    estado = Estado.objects.last()
    q = Q(ID_CCAA__exact='04') | Q(ID_CCAA__exact='05') | Q(ID_CCAA__exact='18') | Q(ID_CCAA__exact='19') | Q(sell_type__exact='R') | Q(diesel_A__exact='')

    gasolineras_diesel = Gasolinera.objects.all().exclude(q).order_by('diesel_A')[:3]
    gasolineras_gasolina = Gasolinera.objects.all().exclude(q).order_by('gasoline_95_E5')[:3]
    context = {"info": estado.fecha, "gasolineras_diesel": gasolineras_diesel, "gasolineras_gasolina": gasolineras_gasolina}

    return render(request, 'index.html', context)

# @login_required(login_url='loginPage')


def listaBBDD(request):
    tok = '445ee35d55fd36'
    handler = ipinfo.getHandler(tok)
    data = handler.getDetails()

    ciudad = data.city

    mas_barata_diesel = Gasolinera.objects.filter(location__iexact=ciudad).exclude(
        diesel_A__exact='').order_by('diesel_A').first()

    mas_barata_gasolina = Gasolinera.objects.filter(location__iexact=ciudad).exclude(
        gasoline_95_E5__exact='').order_by('gasoline_95_E5').first()

    gasolineras = Gasolinera.objects.all().order_by('municipality')
    pagina = Paginator(gasolineras, per_page=20)

    page_number = request.GET.get('page')
    page_obj = pagina.get_page(page_number)

    estado = Estado.objects.last()

    latitud = (mas_barata_diesel.latitude).replace(',', '.')
    longitud = (mas_barata_diesel.longitude).replace(',', '.')
    link_diesel = f'http://maps.google.com/maps?q={latitud},{longitud}'

    latitud = (mas_barata_gasolina.latitude).replace(',', '.')
    longitud = (mas_barata_gasolina.longitude).replace(',', '.')
    link_gasolina = f'http://maps.google.com/maps?q={latitud},{longitud}'

    if(mas_barata_diesel.sell_type == "R"):
        mas_barata_diesel.sell_type = "CERRADA AL PÚBLICO GENERAL"
    else:
        mas_barata_diesel.sell_type = "VENTA AL PÚBLICO"

    if(mas_barata_gasolina.sell_type == "R"):
        mas_barata_gasolina.sell_type = "CERRADA AL PÚBLICO GENERAL"
    else:
        mas_barata_gasolina.sell_type = "VENTA AL PÚBLICO"

    context = {
        "ciudad": ciudad,
        "mas_barata_diesel": mas_barata_diesel,
        "mas_barata_gasolina": mas_barata_gasolina,
        "link_diesel": link_diesel,
        "link_gasolina": link_gasolina,
        "info": estado.fecha,
        "num": estado.validas,
        "page_obj": page_obj}

    return render(request, 'listaBBDD.html', context)


def masBarata(request):

    if request.method == "POST":
        estado = Estado.objects.last()
        if (request.POST['municipality'] != ''):
            context = {}
            name = request.POST['municipality']

            estado = Estado.objects.last()

            mas_barata_ciudad = Gasolinera.objects.filter(municipality__iexact=name).exclude(
                diesel_A__exact='').order_by('diesel_A').first()

            mas_barata_gasolina = Gasolinera.objects.filter(municipality__iexact=name).exclude(
                gasoline_95_E5__exact='').order_by('gasoline_95_E5').first()

            if(not mas_barata_ciudad):

                context = {
                    "name": f'La gasolinera más barata de {name} no ha sido encontrada.', "info": estado.fecha}
                return render(request, 'errorBusqueda.html', context)

            else:

                # mas_barata_ciudad = Gasolinera.objects.filter(**myquery).first()

                print(mas_barata_ciudad)

                latitud = (mas_barata_ciudad.latitude).replace(',', '.')
                longitud = (mas_barata_ciudad.longitude).replace(',', '.')

                link_diesel = f'http://maps.google.com/maps?q={latitud},{longitud}'

                latitud = (mas_barata_gasolina.latitude).replace(',', '.')
                longitud = (mas_barata_gasolina.longitude).replace(',', '.')

                link_gasolina = f'http://maps.google.com/maps?q={latitud},{longitud}'

                if(mas_barata_ciudad.sell_type == "R"):
                    mas_barata_ciudad.sell_type = "CERRADA AL PÚBLICO GENERAL"
                else:
                    mas_barata_ciudad.sell_type = "VENTA AL PÚBLICO"

                if(mas_barata_gasolina.sell_type == "R"):
                    mas_barata_gasolina.sell_type = "CERRADA AL PÚBLICO GENERAL"
                else:
                    mas_barata_gasolina.sell_type = "VENTA AL PÚBLICO"

                context = {
                    "mas_barata_diesel": mas_barata_ciudad,
                    "mas_barata_gasolina": mas_barata_gasolina,
                    "link": link_diesel,
                    "link_gasolina": link_gasolina,
                    "info": estado.fecha,
                    "ciudad": name
                }

                return render(request, 'gasolineraBarata.html', context)
        else:
            context = {
                "name": 'No has introducido el nombre de ninguna ciudad.', "info": estado.fecha}
            return render(request, 'errorBusqueda.html', context)
    else:
        return render(request, 'listaBBDD.html', context)


def infoGasolinera(request, id_gasolinera):
    tok = '445ee35d55fd36'
    handler = ipinfo.getHandler(tok)
    data = handler.getDetails()

    ciudad = data.city
    gasolinera = Gasolinera.objects.get(IDEESS__exact=id_gasolinera)

    latitud = (gasolinera.latitude).replace(',', '.')
    longitud = (gasolinera.longitude).replace(',', '.')
    link = f'http://maps.google.com/maps?q={latitud},{longitud}'

    estado = Estado.objects.all().last()

    if(gasolinera.sell_type == "R"):
        gasolinera.sell_type = "CERRADA AL PÚBLICO GENERAL"
    else:
        gasolinera.sell_type = "VENTA AL PÚBLICO"

    if(gasolinera.margen == "D"):
        gasolinera.margen = "DERECHA"
    else:
        gasolinera.margen = "IZQUIERDA"

    direccion = f'{gasolinera.municipality},{gasolinera.CP}'
    datos = scraper(ciudad, direccion)
    context = {"mas_barata_diesel": gasolinera, "datos": datos,
               "link": link, "ciudad": ciudad, "info": estado.fecha, "busqueda": True}

    return render(request, 'gasolineraBarata.html', context)


# @login_required(login_url='loginPage')
def actualizarBBDD(request):

    Gasolinera.objects.all().delete()

    resp = requests.get(
        'https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/')
    data = resp.json()
    validos = 0
    fallos = 0

    fecha = data['Fecha']
    gasolineras = data['ListaEESSPrecio']

    for gasolinera in tqdm(gasolineras):
        try:
            # if (not gasolinera['Precio Gasoleo A'] and not gasolinera['Precio Gasolina 95 E5'] and not gasolinera['Precio Gasolina 95 E10'] and not gasolinera['Precio Gasolina 95 E5'] and not gasolinera['Precio Gasolina 95 E5 Premium'] and not gasolinera['Precio Gasolina 98 10'] and not gasolinera['Precio Gasolina 98 E5']):
            #     fallos+=1
            # else:
            Gasolinera.objects.update_or_create(CP=gasolinera['C.P.'], address=gasolinera['Dirección'], schedule=gasolinera['Horario'], latitude=gasolinera['Latitud'], location=gasolinera['Localidad'], longitude=gasolinera['Longitud (WGS84)'], margen=gasolinera['Margen'], municipality=gasolinera['Municipio'],
                                                biodiesel=gasolinera['Precio Biodiesel'], bioetanol=gasolinera['Precio Bioetanol'], GNC=gasolinera['Precio Gas Natural Comprimido'], GNL=gasolinera['Precio Gas Natural Licuado'], GLP=gasolinera[
                                                    'Precio Gases licuados del petróleo'], diesel_A=gasolinera['Precio Gasoleo A'], diesel_B=gasolinera['Precio Gasoleo B'], diesel_premium=gasolinera['Precio Gasoleo Premium'],
                                                gasoline_95_E10=gasolinera['Precio Gasolina 95 E10'], gasoline_95_E5=gasolinera['Precio Gasolina 95 E5'], gasoline_95_E5_premium=gasolinera['Precio Gasolina 95 E5 Premium'], gasoline_98_E10=gasolinera[
                                                    'Precio Gasolina 98 E10'], gasoline_98_E5=gasolinera['Precio Gasolina 98 E5'], hydrogen=gasolinera['Precio Hidrogeno'], province=gasolinera['Provincia'], remission=gasolinera['Remisión'],
                                                name=gasolinera['Rótulo'], sell_type=gasolinera['Tipo Venta'], bioetanol_perc=gasolinera['% BioEtanol'], ester_met_perc=gasolinera['% Éster metílico'], IDEESS=gasolinera['IDEESS'], ID_municipality=gasolinera['IDMunicipio'], ID_province=gasolinera['IDProvincia'], ID_CCAA=gasolinera['IDCCAA'])
            validos += 1
        except:
            print(f"\n\nFALLO EN LA GASOLINERA {gasolinera['Rótulo']}\n")
            fallos += 1

    Estado.objects.update_or_create(
        fecha=fecha, validas=validos, invalidas=fallos)

    estado = Estado.objects.all().last()

    context = {"estado": estado, "info": estado.fecha}
    return render(request, 'actualizarBBDD.html', context)
