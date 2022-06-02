# gasolineras/models.py
# from datetime import datetime
from django.db import models
  

class Gasolinera(models.Model):
  CP = models.CharField(max_length=10)
  address = models.CharField(max_length=200)
  schedule = models.CharField(max_length=100)
  latitude = models.CharField(max_length=30)
  location = models.CharField(max_length=100)
  longitude = models.CharField(max_length=30)
  margen = models.CharField(max_length=10)
  municipality = models.CharField(max_length=100)
  biodiesel = models.CharField(max_length=8)
  bioetanol = models.CharField(max_length=8)
  GNC = models.CharField(max_length=8)              # Gas Natural Comprimido
  GNL = models.CharField(max_length=8)              # Gas Natural Licuado
  GLP = models.CharField(max_length=8)              # Gases Licuados Petróleo
  diesel_A = models.CharField(max_length=8)
  diesel_B = models.CharField(max_length=8)
  diesel_premium = models.CharField(max_length=8)
  gasoline_95_E10 = models.CharField(max_length=8)
  gasoline_95_E5 = models.CharField(max_length=8)
  gasoline_95_E5_premium = models.CharField(max_length=8)
  gasoline_98_E10 = models.CharField(max_length=8)
  gasoline_98_E5 = models.CharField(max_length=8)
  hydrogen = models.CharField(max_length=8)
  province = models.CharField(max_length=30)
  remission = models.CharField(max_length=5)
  name = models.CharField(max_length=100)
  sell_type = models.CharField(max_length=30)
  bioetanol_perc = models.CharField(max_length=8)
  ester_met_perc = models.CharField(max_length=8)
  IDEESS = models.CharField(max_length=8, primary_key=True)
  ID_municipality = models.CharField(max_length=8)
  ID_province = models.CharField(max_length=8)
  ID_CCAA = models.CharField(max_length=8)

class Estado(models.Model):
  fecha = models.CharField(max_length=40)
  validas = models.DecimalField(default=0, decimal_places=0,max_digits=10)
  invalidas = models.DecimalField(default=0, decimal_places=0,max_digits=10)

