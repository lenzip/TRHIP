def matchGenVertex(gen, reco, cut=1): #cut is in mm
  zgen = gen.Z
  mindistance = 99999
  minindex = -1
  for i,reco in enumerate(reco):
    if abs(reco - zgen) < mindistance:
      mindistance = abs(reco - zgen)
      minindex = i
  if mindistance > cut:#if it is not close enough reset index
    minindex = -1
  
  return minindex

