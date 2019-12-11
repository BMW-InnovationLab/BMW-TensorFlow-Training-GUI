#!/bin/bash

#Remove deleteme files
rm -f checkpoints/deleteme
rm -f checkpoints/servable/deleteme
rm -f datasets/deleteme

#Adjust basedir path
python3 adjust_basedir_path.py