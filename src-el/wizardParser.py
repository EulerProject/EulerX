# wizard parser
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i","--iFile", action= "append")
parser.add_argument("-t","--tFile", action= "append")
parser.add_argument("-s","--sNum")
args = parser.parse_args()
if args.iFile == None:
    args.iFile = "in.csv"
if args.tFile == None:
    args.tFile = " "
if args.sNum == None:
    args.sNum = 1
