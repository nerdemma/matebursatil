#!/bin/bash

#definir colores
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'



imprimir_variacion() {
variacion=$1
variacion_clean=$(echo "$variacion" | tr -d '%' | tr ',' '.')


if [[ "$variacion_clean" =~ ^-?[0-9]+([.][0-9]+)?$ ]]; then
        if (( $(echo "$variacion_clean > 0" | bc -l) )); then
            echo -e "${GREEN}${variacion_clean} ▲ ${NC}"
        elif (( $(echo "$variacion_clean < 0" | bc -l) )); then
            echo -e "${RED}${variacion_clean} ▼ ${NC}"
        else
            echo "$variacion_clean"
        fi
    else
        echo "NaN"
    fi
   
}


function main()
{
simbolo="$1"

if [ -z "$simbolo" ]; then
	echo "Uso: obtener_cotizacion: SIMBOLO"	
	return 1
fi
	
result=$(jq -c --arg simbolo "$simbolo" '.[] | select(.ticker == $simbolo)' data/cotizaciones.json)

if [ -z "$result" ]; then
	echo "Simbolo '$simbolo' no encontrado"	
	return 1
fi

	ticker=$(echo "$result" | jq -r '.ticker')
    #cotizacion=$(echo "$result" | jq -r '.cotizacion')
    variacion=$(echo "$result" | jq -r '.variacion')

echo "$ticker" "$(imprimir_variacion "$variacion")"
}



main "$@" #obtener cotizacion, variable enviada por argumento. 





