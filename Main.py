# -*- coding: utf-8 -*-
__author__ = 'RicardoMoya'

import ScrapBDFutbol as bd_futbol

# Obtengo los partidos de futbol de las temporadas anteriores
partidos = bd_futbol.get_partidos()

# Verifica si los partidos se están escribiendo correctamente
fichero = open('DataSetPartidos.txt', 'w')
fichero.write('idPartido::temporada::division::jornada::EquipoLocal::'
              'EquipoVisitante::golesLocal::golesVisitante::fecha::timestamp\n')

for value in partidos.values():
    print(f"Escribiendo partido: {value}")  # Muestra los partidos antes de escribir
    fichero.write('%s\n' % str(value))

fichero.close()