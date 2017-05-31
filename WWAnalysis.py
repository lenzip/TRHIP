from utilities import *
import copy


class WWAnalysis:
  def __init__(self, branchMuons, branchElectrons, branchJets, counter):
    counter.increment('all')
    self.steps = ['all']
    muons = branchToList(branchMuons)
    electrons = branchToList(branchElectrons)
    jets = branchToList(branchJets)
    #print len(muons), len(electrons), len(jets)
    if len(muons) == 0:
      self.passed = False
      return  
    if len(electrons) == 0:
      self.passed = False
      return
    counter.increment('twoleptons')
    self.steps.append('twoleptons')
    sorted(muons, key = lambda obj: obj.PT, reverse = True)
    sorted(electrons, key = lambda obj: obj.PT, reverse = True)
    self.mu = muons[0]
    self.e  = electrons[0]
    self.jets = self.filterJets(jets, 20)
    self.rapgap = -99999
    self.diJetMass = -9999
    if len(self.jets) > 1:
      jetsRapidityOrdered = copy.deepcopy(self.jets)
      sorted(jetsRapidityOrdered, key = lambda jet: jet.Eta)
      self.rapgap = abs(jetsRapidityOrdered[0].Eta-jetsRapidityOrdered[-1].Eta)
      self.diJetMass = (jetsRapidityOrdered[0].P4() + jetsRapidityOrdered[-1].P4()).M()

    if not (self.mu.PT > 25. or self.e.PT > 25. or abs(self.mu.Eta) > 4. or abs(self.e.Eta) > 4.):
      self.passed = False
      return
    
    counter.increment('twoleptonsPtEta')
    self.steps.append('twoleptonsPtEta')
    
    pairMomentum = self.mu.P4() + self.e.P4()
    if pairMomentum.Pt() < 30.:
      self.passed = False
      return
    
    counter.increment('leptonPairPt')
    self.steps.append('leptonPairPt')

    if pairMomentum.M() < 70.:
      self.passed = False
      return

    counter.increment('leptonPairMass')
    self.steps.append('leptonPairMass')

    if len(self.jets) < 2:
      self.passed = False
      return
    counter.increment('twojets')
    self.steps.append('twojets')

    if self.rapgap < 3:
      self.passed = False
      return
    
    counter.increment('rapGap')
    self.steps.append('rapGap')

    if self.diJetMass < 300:
      self.passed = False
      return
    
    counter.increment('diJetMass')
    self.steps.append('diJetMass')

      

  def leadingObject(self, objects):
    sorted(objects, key = lambda obj: obj.PT, reverse = True)
    return objects[0]

  def filterJets(self, jets, ptmin = 30):
    filtered = []
    sorted(jets, key = lambda obj: obj.PT, reverse = True)
    for jet in jets:
      if jet.PT> ptmin:
        filtered.append(jet)
    return filtered    
