#!usr/bin/python

import os, random, copy, hmac, hashlib, statistics, scipy, warnings
import numpy as np
import matplotlib.pyplot as plt

from scipy import stats
from scipy.stats import norm
from math import sqrt

def quitar_warnings_molestos():
    warnings.filterwarnings('ignore', 'The iteration is not making good progress')
    warnings.filterwarnings('ignore', 'divide by zero encountered in log')
    warnings.filterwarnings('ignore', 'invalid value encountered in subtract')
    warnings.filterwarnings('ignore', 'Source ID')
    warnings.filterwarnings('ignore', 'invalid value encountered in sqrt')

def limit_by_confidence(list):
    """Returns if we achived the 95 confidence by a property of the normal distribution"""
    if len(list) > 2:
        data = np.asarray(list)
        mu, std = norm.fit(list)
        return std * 100 ==  1.959964

def normal_fit(list):
    """Returns the normal fit for the given list"""
    data = np.asarray(list)
    mu, std = norm.fit(list)
    plt.figure(0)
    plt.hist(data, bins=25, normed=True, alpha=0.6, color='g')
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
    plt.title(title) 
    plt.savefig('normal-fit.png', bbox_inches='tight')
    

def get_distribution(list):
    """Returns al que posible probability distributions for the given list"""
    size = len(list)
    x = scipy.arange(size)
    y = scipy.int_(scipy.round_(scipy.stats.vonmises.rvs(5,size=size)*255))
    plt.figure(1)
    h = plt.hist(y, bins=range(256), color='w')
    dist_names = ['gamma', 'beta', 'rayleigh', 'norm', 'rayleigh']
    for dist_name in dist_names:
        dist = getattr(scipy.stats, dist_name)
        param = dist.fit(y)
        pdf_fitted = dist.pdf(x, *param[:-2], loc=param[-2], scale=param[-1]) * size
        plt.plot(pdf_fitted, label=dist_name)
        plt.xlim(0,255)
    plt.legend(loc='upper right')
    plt.savefig('distribuciones.png', bbox_inches='tight')

def histogram(list):
    """Returns the histogram of the list given"""
    x = np.asarray(list)
    plt.figure(2)
    n, bins, patches = plt.hist(x, 20, normed=1, facecolor='g', alpha=0.75)
    plt.ylabel('Number of occurences')
    plt.xlabel('Hamming distances')
    plt.title('Histogram of Avalanche Effect')
    plt.grid(True)
    plt.savefig('histograma.png', bbox_inches='tight')

def getMessage(size=128):
    """Returns a randomly distributed bytes object with leght size, by default 128"""
    return os.urandom(size)

def getKey(size=128):
    """Returns a Key of 0's equal to the size"""
    Key = ''
    for i in range(size):
        Key = Key + '0'
    return Key

def hammingDistance(s1, s2):
    """Returns the Hamming distance between equal-length sequences"""
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(list(int(l != r) for l, r in zip(s1, s2)))

def check_list(list, i):
    """Checks if the first element of the list is 255 and keeps the elements in range (0-255)"""
    if list[i] == 255:
        list[i] = 0
    else:
        list[i] = list[i] + 1        
    
def avalanche_effect_Message(numIter = 1000, numIterAvalanche = 100):
    """Returns the hamming distances of the resulting HMAC from the key '', two random inputs which differ in only one byte and the function hash SHA-512, changing the message by one byte from last to first"""
    Key = str.encode('') #Metemos la clave secreta que vamos a usar, en este caso es un string vacio
    histograma = {}
    significaciones = {}
    resultados = {}
    Input1 = getMessage()
    m = len(Input1) - 1
    for i in range(numIter):
        if m == 0:
            m = len(Input1) - 1
        k = len(Input1) - 1
        for j in range(numIterAvalanche):
            if k == 0:
                k = len(Input1) - 1
            histogramaAvalancha = []
            signifAvalancha = []
            ultimaIteracion = 0
            Input2 = list(copy.copy(Input1))
            check_list(Input2, k)
            Input2 = bytes(Input2)
            sign1 = hmac.new( Key, Input1, hashlib.sha512).hexdigest()
            sign2 = hmac.new( Key, Input2, hashlib.sha512).hexdigest()
            hamming_distance = hammingDistance(sign1, sign2)
            histogramaAvalancha.append(hamming_distance)
            signif = (hamming_distance)/len(sign1)
            signifAvalancha.append(signif)
            histograma.update({i : {j : {ultimaIteracion : histogramaAvalancha}}})
            significaciones.update({i : {j : {ultimaIteracion : signifAvalancha}}})
            print(get_confiance(histogramaAvalancha))
            k = k - 1
            if limit_by_confidence(avalanche_effect_to_list(significaciones)) == True:
                break
        check_list(list(Input1), m)
        Input1 = bytes(Input1)
        m = m - 1
    return histograma

