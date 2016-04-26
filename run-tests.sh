#!/bin/bash -e

for file in .tests/*.py
do
    echo $file
    PYTHONPATH=. python $file
done
