#Script para la conversion de multiples archivos GRID de temperatura media
#de los ELCCA en unico archivo de texto delimitado por espacios
#Hecho por Jose I. Alvarez Francoso
from __future__ import division
import sys
import datetime
from osgeo import gdal, ogr, osr
from osgeo.gdalconst import GA_ReadOnly, GA_Update
 # Funcion para sobreescribir el mensaje de porcentaje completado 
def restart_line():
 sys.stdout.write('\r')
 sys.stdout.flush()
 # Funcion principal
def elcca2txt_tmed(variable,archivo_salida):
 print 'Iniciado a las: ' + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') 
 archivo_salida2 = open(archivo_salida, 'a')
 for id_modelo in range(1,5):
  if id_modelo == 1:
   modelo_name = "cgcm3"
  elif id_modelo == 2:
   modelo_name = "esm1"
  elif id_modelo == 3:
   modelo_name = "gfdl"
  elif id_modelo == 4:
   modelo_name = "miroc"
  else:
   print "Error en el nombre del modelo"
   raise SystemExit  
  for id_escenario in range(1,5):
   if id_escenario == 1:
    esc_name = "rcp26.ws"
   elif id_escenario == 2:
    esc_name = "rcp45.ws"
   elif id_escenario == 3:
    esc_name = "rcp60.ws"
   elif id_escenario == 4:
    esc_name = "rcp85.ws"
   else:
    print "Error en el bucle escenario"
    raise SystemExit 
   esc_txt = esc_name[:5]	
   for id_periodo in range (1,4):
    if id_periodo == 1:
     per_name = "d2011-2040.ws"
     per_name2 = "11-40c"
    elif id_periodo == 2:
     per_name = "d2041-2070.ws"
     per_name2 = "41-70c"
    elif id_periodo == 3:
     per_name = "d2071-2099.ws"
     per_name2 = "71-99c"
    else:
     print "Error en el bucle periodo"
     raise SystemExit
    for mes in range (1,13):
     mes_name = variable + per_name2 + str(mes)
     archivo = "J:/proyectos/GLOBAL_REDIAM_3/datos/" + modelo_name + "/" + esc_name + "/" + modelo_name + "-" + esc_txt + "-" + variable + ".ws/" + per_name + "/" + mes_name + "/" "w001001.adf"
  #  archivo = archivo.encode('utf-8')
     dataset = gdal.Open( archivo, GA_ReadOnly )
     band = dataset.GetRasterBand(1)
     cols = dataset.RasterXSize
     rows = dataset.RasterYSize
     x = 100419.120
     y = 4288700.548
     # Iteramos filas y columnas y definimos valor
     data = []
     band_data = band.ReadAsArray(0, 0, cols, rows)
     data.append(band_data)
     id_punto = 1
     for r in range(0,rows,10):
      for c in range(0,cols,10):
       # Gestion de los null
       valor = data[0][r,c]
       if valor > -100:
        archivo_salida2.write(str(id_punto) + " " + str(x) + " " + str(y) + " " + str(id_modelo) + " " + str(id_escenario) + " " + str(id_periodo) + " " + str(mes) + " " + str(valor) + "\n")
       x = x + 2000
       id_punto+=10
      y = y - 2000
#     x = 100419.120
     procesado = "Modelo: " + modelo_name + "---" + "Escenario: " + esc_name + "---" + "Periodo: " + per_name2 [:5] + "---" + "Mes:" + str(mes) + "id_punto:" + str(id_punto)
     sys.stdout.write(' Procesando: ' + procesado)
     sys.stdout.flush()
     restart_line() 
 archivo_salida2.close()
 print 'Finalizado a las: ' + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
if __name__ == '__main__':
 # El usuario  tiene que definir la ruta de archivos de entrada y la ruta y el nombre del archivo de salida en una cadena de texto
 if len(sys.argv) < 3 or len(sys.argv) > 3:
  print "uso: <variable y cadena con ruta_nombre de archivo txt>"
  raise SystemExit
 variable = sys.argv[1]
 archivo_salida = sys.argv[2]
 elcca2txt_tmed(variable,archivo_salida)
 raise SystemExit