def avalanche_effect_Key(Key = 128, numIter = 1000, numIterAvalanche = 100):
    """Returns the hamming distances of the resulting HMAC from the key '0'x size, message '0123456789ABCDEF' and the function hash SHA-512, changing the key one byte from last to first"""
    Key1 = getKey(Key)
    Key1 = str.encode(Key1)
    m = len(Key1) - 1
    Message = str.encode('0123456789ABCDEF')
    histograma = {}
    significaciones = {}
    resultados = {}
    for i in range(numIter):
        histogramaAvalancha = []
        signifAvalancha = []
        sigMayorAva = False
        ultimaIteracion = 0
        k = len(Key1) - 1
        for j in range(numIterAvalanche):
            Key2 = list(copy.copy(Key1))
            check_list(Key2, k)
            Key2 = bytes(Key2)
            k -= 1
            if k == -1:
                k = len(Key1) - 1
            sign1 = hmac.new( Key1, Message, hashlib.sha512).hexdigest()
            sign2 = hmac.new( Key2, Message, hashlib.sha512).hexdigest()
            hamming_distance = hammingDistance(sign1, sign2)
            histogramaAvalancha.append(hamming_distance)
            signif = (hamming_distance)/len(sign1)
            signifAvalancha.append(signif)
            histograma.update({i : {j : histogramaAvalancha}})
            significaciones.update({i : {j  : signifAvalancha}})
            if limit_by_confidence(avalanche_effect_to_list(significaciones)) == True:
                break
        Key1 = list(Key1)
        check_list(Key1, m)
        Key1 = bytes(Key1)
        m -= 1
        if m == -1:
            m = len(Key1) - 1
    return histograma, significaciones

def avalanche_effect_to_list(dict):
    histograma_general = []
    for key1, value1 in dict.items(): #Accedemos a la clave i  
        for key2, value2 in value1.items(): #Accedemos a la clave j
            for item in value2: #Accedemos a la lista del histogramade esa iteracion
                histograma_general.append(item) #Juntamos los valores para hacer un histograma con todos los valores estadisticos conseguidos 
    return histograma_general

def estadisticas(list):
    print ("La media aritmética es: {0}".format((statistics.mean(list))))
    print ("La desviación media respecto a la media aritmética es: {0}".format(statistics.median(list)))
    print ("La varianza es: {0}".format(statistics.variance(list)))
    print ("La La desviación típica es: {0}".format(statistics.stdev(list)))

def main():    
    numIter = int(input("Introduzca el numero mayor que 0 de veces que quiere cambiar la clave:\n"))
    numIterAva = int(input("Introduzca la cantidad mayor que 0 de veces que quiere cambiar 1 byte en el string a comparar:\n"))
    Key = int(input("Introduzca el tamaño de la clave a utilizar para el algoritmo:\n"))
    if Key > 0 and numIter > 0 and numIterAva > 0:
        resultado_dict, signif_dict = avalanche_effect_Key(Key, numIter, numIterAva)
    else:
        print('Usaremos los valores por defecto: clave = 128, numero_claves = 1000, numero_iterciones = 100')
        resultado_dict, signif_dict = avalanche_effect_Key()
    resultado_list = avalanche_effect_to_list(resultado_dict)
    print('Resultado de las distancias de Hamming:\n')
    estadisticas(resultado_list)
    histogram(resultado_list)
    normal_fit(avalanche_effect_to_list(signif_dict))
    get_distribution(resultado_list)

if __name__ == '__main__':
    quitar_warnings_molestos()
    main()
