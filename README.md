# CYKToolset

## Resumen

Este proyecto está diseñado para transformar una Gramática Libre de Contexto en Forma Normal de Chomsky y luego utilizar el algoritmo CYK para analizar una oración dada. Consiste en tres componentes principales:

1. GrammarCNFTransformer: Una utilidad para convertir cualquier GLC en FNC, lo cual es necesario para el algoritmo CYK.
2. CYKGrammarParser: Una implementación del algoritmo de análisis CYK que verifica si una oración pertenece al lenguaje definido por la gramática.
3. Programa Principal: El punto de entrada para cargar una gramática, transformarla y probar oraciones para determinar si pertenecen al lenguaje.

## Estructura del Proyecto

- Chomsky.py: Contiene la clase GrammarCNFTransformer utilizada para convertir una GLC a FNC.
- Cyk.py: Contiene la clase CYKGrammarParser utilizada para analizar oraciones mediante el algoritmo CYK.
- main.py: El script principal que coordina la conversión a FNC y el proceso de análisis.
- test_grammar.json: Un archivo JSON que contiene la GLC de entrada que se utilizará para la conversión a FNC y el análisis.

## Características

1. Conversión de GLC a FNC:

  - La clase GrammarCNFTransformer lee una GLC desde un archivo JSON y aplica una serie de transformaciones para convertirla en FNC. La FNC es necesaria para un análisis eficiente con el algoritmo CYK.

2. Análisis CYK:

  - La clase CYKGrammarParser implementa el algoritmo CYK, que utiliza un enfoque ascendente para determinar si una oración puede ser generada por la gramática en FNC.
  - Genera un árbol de análisis para visualizar el proceso de análisis.

## Cómo Ejecutar

Requisitos Previos:

- Python 3.x
- graphviz para generar el gráfico del árbol de análisis (se puede instalar con pip install graphviz).

Ejecución del Programa:

Asegúrate de que la gramática de entrada esté en input.json en un formato JSON válido.

Ejecuta el programa principal utilizando el siguiente comando:
```bash
python main.py
```
El programa solicitará una oración para analizar e indicará si la oración pertenece al lenguaje definido por la gramática de entrada.

Una oracion de ejemplo puede ser "she cooks with a cat" que esta dentro del lenguaje y por consiguiente, es aceptada.

## Ejemplo

Crea un archivo test_grammar.json con tu GLC, como:
```bash
{
    "VARIABLES": ["S", "A", "B"],
    "TERMINALES": ["a", "b"],
    "INICIAL": "S",
    "REGLAS": {
        "S": ["A B", "B"],
        "A": ["a"],
        "B": ["b"]
    }
}
```
Ejecuta el programa, y este mostrará la gramática en FNC, analizará una oración y generará un árbol de análisis si la oración es aceptada.

## Salida

El programa mostrará la gramática convertida a FNC.

Imprimirá la tabla CYK utilizada en el análisis.

Si la oración pertenece al lenguaje, se generará un árbol de análisis como un archivo PNG.

## Notas

La gramática de entrada debe proporcionarse en formato JSON con secciones para VARIABLES, TERMINALES, INICIAL y REGLAS.

El convertidor a FNC eliminará producciones epsilon, producciones unitarias y reducirá producciones largas para garantizar que la gramática cumpla con los requisitos de la FNC.

## Dependencias

- Python 3.x
- graphviz para la visualización.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT.
