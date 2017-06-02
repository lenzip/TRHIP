#!/usr/bin/env python

import sys

import ROOT

from vertexLocatorWithTiming import *
from utilities import *
import numpy as np

if len(sys.argv) < 2:
  print " Usage: Example1.py input_file"
  sys.exit(1)

ROOT.gSystem.Load("libDelphes")

inputFile = sys.argv[1]
outfile = sys.argv[2]

# Create chain of root trees
chain = ROOT.TChain("Delphes")
chain.Add(inputFile)

# Create object of class ExRootTreeReader
treeReader = ROOT.ExRootTreeReader(chain)
numberOfEntries = treeReader.GetEntries()
#numberOfEntries = 3000

# Get pointers to branches used in this analysis
genJets = treeReader.UseBranch("GenJet") 
trkJets = treeReader.UseBranch("Jet") 
verbose=False

outf = ROOT.TFile(outfile, "RECREATE")
outf.cd()
#hvertex_pos = ROOT.TH1F("pos", "pos", 200, -100, 100);
ptbins =  np.array([10., 100., 300., 500., 1500., 3000., 5000.])
etabins = np.array([0., 1., 2., 3., 4., 5.])
profile = ROOT.TProfile2D("profile", "profile", 5, etabins, 6, ptbins)

resolution2D = ROOT.TH2F("res2D", "res2D", 20, 30, 500, 30, -1, 1)

# Book histograms
for entry in range(0, numberOfEntries):
  # Load selected branches with data from specified event
  treeReader.ReadEntry(entry)
  if (verbose):
    print "#####################################################################Reading enrty", entry
  else:
    if entry%1000 == 0:
      print "Reading enrty", entry
  
  for genJet in genJets:
    recIndex = matchDeltaR(genJet, trkJets, 0.5)
    if recIndex != -1:
      recJet = trkJets[recIndex]
      profile.Fill(abs(recJet.Eta), recJet.PT, genJet.PT/recJet.PT)
      if (genJet.PT > 30.):
        resolution2D.Fill(genJet.PT, (recJet.PT-genJet.PT)/genJet.PT)
      

    

resolution2D.FitSlicesY()
hbias = ROOT.gDirectory.Get("res2D_1")
hbias.SetNameTitle("bias", "bias")
hresolution = ROOT.gDirectory.Get("res2D_2")
hresolution.SetNameTitle("resolution", "resolution")
hbias.Write()
hresolution.Write()
outf.Write()
raw_input("Press Enter to continue...")
