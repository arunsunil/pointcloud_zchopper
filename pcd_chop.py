#!/usr/bin/env python

"""
Takes in pcd filename and level as arguments and chops off
everything above it and creates a new pcd file with the remaining
points. 

Useful for making Vector Maps as Autoware VectorMapper does only a top-down
view. Hence if there are objects covering the road from above, the tool will
put lanes, stoplines, etc. on these objects, instead of on the road.

This script works only with PCD file format v0.7
"""

import sys
from time import sleep

# Takes in 2 arguments - pcd filename and z-level at which the map is to be chopped
if len(sys.argv) < 3:
	print "Not enough arguments"
	print "Format: python pcd_chop.py <pcd_filename> <level>"
	print "Exiting..."
	sys.exit(0)

filepath = str(sys.argv[1])
new_filename = filepath[:-4] + "_chopped.pcd"
level = float(sys.argv[2])
lines = []
idx = 0

# Write list of lines to file
def writefile(filename, line_list):
	f = open(filename, "a")
	for i in range(len(line_list)):
		f.write(line_list[i])
	f.close()

with open(filepath) as fp:
	line = str(fp.readline())
	lines.append(line)
	line = str(fp.readline())
	while line:
		if len(lines) <= 11:
			lines.append(line)
			# If PCD is not v0.7, this script will not work
			if lines[1] != "VERSION 0.7\n":
				print "Unsupported file format. Exiting..."
				sys.exit(0)
		else:
			split_line = line.split()
			z = float(split_line[2])
			# Discard points below z = level
			if z <= level:
					lines.append(line)	
		line = str(fp.readline())
		idx += 1
		# Print message every 1000 iterations
		if (idx % 1000) == 0:
			print "Working on it..."

	# Change width and number of points according to new PCD
	lines[6] = "WIDTH " + str(len(lines) - 11) + "\n"
	lines[9] = "POINTS " + str(len(lines) - 11) + "\n"

writefile(new_filename, lines)
print "Done."