#!/bin/bash

source scripts/env.sh

jet_apply_jec_x -input $inDIR/JRA_l1.root \
		-era $ERA \
		-levels 2 \
	 	-algs ${ALGO}l1 \
	 	-output $inDIR/JRA_jec.root \
		-saveitree false
