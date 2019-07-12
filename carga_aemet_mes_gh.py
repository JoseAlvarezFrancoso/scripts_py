#Autor-Jose I. Alvarez Francoso
import httplib
import json
import csv
import time
import io
import sys
def carga_aemet(inicio,fin,variable):
 conn = httplib.HTTPSConnection("opendata.aemet.es")
 headers = {
     'cache-control': "no-cache"
     }
 with io.open('ruta_archivo_estaciones', encoding='ISO 8859-1') as data_file:    
     data = json.load(data_file)
 archivo = open('ruta_csv' + variable + '_' + str(inicio) + '-' + str(fin) + '.csv','wb')
 fin2= int(fin) + 1
 inicio2 = int(inicio)
 for agno in range(inicio2, fin2):
  print ('Procesando agno :   ' + str(agno) + "..." + "___________________________________________________________________")
  i=-1
  for estacion in data:
   i=i+1
   codigo = data[i]["indicativo"]
   conn.request("GET", "/opendata/api/valores/climatologicos/mensualesanuales/datos/anioini/"+str(agno)+"/aniofin/"+str(agno)+"/estacion/"+codigo+"/?api_key=AQUI_VA_LA_API_KEY", headers=headers)
   res = conn.getresponse()
   if res:
 #  print('Estacion codigo :   ' + codigo )
    data1 = res.read()
    data2 = data1.decode("ISO 8859-1",'ignore')
    data3= json.loads(data2)
    res_state = data3['estado']
    if res_state == 200:
     conn.request("GET", data3['datos'], headers=headers)
     res= conn.getresponse()
     datos2 = res.read().decode('utf-8','ignore')
# Validar json. Aunque se espere 1 minuto, al hacer un cierto numero de peticiones, la API devuelve un 429 y el json es invalido, por lo que volver a hacer la peticion
     try:
	  json.loads(datos2)
	  datos3= json.loads(datos2)
	  wr = csv.writer(archivo, delimiter=';')
	  for item in datos3:
	   if variable in item:
	    print ('Processing station ' + codigo + ' and year ' + str(agno))
	    wr.writerow(([item['indicativo']]+[item['fecha']]+[item[variable]]))
     except ValueError as error:
	  print ('Processing year ' + str(agno))
	  print("invalid json: %s" % error)
	  print("I keep trying, hang on please...")
	  time.sleep(60)
	  i=i-1
    if res_state == 429:
	 print ('Processing year ' + str(agno))
	 time.sleep(60)
	 i=i-1
    if res_state == 404:
	 print ('No data for this station, I skip it...')
 # if i%10 == 0:
 #  time.sleep(60)
 archivo.close()
if __name__ == '__main__':
 # El usuario  tiene que definir agno inicio, fin y variable
 if len(sys.argv) < 4 or len(sys.argv) > 4:
  print "uso: <agno inicio><agno fin><variable:tm_mes,tm_max,tm_min>"
  raise SystemExit
 inicio = sys.argv[1] 
 fin = sys.argv[2]
 variable = sys.argv[3]
 carga_aemet(inicio,fin,variable)
 raise SystemExit