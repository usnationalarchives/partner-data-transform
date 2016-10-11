## This script takes the CSV file from the S3 Manifester and breaks it into individual files for each microfilm roll.
## NOTES: The following data must be modified for each use:
##	* Line 10 - The CSV file name, e.g. "opaexport-conv_m384_1473437803.csv"
##	* Line 16 - The row numbers

import csv

# Construct python command like: python s3_csv_split.py

print 'Generating CSV files...'
with open('objects/opaexport-conv_m384_1473437803.csv', 'r') as log :
	readfile = csv.reader(log, delimiter= ',')
	for row in readfile:
		with open('objects/' + row[4] + '.csv', 'a') as write:
			writelog = csv.writer(write, delimiter= '\t', quoting=csv.QUOTE_ALL)
			try:
				writelog.writerow( (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7] ) )
			except IndexError:
				pass