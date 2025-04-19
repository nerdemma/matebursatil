mercados y valores argentinos
-----------------------------

es una api y serie de scripts para el acceso a las ultimas cotizaciones del mercado bursatil
argentino, la misma es implementada en el lenguaje de programacion python y bash mediante las librerias de scrapping, beautiful soup y expresiones regulares Regex. 

en primera instancia, esta aplicacion es utilizada en la terminal linux/unix la cual puede utilizarse para sus aplicaciones de escritorio.

como funciona?
al ejecutarse el script get_share.py, el script obtiene las cotizaciones realizando scraping y guardandolo en un archivo .json, este script puede configurarse para obtener las cotizaciones cada cierta cantidad de tiempo preestablecida, mediante el servicio crontrab. 

como obtener la informacion?
ejecutando el script ./get_marketshare GGAL obtenemos la cotizacion de "Banco Galicia y Buenos Aires" como para tomar un ejemplo, en caso de no encontrar la cotizacion que estamos buscando nos devolvera "No encontrado!". 

Renuncia de Responsabilidad: 
Esta aplicacion proporciona información con fines educativos e informativos. la cual no constituye asesoramiento financiero, legal o de inversion.
No garantizamos la exactitud ni la integridad de los datos presentados. 
El uso de esta aplicacion es bajo su propio riesgo. Siempre consulte a un profesional antes de tomar desiciones financieras. 

