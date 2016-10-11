# partner-data-transform
This repo contains the files necessary to transform the data from partner digitization projects into a format compliant with the data scheme to import to the Description and Authority Service (DAS) for inclusion in the [National Archives Catalog](https://catalog.archives.gov).

[Download this repo](https://github.com/usnationalarchives/partner-data-transform/archive/master.zip) as it exists for a working directory.

## /metadata
Partner XML metadata for each microfilm publicaton must go in the metadata folder. Samples for a publication can be found in the [metadata folder here](https://github.com/usnationalarchives/partner-data-transform/tree/master/metadata).

## /objects
The CSV file generated by the S3 Manifester must go in the objects folder. Samples for a publication can be found in the [objects folder here](https://github.com/usnationalarchives/partner-data-transform/tree/master/objects).

## Python scripts
Python scripts must be modified for each new instance. Notes for where to modify scripts can be found below.

Python scripts must be run in the following order:

1. [s3_csv_split.py](https://github.com/usnationalarchives/partner-data-transform/blob/master/s3_csv_split.py)
  * This script takes the CSV file with all the digital image filepaths from the Amazon S3 cloud and breaks them out per microfilm roll.
  * Modifications: 
    * **Change the file name:** 
`with open('m268_copy.csv', 'r') as log :`
    *  **Change the number of rows to match the number of columns on the original csv:** 
`writelog.writerow( (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7] ) )`
2. [reformat_partner_xml.py](https://github.com/usnationalarchives/partner-data-transform/blob/master/reformat_partner_xml.py)
  * This script reformats the partner xml into a DAS xml format, then marries the xml with the digital object filepaths.
  * Modifications:
    * **Change the series NAID:**
`series = 586957`
    * **Change the microfilm publication number:**
`pub = 'M268'`
    * **Ensure the xml tags for r.replace match the metadata:**
```
try:
	with open('metadata/' + file + '_metadata.xml', 'r') as y :
		r = re.sub('<metadata name=\"(.*?)\" value=\"(.*?)\" />',r'<\1>\2</\1>', y.read())
		r = r.replace('Publication Number','Publication_Number')
		r = r.replace('Publication Title','Publication_Title')
		r = r.replace('Content Source','Content_Source')
		z = open(file + '_metadata_(reformatted).xml', 'w')
		z.write(r)
		z.close()
except IOError:
	print '   Error: ROLL NOT FOUND'
	x = x + 1
	continue
	
tree = ET.parse(file + '_metadata_(reformatted).xml')
root = tree.getroot()

Publication_Number = root.find('Publication_Number').text
Publication_Title = root.find('Publication_Title').text
print str(datetime.datetime.now().time()) + ': ' + Publication_Number, Publication_Title, 'Roll ' + str(roll)
```
    * **Ensure the data values match the metadata (lines 65-90):**
```
try:
	for page in root.findall('page'):
		with open('objects/' + file + '.csv', 'r') as log :
			readfile = csv.reader(log, delimiter= '\t')
	
			file_name = ''
			id = ''
			givenname = '[BLANK]'
			surname = '[BLANK]'
			age = '[BLANK]'
			year = '[BLANK]'
			military_unit = '[BLANK]'
			file_size = ''

			file_name = page.get('image-file-name')
			id = page.get('footnote-id')
			if page.find('givenname') is not None:
				givenname = page.find('givenname').text
			if page.find('surname') is not None:
				surname = page.find('surname').text
			if page.find('age') is not None:
				age = page.find('age').text
			if page.find('year') is not None:
				year = page.find('year').text
			if page.find('military-unit') is not None:
				military_unit = page.find('military-unit').text
```
    * **Ensure the csv row numbers are accurate (lines 96-104):**
```
for row in readfile:
	try:
		if new_file_name == row[7]:
			if file == row[4]:
				file_size = str(row[1])
				file_path = row[0]
				label_flag = row[7]
	except IndexError:
		pass
```
    * **Modify the title string as appropriate (line 108):**
`title = ('[Tennessee] ' + surname + ', ' + givenname + ' - Age ' + age + ', Year: ' + year + ' - ' + military_unit).encode('utf-8')`
3. [combine_xml.py](https://github.com/usnationalarchives/partner-data-transform/blob/master/combine_xml.py)
  * This script combines multiple xml files for each microfilm roll into one for bulk import.

*All scripts in this repo are written in [Python 2.7](https://www.python.org/download/releases/2.7/).*

## Other files
The following files must be in the working directory as they exist here:
* .DS_store
* .gitignore
* log.txt - *must be empty*
* uniquetest.csv - *must be empty*
