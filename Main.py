# -*- coding: utf-8 -*-
__author__ = 'RicardoMoya'

import ScrapBDFutbol as bd_futbol

# Obtengo los partidos de futbol de las temporadas anteriores
partidos = bd_futbol.get_partidos()

# Verifica si los partidos se están escribiendo correctamente
fichero = open('DataSetPartidos.txt', 'w')
fichero.write('idPartido,EquipoLocal,'
              'EquipoVisitante,golesLocal,golesVisitante,Temporada\n')

fichero.close()