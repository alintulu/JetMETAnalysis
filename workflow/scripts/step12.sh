#!/bin/bash

source scripts/env.sh

# compute corrections for pileup effects (L1)
# output: text file with corrections (Autumn18_V15_V1__MC_L1FastJet_AK4PF.txt)
jet_synchfit_x 	-inputDir $inDIR \
		-outputDir CondFormats/JetMETObjects/data/ \
		-era $ERA \
		-algo1 $ALGO \
		-algo2 $ALGO
