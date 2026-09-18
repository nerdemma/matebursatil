Mate Bursatil
-----------------------------



Una API para tener al alcance las ultimas cotizaciones del MERVAL a traves de un fichero json, información actualizada cada 10 minutos. 

Funcionalidades
Lista las ultimas cotizaciones el mercado bursatil argentino mediante scraping a la fuente, esto es posible gracias a la libreria beautyful soup en python.  

Instalación
```
git clone https://github.com/nerdemma/matebursatil
cd matebursatil
./init.sh
```


Obtener Cotizacion Especifica
Es posible obtener la lista de cotizaciones en general asi como tambien una especifica mediante su simbolo, por ejemplo si quiero obtener la cotización de "Grupo Financiero Galicia" escribo el simbolo GGAL en la solicitud. 

Para obtener todas las cotizaciones. 
```
curl -i http://127.0.0.1:8000/shares
```
Para solo obtener la cotizacion de un solo titulo especifico.
```
curl -i http://127.0.0.1:8000/shares/GGAL
```
Dependencias 

fastapi
uvicorn
requests
beautifulsoup4
pydantic
pytest
httpx

Renuncia de Responsabilidad: 
Esta aplicacion proporciona información con fines educativos e informativos. la cual no constituye asesoramiento financiero, legal o de inversion.
No garantizamos la exactitud ni la integridad de los datos presentados. 
El uso de esta aplicacion es bajo su propio riesgo. Siempre consulte a un profesional antes de tomar desiciones financieras. 

