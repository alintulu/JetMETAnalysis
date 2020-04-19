#!/bin/bash

source scripts/env.sh

# aply L1 corrections
# output: root file with corrections applied
jet_apply_jec_x -input $inDIR/JRA_MM_.root \
		-era $ERA \
		-levels 1 \
		-algs $ALGO \
		-output $inDIR/JRA_l1.root \
		-L1FastJet true \
		-saveitree false
