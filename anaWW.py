#!/usr/bin/env python

import sys

import ROOT

from WWAnalysis import *


if len(sys.argv) < 2:
  print " Usage: Example1.py output_file"
  sys.exit(1)

ROOT.gSystem.Load("libDelphes")

outfile = sys.argv[1]

samples = [
          ['/eos/cms/store/user/lenzip/ERCLaVendetta/pythia8_14TeV_WWTo2L2Nu__CMS_PhaseII_Substructure_PIX4022_200PU/total.root', "WW_PU200", 3387.],
          ['/eos/cms/store/user/lenzip/ERCLaVendetta/pythia8_14TeV_WWTo2L2Nu__CMS_PhaseII_Substructure_PIX4022_200PU_timing20/total.root', 'WW_PU200_timing20ps', 3387.]
          ]

plotList = [
           ['rapgap', 10, 0, 10], 
           ['diJetMass', 10, 0, 1000],
           ]

outf = ROOT.TFile(outfile, "RECREATE")
plots = {}
for sample in samples:
  plots[sample[1]] = {}
  for plot in plotList:
    plots[sample[1]][plot[0]] = ROOT.TH1F(plot[0]+"_"+sample[1], plot[0]+"_"+sample[1], plot[1], plot[2], plot[3])

print plots
lumi = 2500 #/fb

for sample in samples:
  # Create chain of root trees
  filein = ROOT.TFile(sample[0])
  chain = filein.Get("Delphes")
  print "sample", sample 

  # Create object of class ExRootTreeReader
  treeReader = ROOT.ExRootTreeReader()
  treeReader.SetTree(chain)
  numberOfEntries = treeReader.GetEntries()

  # Get pointers to branches used in this analysis
  electrons = treeReader.UseBranch("ElectronCHS")
  muons = treeReader.UseBranch("MuonTightCHS")
  jets = treeReader.UseBranch("Jet")

  xsec =  sample[2]#fb
  # Book histograms
  counter       = Counter()   
  for entry in range(0, numberOfEntries):
    # Load selected branches with data from specified event
    treeReader.ReadEntry(entry)
    if entry%1000 == 0:
      print "Reading enrty", entry
    wwana       = WWAnalysis(muons, electrons, jets, counter) 
    if 'leptonPairMass' in wwana.steps:
      for plot in plotList:
        plots[sample[1]][plot[0]].Fill(eval('wwana.'+plot[0]))
  
  scalefact = lumi*xsec/numberOfEntries
  for plot in plotList:
    plots[sample[1]][plot[0]].Scale(scalefact)

  print counter.cuts

outf.Write()
#raw_input("Press Enter to continue...")
