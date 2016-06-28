# SEGTI_2.0
Practica de la asignatura de seguridad

## Getting Started

The python hmac-sha512.py is a practice script for doing a better one for this practice. The main one would be **hmac-sha512_efecto_avalancha.py**.

### Prerequisities

To run this script you will need python3, and the following librarires:

* os
* random
* copy
* hmac
* hashlib
* statistics
* scipy
* warnings
* numpy
* matplot
* math

To install this libraries I recommend using the python package manager PIP, an example would be:

```
pip install python-scipy
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

You just have to follow the steps given by console, introduce always integers.

```
python hmac-sha512_efecto_avalancha.py
Introduzca el numero mayor que 0 de veces que quiere cambiar la clave:
1000
Introduzca la cantidad mayor que 0 de veces que quiere cambiar 1 byte en el string a comparar:
100
Introduzca el tamaño de la clave a utilizar para el algoritmo:
128
```

### Simple example of the default test

This is a simple example on how to use the script. Being all the values positive and integers, you can change all the iterations numbers. The key space is recommendable to be 128, any higher will not increase the security. 

```
python hmac-sha512_efecto_avalancha.py
Introduzca el numero mayor que 0 de veces que quiere cambiar la clave:
0
Introduzca la cantidad mayor que 0 de veces que quiere cambiar 1 byte en el string a comparar:
0
Introduzca el tamaño de la clave a utilizar para el algoritmo:
0
Usaremos los valores por defecto: clave = 128, numero_claves = 1000, numero_iterciones = 100
...
```

## Built With

* Python

## Authors

* **Alberto Revuelta Arribas** - *Initial work* - [kamigari](https://github.com/kamigari)


## License

This project is licensed under the GNU License - see the [LICENSE.md](LICENSE.md) file for details

