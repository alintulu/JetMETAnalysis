#!/bin/bash

source scripts/env.sh

# compute PU distribution for data
pileupCalc.py -i /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PromptReco/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt \
    --inputLumiJSON \
    /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PileUp/pileup_latest.txt \
    --calcMode true --minBiasXsec 69200 \
    --maxPileupBin 100 --numPileupBins 100 $inDIR/MyDataPileupHistogram.root

# compute PU distribution for MC
python scripts/makeMCPileupHist.py \
    SimGeneral.MixingModule.mix_2018_25ns_JuneProjectionFull18_PoissonOOTPU_cfi \
    --outputFilename $inDIR/PileupMC.root

# match reconstructed jets in PU and noPU sample
jet_synchtest_x -sampleNoPU JRA_noPU.root \
		-samplePU JRA_MM_.root \
		-basepath $inDIR \
		-outputPath $inDIR \
		-algo1 $ALGO \
		-algo2 $ALGO \
		-MCPUReWeighting PileupMC.root \
		-DataPUReWeighting MyDataPileupHistogram.root



