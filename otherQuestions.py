import numpy as np
import matplotlib.pyplot as plt
from orbit import *
from scipy.signal import argrelextrema

AU = 1.49597871e13 #cm
Msun = 1.989e33 #g
Mjup = 1.89813e30 #g
Day = 86164.0916 #seconds in a day
Rjup = 7.1492e9 #radius of jupiter in cm
Rs = 6.9599e10 #radius of sun in cm

#####Q2

# HD 80606 b orbit parameters from http://exoplanet.eu/catalog/hd_80606_b/#6832
# updated Aug. 16, 2014

t0 = 2454424.852*Day #JD
a = 0.449 * AU
e = 0.9332
i = np.radians(89.32)
W = np.radians(160.98) # or -19.02 http://adsabs.harvard.edu/abs/2014AAS...22341102W
w = np.radians(300.80)
m1 = 0.97 * Msun
m2 = 3.94 * Mjup

t1 = 2457235.5 #JD of Sep 1 2015 
t2 = 2457387.5 #JD of Dec 31 2015

#calculate range of time in seconds
JDs = np.arange(t1,t2,0.001)
ts = JDs*Day

p=[t0,a,e,i,W,w,m1,m2]
HD80606b=Orbit(p)
obs=HD80606b.calcObs(ts)
Rvs=obs[6]
#Rvs=np.append(Rvs,Rv)

plt.clf()
plt.plot(JDs ,Rvs/100.)
plt.xlabel("Julian date [days]")
plt.ylabel("Radial Velocity [m/s]")
plt.title("HD 80606 b")
plt.savefig("Q2.pdf")

f = open('results.out','w')
f.write("Extreme neg vel on: {}\n".format(JDs[argrelextrema(Rvs,np.less)]))
f.write("Extreme pos vel on: {}\n".format(JDs[argrelextrema(Rvs,np.greater)]))

'''
plt.clf()
plt.plot(JDs ,obs[0]/AU)
plt.xlabel("Julain date [days]")
plt.ylabel("Projected seperation [AU]")
plt.title("HD 80606 b")
plt.savefig("Q3.pdf")
'''

##### Q3 #####
f.write("minimum projected seperation on JD {}\n".format(JDs[argrelextrema(obs[0],np.less)]))

rpl = 0.98*Rjup
rs = 0.978*Rs
f.write("1/4 contact occurs on JD {}\n".format(JDs[argrelextrema(np.abs(obs[0]-rpl-rs),np.less)]))
f.write("2/3 Contact occurs on JD {}\n".format(JDs[argrelextrema(np.abs(obs[0]+rpl-rs),np.less)]))

f.close()


##### Q4 #####

paralax=0.01713 #arcsec \pm 0.00577
D=1./paralax #distance in PC

dt = 5.*365.256*Day
samples = np.random.random_sample(size=100)*dt 
samples = np.sort(samples)
epochs = samples + 2456863.5*Day #July 25 2014 Gaia's first science day

Gobs=HD80606b.calcObs(epochs)
Rcm, PAcm = Gobs[2], Gobs[3]
DRA, DDEC = (Rcm/(AU*D))*[-np.cos(PAcm),np.sin(PAcm)]*1000.

plt.clf()
f, axarr = plt.subplots(2, sharex=True)
axarr[0].plot(epochs/Day,DRA)
axarr[0].set_title('Reflex motion')
axarr[1].plot(epochs/Day,DDEC)
plt.xlabel("Julian date [days]")
plt.savefig("1time.pdf")

plt.clf()
plt.plot(DRA,DDEC,'kx')
plt.title('Reflex motion')
plt.xlabel("RA []")
plt.ylabel("DEC []")
plt.savefig('1radec.pdf')

'''
plt.clf()
f, axarr = plt.subplots(2, sharex=True)
axarr[0].plot(epochs/Day,y)
axarr[0].set_title('Reflex + parallax motion')
axarr[1].plot(epochs/Day,y)
plt.xlabel("Julian date [days]")
plt.savefig("2time.pdf")

plt.clf()
plt.plot(ra,dec)
plt.title('Reflex + parallax motion')
plt.xlabel("RA []")
plt.ylabel("DEC []")
plt.savefig('2radec.pdf')
'''

DRA = DRA + 46.98*samples/(365.256*Day)
DDEC = DDEC + 6.92*samples/(365.256*Day)

plt.clf()
f, axarr = plt.subplots(2, sharex=True)
axarr[0].plot(epochs/Day,DRA)
axarr[0].set_title('Reflex + parallax + proper motion')
axarr[1].plot(epochs/Day,DDEC)
plt.xlabel("Julian date [days]")
plt.savefig("3time.pdf")

plt.clf()
plt.plot(DRA,DDEC,'kx')
plt.title('Reflex + parallax + proper motion')
plt.xlabel("RA []")
plt.ylabel("DEC []")
plt.savefig('3radec.pdf')
