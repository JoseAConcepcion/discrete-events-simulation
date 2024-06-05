import random 
import math

#Generacion de una uniforme en (0,1)
def Uniform():
    return random.random()

#Generacion de una uniforme en (a,b)
def UniformInterval(a:float, b:float):
    return a+(b-a)*Uniform()

#Generacion de una Bernoulli con probabilidad de exito p
def Bernoulli(p:float):
    gen:float = Uniform()
    if(gen<p): return 1
    else: return 0

#Generacion de una Binomial con parametros n y p
def Binomial(n:int, p:float):
    count:int = 0
    for i in range(n):
        if(Bernoulli(p)): count+=1
    return count

#Generacion de una Poisson con parametro l
def Poisson(l:float):
    count:int = 0
    acum:float = 1
    while acum >= math.exp(-l):
        U = Uniform()
        acum*=U
        count +=1
    return count-1

#Generacion de una Exponencial con parametro l
def Exponential(l:float):
    return -1/l*math.log(1-Uniform())

#Generacion de una Gamma con parametros n y l
def Gamma(n:int, l:float):
    acum:float = 1
    for i in range(n):
        acum*=Uniform()
    return -1/l*math.log(acum)
