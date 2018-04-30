## This script cobmined the newly-generated XML files from reformat_partner_xml.py into files of 75 KB or less for import into the Description and Authority Service (DAS).
## NOTES: The following data must be modified for each use:
##	* Line 7 - The XML file name for the combined files

import os, re, glob

file = 'm384-import-1.xml'
filenames = glob.glob("*.xml")

counter = 2
outputfile = file

print 'Combining XML files...'

with open(file, 'a') as outfile:
	outfile.write('<import xmlns="http://ui.das.nara.gov/"><fileUnitArray>')

for fname in filenames:  	
	in_size = (os.stat(fname).st_size / 1000000)
	try:
		out_size = (os.stat(file).st_size / 1000000)
	except OSError:
		out_size = 0
	if (in_size + out_size) > 30:
		with open(file, 'a') as outfile:
			outfile.write('</fileUnitArray></import>')
		file = re.split('\.', outputfile)[0] + '_' + str(counter) + '.xml'
		counter = counter + 1
		with open(file, 'a') as outfile:
			outfile.write('<import xmlns="http://ui.das.nara.gov/"><fileUnitArray>')
	with open(file, 'a') as outfile:   
		with open(fname) as infile:
			for line in infile:
				outfile.write(line)
				
with open(file, 'a') as outfile:
			outfile.write('</fileUnitArray></import>')	
			
print "Complete."