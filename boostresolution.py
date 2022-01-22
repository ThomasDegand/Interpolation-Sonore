from numba import jit, cuda
import numpy as np
import matplotlib.pyplot as plt

@jit
def d(Y, x):
    return (Y[x-3]+8*Y[x-2]-115*Y[x-1]+115*Y[x+1]-8*Y[x+2]-Y[x+3])/192

@jit
def mid(Y0):
    n0 = len(Y0)
    Y1 = [d(Y0, x) for x in range(3, n0-3)]
    n1 = len(Y1)
    Y2 = [d(Y1, x) for x in range(3, n1-3)]
    n2 = len(Y2)
    Ydemi = np.zeros(2*n0)
    for i in range(6, 2*(n0-12), 2):
        Ydemi[i] = Y0[i//2]
    for i in range(6, 2*(n0-13), 2):
        Ydemi[i+1] = (8*(Y0[i//2]+Y0[1 + (i//2)])+4*(Y1[i//2]-Y1[1 + (i//2)])+2*(Y2[i//2]+Y2[1 + (i//2)]))/16
    return Ydemi


import wave
namee = input("Nom du wav? ")
fichier = wave.open(namee, 'r')

channels = fichier.getnchannels()
print("channels:"+str(channels))
width = fichier.getsampwidth()
print("width:"+str(width))
frequency = fichier.getframerate()
print("frequency:"+str(frequency))
N = fichier.getnframes()
print("N:"+str(N))
ftype = fichier.getcomptype()
fname = fichier.getcompname()

frames = np.frombuffer(fichier.readframes(N), dtype="int16") #Nombre de frame depuis le curseur
fichier.close()

frames.resize(N,2)

#pas = 1/frequency

XL = frames[:,0]/1.3
XR = frames[:,1]/1.3

XLdemi = mid(XL)
XRdemi = mid(XR)

XLhex = np.array(XLdemi, dtype="int16")
XRhex = np.array(XRdemi, dtype="int16")
fichier = wave.open(namee[:-4]+"_x2.wav", 'wb')
fichier.setnchannels(2)
fichier.setsampwidth(2)
fichier.setframerate(frequency*2)
fichier.setnframes(N*2)
data = np.concatenate((XLhex,XRhex))
data.resize(2, N*2)
data = data.transpose()
data = data.tobytes()
fichier.writeframes(data)
fichier.close()

##X = np.arange(60)
##Y = np.cos(X)
##Xdemi = np.arange(120)
##Ydemi = mid(Y)
##Xquart = np.arange(240)
##Yquart = mid(Ydemi)
##
##plt.stem(Xquart, Yquart, markerfmt ='rx', linefmt='r')
##plt.stem(X*4, Y, markerfmt ='gx', linefmt='g')
##plt.show()
