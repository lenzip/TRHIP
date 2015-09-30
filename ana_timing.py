#!/usr/bin/env python

import sys

import ROOT

from vertexLocatorWithTiming import *
from utilities import *


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
#numberOfEntries = treeReader.GetEntries()
numberOfEntries = 3000

# Get pointers to branches used in this analysis
branchDisk1 = treeReader.UseBranch("pixelDisk1")
branchDisk2 = treeReader.UseBranch("pixelDisk2")
branchDisk3 = treeReader.UseBranch("pixelDisk3")
branchDisk4 = treeReader.UseBranch("pixelDisk4")
branchDisk5 = treeReader.UseBranch("pixelDisk5")
branchDisk6 = treeReader.UseBranch("pixelDisk6")
branchTrueVertices = treeReader.UseBranch("Vertex") 
verbose=False

outf = ROOT.TFile(outfile, "RECREATE")
outf.cd()
#hvertex_pos = ROOT.TH1F("pos", "pos", 200, -100, 100);
hvertex_res = ROOT.TH1F("res", "res", 200, -2, 2);
hvertex_n = ROOT.TH1F("n", "n", 200, 0, 200);
heff_numerator = ROOT.TH1F("heff_numerator", "heff_numerator", 200, -100, 100);
heff_denominator = ROOT.TH1F("heff_denominator", "heff_denominator", 200, -100, 100);
hfake_numerator = ROOT.TH1F("hfake_numerator", "hfake_numerator", 200, -100, 100);
hfake_denominator = ROOT.TH1F("hfake_denominator", "hfake_denominator", 200, -100, 100);

hpos_n = ROOT.TH1F("hpos_n", "hpos_n", 30, 0, 30)
hneg_n = ROOT.TH1F("hneg_n", "hneg_n", 30, 0, 30)



# Book histograms
for entry in range(0, numberOfEntries):
  # Load selected branches with data from specified event
  treeReader.ReadEntry(entry)
  if (verbose):
    print "#####################################################################Reading enrty", entry
  else:
    if entry%10 == 0:
      print "Reading enrty", entry
      

  vl = vertexLocatorWithTiming(branchDisk1, 1)
  hpos_n.Fill(len(vl.pos_sideRadii))
  hneg_n.Fill(len(vl.neg_sideRadii))
  vertices = vl.vertices(4)
  #print vertices
  hvertex_n.Fill(len(vertices))
  for vertex in vertices:
    #hvertex_pos.Fill(vertex)
    hfake_denominator.Fill(vertex)

  matchedIndexes = []
  for trueVertex in branchTrueVertices:
    #print trueVertex.Z
    heff_denominator.Fill(trueVertex.Z)
    imatch = matchGenVertex(trueVertex, vertices, 1.)
    if (imatch != -1):
      heff_numerator.Fill(trueVertex.Z)
      hvertex_res.Fill(vertices[imatch] - trueVertex.Z)
      matchedIndexes.append(imatch)
   
  for i in range(len(vertices)):
    if i not in matchedIndexes:
      hfake_numerator.Fill(vertices[i])


      

    

#hvertex_pos.Draw()
#hvertex_n.Draw()
eff = ROOT.TGraphAsymmErrors(heff_numerator, heff_denominator)
eff.SetNameTitle("eff", "eff")
eff.Write()
fake = ROOT.TGraphAsymmErrors(hfake_numerator, hfake_denominator)
fake.SetNameTitle("fake", "fake")
fake.Write()
outf.Write()
raw_input("Press Enter to continue...")
