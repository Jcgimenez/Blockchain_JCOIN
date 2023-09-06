# Blockchain_JCOIN# README.md - Creación de una Criptomoneda

Este repositorio contiene un proyecto de Python para crear una criptomoneda básica utilizando la tecnología de cadena de bloques. La criptomoneda se denomina "JCOIN" y se implementa con la ayuda del framework Flask para crear una aplicación web que admite operaciones de minería de bloques, transacciones y descentralización de la cadena de bloques.

## Parte 1 - Crear la Cadena de Bloques

En esta sección, se define la estructura básica de la cadena de bloques y se implementan las operaciones esenciales para su funcionamiento.

### Clase Blockchain

- `Blockchain` es la clase principal que representa la cadena de bloques.
- `create_block(proof, previous_hash)`: Crea un nuevo bloque en la cadena con un cierto nivel de "prueba" y un hash anterior.
- `get_previous_block()`: Obtiene el bloque más reciente en la cadena.
- `proof_of_work(previous_proof)`: Realiza la prueba de trabajo para encontrar un número que cumpla con ciertos requisitos.
- `hash(block)`: Calcula el hash de un bloque dado.
- `is_chain_valid(chain)`: Verifica la integridad de la cadena de bloques.
- `add_transaction(sender, receiver, amount)`: Agrega una nueva transacción a la lista de transacciones pendientes.
- `add_node(address)`: Agrega un nuevo nodo a la red.
- `replace_chain()`: Reemplaza la cadena actual por la cadena más larga en la red.

## Parte 2 - Minado de un Bloque de la Cadena

Esta parte se enfoca en el proceso de minería de un nuevo bloque en la cadena de bloques.

### Flask y Operaciones de la Aplicación Web

- `Flask` se utiliza para crear una aplicación web que interactúa con la cadena de bloques.
- `mine_block()`: Permite a los usuarios minar un nuevo bloque.
- `get_chain()`: Obtiene la cadena de bloques completa.
- `is_valid()`: Verifica la validez de la cadena de bloques.
- `add_transaction()`: Agrega una nueva transacción a la cadena de bloques.
- `node_address`: Representa la dirección única de este nodo en la red.

## Parte 3 - Descentralizar la Cadena de Bloques

La última sección se centra en la descentralización de la cadena de bloques y cómo se conectan y sincronizan los nodos.

- `connect_node()`: Permite a un nodo conectarse con otros nodos en la red.
- `replace_chain()`: Reemplaza la cadena local con la cadena más larga de la red.

## Ejecución de la Aplicación

Para ejecutar la aplicación de la cadena de bloques JCOIN, se utiliza el método `app.run()`. La aplicación escucha en el puerto 5000 y puede ser accedida a través de una interfaz web.

Asegúrese de tener Flask y las dependencias necesarias instaladas antes de ejecutar la aplicación.

```python
app.run(host='0.0.0.0', port=5000)
```

## Uso

Puede utilizar las siguientes rutas en la aplicación web para interactuar con la cadena de bloques JCOIN:

- `/mine_block`: Minar un nuevo bloque.
- `/get_chain`: Obtener la cadena de bloques completa.
- `/is_valid`: Verificar la validez de la cadena de bloques.
- `/add_transaction`: Agregar una nueva transacción a la cadena de bloques.
- `/connect_node`: Conectar con otros nodos en la red.
- `/replace_chain`: Reemplazar la cadena local con la cadena más larga de la red.

Asegúrese de que la aplicación esté en funcionamiento antes de usar estas rutas.

Este proyecto es una implementación simple de una cadena de bloques y tiene fines educativos. Para proyectos en producción, se requiere una seguridad y robustez adicionales.
