#!/bin/bash

source scripts/env.sh

jet_l2_correction_x -input $inDIR/JRA_l1_f.root \
		-era $ERA \
	 	-l2l3 true \
		-batch true \
	 	-mpv false \
		-output CondFormats/JetMETObjects/data/JRA_l2.root
