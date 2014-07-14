#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import re
import sys
import os
import os.path
from os.path import join
import glob

shows_folder = "/mnt/TOURO/shows/"
films_folder = "/mnt/TOURO/peliculas/"


def crea_enlaces_simbolicos(archivo):
    nombre_archivo = os.path.basename(archivo)
    target = None
    try:
        serie, temporada, _ = re.findall("(.*?)S(\d{2})E(\d{2})",
                                         nombre_archivo.replace(".", " "))[0]
        serie, temporada = serie.strip(), temporada.strip()
        os.makedirs(join(shows_folder, "{}/Season {}/").format(serie, temporada))
    except OSError:
        #Folder exists
        pass

    except TypeError:
        #Regular expression fail
        target = join(films_folder, "{}").format(nombre_archivo)
    finally:
        if not target:
            target = join(shows_folder, "{}/Season {}/{}").format(serie, temporada,
                                                                   nombre_archivo)

    if target:
        os.symlink(os.path.abspath(archivo), target)
        print("{}".format(target))


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
