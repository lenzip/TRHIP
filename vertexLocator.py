import math
import scipy.signal as signal
import numpy as np
import bisect

class vertexLocator:
  def __init__(self, disk1, disk2, n1, n2):
    self.id1 = n1
    self.id2 = n2
    self.pos_sideRadii1 = self.filterHits(disk1, n1) 
    self.pos_sideRadii2 = self.filterHits(disk2, n2)
    self.neg_sideRadii1 = self.filterHits(disk1, -n1)
    self.neg_sideRadii2 = self.filterHits(disk2, -n2)

    #print "self.pos_sideRadii1", self.pos_sideRadii1
    #print "self.pos_sideRadii2", self.pos_sideRadii2
    #print "self.neg_sideRadii1", self.neg_sideRadii1
    #print "self.neg_sideRadii2", self.neg_sideRadii2
 

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
    
      

  def filterHits(self,disk,iddisk):
    (z, rmin, rmax) = self.getDiskEnvelope(iddisk)
    hits = []
    for track in disk:
      if abs(track.ZOuter - z) < 5 : #mm
        r = math.sqrt(track.XOuter**2+track.YOuter**2)
        phi = math.atan2(track.YOuter,track.XOuter)
        if (r > rmin and r < rmax):
          hits.append((r,phi))
    #sort by phi
    hits.sort(key=lambda hit: hit[1])
    return hits 

  def vertices(self, ntracks):
    z0sPlus = self.make_pairs(self.pos_sideRadii1, self.id1, self.pos_sideRadii2, self.id2)
    z0sMinus = self.make_pairs(self.neg_sideRadii1, self.id1, self.neg_sideRadii2, self.id2)

    z0s = []
    z0s.extend(z0sPlus)
    z0s.extend(z0sMinus)
    #print "z0s ", z0s
    bins=np.arange(-100,100,1)
    h,bin_edges = np.histogram(z0s, bins=bins)
    #print "h", h
    median = np.median(h)
    all_maxima = signal.find_peaks_cwt(h, np.arange(0.5,1))
    the_vertices = []
    for i in all_maxima:
      if h[i] >= ntracks:
        the_vertices.append((bin_edges[i]+bin_edges[i+1])/2.)
  
    #print the_vertices
    return the_vertices

    
  def make_pairs(self, r1s, id1, r2s, id2):
    z1 = self.getDiskEnvelope(id1)[0]
    z2 = self.getDiskEnvelope(id2)[0]
    z0s = []
    if (len(r1s)>1 and len(r2s)>1):
      for r1,phi1 in r1s:
        #get close hits in phi in the other disk
        keys = [rp[1] for rp in r2s]
        minimum = phi1-10*math.pi/180 if phi1-10*math.pi/180. > -math.pi else 2*math.pi+phi1-10*math.pi/180.
        maximum = phi1+10*math.pi/180 if phi1+10*math.pi/180. < math.pi else phi1+10*math.pi/180. -2*math.pi
        if maximum < minimum:
          tmp = maximum
          maximum = minimum
          minimum = tmp
        start = bisect.bisect_left(keys,minimum)
        stop = bisect.bisect_left(keys,maximum)
        secondDiskHits = r2s[start:stop] 
        #print "phi1 is",phi1," propagating to", secondDiskHits
        for r2,phi2 in secondDiskHits:
          m = (z2-z1)/(r2-r1)
          z0 = -m*r1+z1 
          z0s.append(z0)
    
    return z0s
