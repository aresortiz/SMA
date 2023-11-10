# Vaccum Cleanear

El programa es un simulación de agentes (robots de limpieza) que se deben encargar de limpiar las celdas que se encuentren con basura dentro de un grid. Las siguientes carácteristicas pueden ser modificadas:
   * Habitación de MxN espacios
   * Número de agentes
   * Porcentaje de celdas inicialmente sucias
   * Tiempo máximo de ejecución.
   
Las celdas deben inicializar sucias en ubicaciones aleatorias del grid.
Todos los agentes empiezan en la celda [1,1].
En cada paso de tiempo:

- Si la celda está sucia, entonces aspira.
- Si la celda está limpia, el agente elije una dirección aleatoria para moverse (unas de las 8 celdas vecinas) y elije la acción de movimiento (si no puede moverse allí, permanecerá en la misma celda).
- Se ejecuta el tiempo máximo establecido.

Al finalizar los datos recopilados que se mostraran en la terminal serán los siguientes:

- Tiempo necesario hasta que todas las celdas estén limpias (o se haya llegado al tiempo máximo).
- Porcentaje de celdas limpias después del termino de la simulación.
- Número de movimientos realizados por todos los agentes.

