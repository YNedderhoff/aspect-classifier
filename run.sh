#!/bin/bash

paste ../team-lab-ss2015/data/pos/dev.col ../team-lab-ss2015/data/pos/dev-predicted.col >> ../team-lab-ss2015/data/pos/train.col

python evaluation.py -i ../team-lab-ss2015/data/pos/train.col


