#!/usr/bin/python
__author__="Hayden Panike"
__maintainer__="Hayden Panike"
__email__="hpanike@gmail.com"
__status__="Prototype"


## This simple script is used to test argParse

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('integers', metavar='N', type=int, nargs='+', help= 'an integer for the accumulator')
parser.add_argument('-s','--sum', dest='accumulate',action='store_const', const=sum, default=max, help='sum the integers (default: find the max)')
args = parser.parse_args()
print args.accumulate(args.integers)
