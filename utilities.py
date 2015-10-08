def matchGenVertex(gen, recov, cut=1): #cut is in mm
  zgen = gen.Z
  mindistance = 99999
  minindex = -1
  for i,reco in enumerate(recov):
    if abs(reco - zgen) < mindistance:
      mindistance = abs(reco - zgen)
      minindex = i
  if mindistance > cut:#if it is not close enough reset index
    minindex = -1
  
  return minindex

def matchDeltaR(gen, recov, cut):
  p4gen = gen.P4()
  mindistance = 99999
  minindex = -1
  for i,reco in enumerate(recov):
    p4reco = reco.P4()
    if p4gen.DeltaR(p4reco) < mindistance:
      mindistance = p4gen.DeltaR(p4reco)
      minindex = i
  if mindistance > cut:#if it is not close enough reset index
    minindex = -1
  
  return minindex
