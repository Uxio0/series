#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import re
import sys
import os
import os.path
from os.path import join
import glob

shows_folder = "/mnt/TOURO/shows/"
#shows_folder = "/home/shows"
films_folder = "/mnt/TOURO/peliculas/"

patterns = (
    r"(.*?)S(\d{2})E(\d{2})",   # American S01E03
    r"(.*?)(\d{1,2})x(\d{2})",  # English 1x03
)


def crea_enlaces_simbolicos(archivo):
    nombre_archivo = os.path.basename(archivo)
    target = None
    serie = None
    for pattern in patterns:
        result = re.findall(pattern,
                            nombre_archivo.replace(".", " "))
        if result:
            break

    if result:
        # Doesn't need episode for XMBC folder structure
        serie, temporada, _ = result[0]
        serie, temporada = serie.strip(), temporada.strip()
        target = join(shows_folder, "{}/Season {}/{}").format(serie, temporada,
                                                              nombre_archivo)
        try:
            os.makedirs(join(shows_folder, "{}/Season {}/").format(serie,
                                                                   temporada))
        except OSError:
            #Folder exists
            pass
    elif archivo:
        #Film
        target = join(films_folder, "{}").format(nombre_archivo)
    else:
        print('Error, file is empty')

    if target:
        try:
            os.symlink(os.path.abspath(archivo), target)
        except OSError:
            #Symlink exists
            pass
        print("{}".format(target))


if len(sys.argv) == 2:
    archivo = sys.argv[1]
    if os.path.isdir(archivo):
        os.chdir(archivo)
        tipos = ("*.mkv", "*.mp4", "*.avi")
        archivos = [y for x in tipos for y in glob.glob(x)]
        for archivo in archivos:
            crea_enlaces_simbolicos(archivo)
    else:
        crea_enlaces_simbolicos(archivo)
else:
    sys.exit(1)
