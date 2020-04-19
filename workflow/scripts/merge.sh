#!/bin/bash

stem=$1
batch=$2

merge()
{

  stem=$1
  batch=$2
  id=$3
  name=${stem}${id}
  N=$(ls ${name}*.root | wc -l)

  if (( $N <= $batch )); then
    hadd -k JRA_M_final.root ${name}{1..$N}*.root
  else
    new_id=$(($id+1)) 
    j=0
    for ((i=0;i<=$N;i+=$batch)); do
      if (($(($i+$batch)) > $N)); then
        hadd -k ${stem}${new_id}${j}.root ${name}{$i..$N}.root
      else
        hadd -k ${stem}${new_id}${j}.root ${name}{$i..$(($i+$batch))}.root
      fi
      j=$(($j+1))
    done
    merge $stem $batch $new_id
  fi
}

merge $stem $(($batch-1)) 0
