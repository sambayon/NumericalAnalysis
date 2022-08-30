import numpy as np
# Partimos de la ecuación
# y' = exp(-y)*t^3, y(0) = 0
# y(t)=ln(t^4/4+1)


## El objetivo es integrar usando Euler

def y_prima(y,t):
    resultado = np.exp(-y)*t**3
    return(resultado)
    
def resuelve_y(y0,t0,T,N):
    t = [t0] # Lista con elementos de t
    y = [y0] # Lista con elementos de y
    dt = (T-t0)/N # paso temporal
    while t[-1]<T: # Mientras t no haya alcanzado T (miro el el último elemento)
        yN = y[-1] + dt*y_prima(y[-1],t[-1])
        tN = t[-1] + dt
        y.append(yN)
        t.append(tN)
    resultado = [np.array(t),np.array(y)]
    return(resultado) # Retorno lista con listas de t e y
    
def y_exacta(t):
    resultado = np.log(t**4/4 + 1)
    return(resultado)
    
y0 = 0
t0 = 0
T = 10
N_lista = [50,100,500,1000]
resultados = []

for N in N_lista:
    resultado = resuelve_y(y0,t0,T,N)
    resultados.append(resultado) # Guardo las integraciones en una lista

import matplotlib.pyplot as plt

for i in range(len(N_lista)):
    resultado = resultados[i] # agarro el resultado i-esimo
    N = N_lista[i]
    t = resultado[0]
    y = resultado[1]
    plt.plot(t,y,label=N)
    
# Calculo la solución exacta
tE = np.arange(t0,T,0.001)
yE = y_exacta(tE)
plt.plot(tE,yE,label='Exacta')
plt.xlabel('Tiempo')
plt.ylabel('y')
plt.legend()
plt.savefig('pa_evoluciony.png')

# Error en general
plt.figure()
for i in range(len(N_lista)):
    resultado = resultados[i] # agarro el resultado i-esimo
    N = N_lista[i]
    t = resultado[0]
    y = resultado[1]
    yE = y_exacta(t)
    plt.plot(t,abs(y-yE),label=N)
    
# Calculo la solución exacta
plt.xlabel('Tiempo')
plt.ylabel('y-yE')
plt.legend()
plt.savefig('pa_errory.png')

# Error en t=T=10
plt.figure()
errores = []
for i in range(len(N_lista)):
    resultado = resultados[i] # agarro el resultado i-esimo
    N = N_lista[i]
    t = resultado[0]
    y = resultado[1][-1] # Lo calculo en el ultimo valor en todos los casos
    yE = y_exacta(t[-1])
    errores.append(abs(y-yE))

plt.plot(1/np.array(N_lista),errores)
plt.xlabel('1/N')
plt.ylabel('y(T)-yE(T)')
plt.savefig('pa_errorenT.png')

#%%

# La ecuación es 
# y'' = -5y -y'
# y(0) = 1
# y'(0) = 0
# Como la quiero en formato de primero orden
# y1=y, y2 = y'
## y1' = y2
## y2' = -5*y1 -y2
## V = [y1,y2]
import numpy as np
import matplotlib.pyplot as plt
def V_prima(V):
    resultado = np.array([V[1],-5*V[0]-V[1]])
    return(resultado)
    
def euler_A(t0,V0,T,N):
    t = [t0]
    V = [V0]
    dt = (T-t0)/N
    while t[-1] < T:
        VN = V[-1] + dt*V_prima(V[-1]) 
        tN = t[-1] + dt
        t.append(tN)
        V.append(VN)
    resultado = [t,V]
    return(resultado)

def euler_B(t0,V0,T,N):
    t = [t0]
    V = [V0]
    dt = (T-t0)/N
    while t[-1] < T:
        # Acá para poder calcular voy a tener que desarmar V
        VO = V[-1] # O de old
        y1O = VO[0]
        y2O =  VO[1]
        VpO = V_prima(VO)
        y1N = y1O + VpO[0]*dt
        Vp1 = V_prima(np.array([y1N,y2O]))
        y2N = y2O + Vp1[1]*dt
        VN = np.array([y1N,y2N])
        tN = t[-1] + dt
        t.append(tN)
        V.append(VN)
    resultado = [t,V]
    return(resultado)

def euler_C(t0,V0,T,N):
    t = [t0]
    V = [V0]
    dt = (T-t0)/N
    while t[-1] < T:
        # Acá para poder calcular voy a tener que desarmar V
        VO = V[-1] # O de old
        y1O = VO[0]
        y2O =  VO[1]
        VpO = V_prima(VO)
        y2N = y2O + VpO[1]*dt
        Vp1 = V_prima(np.array([y1O,y2N]))
        y1N = y1O + Vp1[0]*dt
        VN = np.array([y1N,y2N])
        tN = t[-1] + dt
        t.append(tN)
        V.append(VN)
    resultado = [t,V]
    return(resultado)


def dame_yt(integracion):
    t = integracion[0]
    V = integracion[1]
    y = []
    for i in range(len(V)):
     y.append(V[i][0])
    resultado = [np.array(t),np.array(y)]
    return(resultado)

def y_exacta(t):
    w = np.sqrt(19/4)
    phi = np.arctan2(1,-2*w)
    #phi = np.arctan(1/(-2*w))
    A = 1/np.cos(phi)
    resultado = A*np.exp(-t/2)*np.cos(w*t+phi)
    return(resultado)

y10 = 1
y20 = 0
V0 = np.array([y10,y20])
t0 = 0
T = 5
N = 100

euA = euler_A(t0,V0,T,N)
euB = euler_B(t0,V0,T,N)
euC = euler_C(t0,V0,T,N)

ytA = dame_yt(euA)
tA = ytA[0]
yA = ytA[1]

ytB = dame_yt(euB)
tB = ytB[0]
yB = ytB[1]

ytC = dame_yt(euC)
tC = ytC[0]
yC = ytC[1]

tE = np.arange(t0,T,1/10**3)
yE = y_exacta(tE)

plt.plot(tA,yA,label='A')
plt.plot(tB,yB,label='B')
plt.plot(tC,yC,label='C')
plt.plot(tE,yE,label='Exacta')
plt.legend()
plt.xlabel('Tiempo')
plt.ylabel('y')
plt.savefig('pb_ABC.png')


plt.figure()
N_lista = np.array([100,500,1000])
resultados = []
for N in N_lista:
    integracion = euler_B(t0,V0,T,N)
    yt = dame_yt(integracion)
    resultados.append(yt)
    
for i in range(len(N_lista)):
    resultado = resultados[i]
    t = resultado[0]
    y = resultado[1]
    yE = y_exacta(t)
    plt.plot(t,abs(y-yE),label=N_lista[i])

plt.xlabel('Tiempo')
plt.ylabel('Error')
plt.legend()
plt.savefig('pb_errort.png')