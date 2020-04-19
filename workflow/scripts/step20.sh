#!/bin/bash

source scripts/env.sh

cp $CMSSW_BASE/src/JetMETAnalysis/JetAnalyzers/config/jra_dr_finebinning.config jra.config

# create histograms necessary for higher level corrections
# output: root filw with histograms
jet_response_analyzer_x jra.config \
   -input $inDIR/JRA_l1.root \
   -nbinsabsrsp 0 \
   -nbinsetarsp 0 \
   -nbinsrelrsp 200 \
   -doflavor false\
   -flavorDefinition phys \
   -MCPUReWeighting $inDIR/PileupMC.root \
   -DataPUReWeighting $inDIR/MyDataPileupHistogram.root \
   -DataPUHistoName pileup \
   -output $inDIR/JRA_l2.root \
   -useweight true \
   -nrefmax 3 \
   -algs ${ALGO}l1:0.2 \
   -relrspmin 0.0 \
   -relrspmax 2.0
