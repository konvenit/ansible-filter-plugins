#!/bin/bash -e

for file in .tests/*.py
do
    echo $file
    python $file
done
