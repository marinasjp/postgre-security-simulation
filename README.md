# postgre-security-simulation
Simulación de un método de securización en PostgreSQL.

Como ejercicio adicional para el trabajo de la asignatura Protección de Sistemas y Servicios, he desarrollado este proyecto.
Es una simulación de los elementos básicos de la solución presentada en el ensayo  End-to-End Database Software Security de Denis Ulybyshev, Michael Rogers, Vadim Kholodilo y Bradley Northern.

# Pasos del código
El código hace los siguientes pasos:

1.	Los valores del archivo config.ini determinan el usuario que ejecuta la query y la query.
2.	PROSPEGQL determina qué columnas y tablas está pidiendo el usuario. 
3.	La función genera una ACL preguntando a la base de datos sobre los privilegios de estas tablas y columnas. 
4.	PROSPEGQL realiza la query a la base de datos para obtener los resultados
5.	Los resultados y la ACL se pasan a un generador de contenedores. 
6.	La respuesta contiene los resultados SQL y los privilegios de control de acceso cifrados. El usuario puede ver estos datos, guardarlos e incluso compartirlos. 
   
Por el momento, el código solo acepta una query de la estructura "SELECT \<columnas> FROM <tabla>".
