#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import re
import sys
import os
import os.path
from subprocess import call
import glob


def crea_enlaces_simbolicos(archivo):
	nombre_archivo = os.path.basename(archivo)
	try:
	    serie, temporada, _ = re.findall("(.*?)S(\d{2})E(\d{2})", nombre_archivo.replace(".", " "))[0]
	    serie, temporada = serie.strip(), temporada.strip()
	    call(["mkdir", "-p", "/mnt/TOURO/shows/{}/Season {}/".format(serie, temporada)])
	    destino = "/mnt/TOURO/shows/{}/Season {}/{}".format(serie, temporada,
							    nombre_archivo)
	except:
	    destino = "/mnt/TOURO/peliculas/{}".format(nombre_archivo)
	    
	if not call(["ln", "-s", os.path.abspath(archivo),
		       destino]):
	    print "{}".format(destino)

if len(sys.argv) == 2:
	archivo = sys.argv[1]
	if os.path.isdir(archivo):
		os.chdir(archivo)
		tipos = ("*.mkv", "*.mp4")
		archivos = [y for x in tipos for y in glob.glob(x)]
		for archivo in archivos:
			crea_enlaces_simbolicos(archivo)
	else:
		crea_enlaces_simbolicos(archivo)
else:
	sys.exit(1)

