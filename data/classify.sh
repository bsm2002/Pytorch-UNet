#!/bin/bash

# This script is used to classify the data into analyzed, original
# images are saved in ./pore/

# if contains org -> imgs
# else -> analyzed

for file in $(ls ./pore/); do
  if [[ $file == *"org"* ]]; then
    cp ./pore/$file ./imgs/$file
  else
    cp ./pore/$file ./analyzed/$file
  fi
done


