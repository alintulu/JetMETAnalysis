#!/bin/bash

ERA=Autumn18_V15_V1__MC
ALGO=ak4pf
inDIR=/eos/user/a/adlintul/JRA/

jet_synchtest_x -sampleNoPU JRA_noPU.root \
		-samplePU JRA_MM_.root \
		-basepath $inDIR \
		-outputPath $inDIR \
		-algo1 $ALGO \
		-algo2 $ALGO \
		-MCPUReWeighting PileupMC.root \
		-DataPUReWeighting MyDataPileupHistogram.root



