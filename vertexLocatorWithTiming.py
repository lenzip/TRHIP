import math
import scipy.signal as signal
import numpy as np
import bisect
import random

class vertexLocatorWithTiming:
  def __init__(self, disk, n):
    self.idDisk = n
    self.pos_sideRadii = self.filterHitsAndSmear(disk,  n) 
    self.neg_sideRadii = self.filterHitsAndSmear(disk, -n)

    #print "self.pos_sideRadii", self.pos_sideRadii
    #print "self.neg_sideRadii", self.neg_sideRadii


  def getDiskEnvelope(self, n):
    nabs = abs(n)
    sgn = nabs/n
    if (nabs == 1):
      return (sgn*300., 30., 150.)
    elif (nabs == 2):
      return (sgn*400., 30., 150.)
    elif (nabs == 3):
      return (sgn*500., 30., 150.)   
    elif (nabs == 4):
      return (sgn*650., 30., 150.)
    elif (nabs == 5):
      return (sgn*850., 30., 150.)   
    elif (nabs == 6):
      return (sgn*1100., 30., 150.)
    elif (nabs == 7):
      return (sgn*1400., 30., 150.)
    elif (nabs == 8):
      return (sgn*2000., 100., 150.)
    elif (nabs == 9):
      return (sgn*2300., 100., 150.)
    elif (nabs == 10):
      return (sgn*2650., 100., 150.)
    else:
      return (0.,0.,0.)  
    
      

  def filterHitsAndSmear(self,disk,iddisk):
    (z, rmin, rmax) = self.getDiskEnvelope(iddisk)
    hits = []
    for track in disk:
      if abs(track.ZOuter - z) < 5 : #mm
        r = math.sqrt(track.XOuter**2+track.YOuter**2)
        t = track.TOuter+random.gauss(0., 10e-12) #10 ps smearing
        if (r > rmin and r < rmax):
          hits.append((r,t))
    #sort by phi
    hits.sort(key=lambda hit: hit[1])
    return hits 

  def vertices(self, ntracks):
    crossings = self.make_crossings(self.pos_sideRadii, self.neg_sideRadii)
    #print "z0s ", z0s
    #print "crossings", crossings
    bins=np.arange(-100,100,0.2)
    h,bin_edges = np.histogram(crossings, bins=bins)
    #print h
    all_maxima = signal.find_peaks_cwt(h, np.arange(0.5,1))
    the_vertices = []
    for i in all_maxima:
      if h[i] >= ntracks: 
        the_vertices.append((bin_edges[i]+bin_edges[i+1])/2.)
    #print "the_vertices", the_vertices    
    return the_vertices

    
  def make_crossings(self, plus, minus):
    zp = self.getDiskEnvelope( self.idDisk)[0]
    zn = -zp
    c = 2.99792458e11 #mm/s
    crossings = []
    if (len(plus)>1 and len(minus)>1):
      for rp,tp in plus:
        for rn,tn in minus:
          vp = c*math.cos(math.atan(rp/zp))
          vn = c*math.cos(math.atan(rn/abs(zn)))
          #vp = c
          #vn = c
          #print "zp,rp,tp", zp,rp,tp, " zn,rn,tn", zn,rn,tn, "   vp,vn", vp, vn

          #z = zp - (tp - t)*vp
          #z = zn + (tn - t)*vn
          A = np.array([[1., -vp], [1., vn]])
          B = np.array([zp - tp*vp, zn + tn*vn])
          #solve AX = B
          x = np.linalg.solve(A,B)
          #print "x = ",x
          crossings.append(x[0]) #z value

    return crossings


          
    
    return z0s
