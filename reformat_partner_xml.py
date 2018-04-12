# -*- coding: utf-8 -*-

### NOTES: The following data is hard-coded:
###   * "M268_" in source file names--this is necessary to parse the roll number. This needs to be updated for other publications or it will not be able to open the files.
###   * Source XML files need to be in subdirectory titled "metadata" and have file names "M268_ROLL_metadata.xml", where "ROLL" is a four-digit number with leading zeroes
###   * Following fields are all hard-coded based on M268's data: Level of description (file unit), general records type, data control group, use restriction, access restriction, online resource note, variant control number, physical occurrence, copy status, reference unit, location, media occurrence, general media type, object type, object designator, thumbnail file name.
###   * All file paths must be in the form "https://opaexport-conv.s3.amazonaws.com/" + supplied path.
###   * All online resources must be in the form "http://www.fold3.com/image/" + footnote ID.
###   * The objects file is set to be comma-delimited (csv) by default, rather than tab or something different.

import csv, xml, re, time, os, datetime, argparse
import xml.etree.ElementTree as ET

# Construct python command like: python reformat_partner_xml.py

parser = argparse.ArgumentParser()
parser.add_argument('--series', dest='series', metavar='SERIES',
                    action='store')
parser.add_argument('--objects', dest='objects', metavar='OBJECTS',
                    action='store')
parser.add_argument('--pub', dest='pub', metavar='PUB',
                    action='store')
args = parser.parse_args()

series = 300398
if args.series is not None:
	series = args.series
objectfile = args.objects

pub = 'M384'
if args.pub is not None:
	pub = args.pub

sequence_order = 1	
x = 1
while x > 0:
	roll = x
	file = str(pub) + '_' + str(roll).zfill(4)

## This part takes the partner XML and reformats it to more usable XML (i.e. going from attributes to elements - http://www.ibm.com/developerworks/library/x-eleatt/). The reformatted XML is saved as a new document with "_(reformatted)" appended to the name, so that the original file is not altered.
	try:
		with open('metadata/' + file + '.xml', 'r') as y :
			r = re.sub('<metadata name=\"(.*?)\" value=\"(.*?)\" />',r'<\1>\2</\1>', y.read())
			r = r.replace('Publication Number','Publication_Number')
			r = r.replace('Publication Title','Publication_Title')
			r = r.replace('Content Source','Content_Source')
			r = r.replace('Content Partner','Content_Partner')
			r = r.replace('Footnote Job','Footnote_Job')
			r = r.replace('Footnote Publication Year','Footnote_Publication_Year')
			r = r.replace('Nara Catalog Id','Nara_Catalog_Id')
			r = r.replace('Nara Catalog Title','Nara_Catalog_Title')
			r = r.replace('Record Group','Record_Group')
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

## This parses the XML for each page element. Default values for title components are "[BLANK]".
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

	## Changes the given .jp2 file name to .jpg and adding the roll/publication information. Then, using the new file name extracted from partner data, look it up in the images CSV to extract file size, file path, and label flag fields.

				new_file_name = file_name[:-4] + '.jpg'
	
				for row in readfile:
					try:
						if new_file_name == row[3]:
							if file == row[2]:
								file_size = str(row[1])
								file_path = row[0]
								label_flag = row[3]
					except IndexError:
						pass

	## Generates the title based on the established formula.

				title = ('[Maryland] ' + surname + ', ' + givenname + ' - Age ' + age + ', Year: ' + year + ' - ' + military_unit).encode('utf-8')

	## Using all above parsed fields, generate the whole output XML document with 3 parts. XML_top (everything above the digital objects, since this will only appear once per title), digital_objects (so that it can repeat for each new page in the same title/file unit), and XML_bottom (completes each file unit).

				DASxml_top = """<fileUnit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">

<sequenceOrder>""" + str(sequence_order) + """</sequenceOrder>

<title>""" + title + """</title>

<parentSeries><naId>""" + str(series) + """</naId></parentSeries>

<generalRecordsTypeArray><generalRecordsType><termName>Textual Records</termName></generalRecordsType></generalRecordsTypeArray>

<onlineResourceArray><onlineResource><termName>https://www.fold3.com/image/""" + id + """</termName><description>Fold3</description><note>This file was scanned as part of a collaboration effort between Fold3 and the National Archives.</note></onlineResource></onlineResourceArray>

<variantControlNumberArray><variantControlNumber><number>Fold3 2016</number><type><termName>Search Identifier</termName></type></variantControlNumber></variantControlNumberArray>

<microformPublicationArray><microformPublication><note>The start of this file can be found on Roll """ + str(roll) + """.</note><publication><termName>M384 - Compiled Service Records of Volunteer Union Soldiers Who Served in Organizations From the State of Maryland.</termName></publication></microformPublication></microformPublicationArray>

<dataControlGroup><groupCd>RDTP1</groupCd><groupId>ou=RDTP1,ou=groups</groupId></dataControlGroup>

<accessRestriction><status><termName>Unrestricted</termName></status></accessRestriction>

<useRestriction><status><termName>Unrestricted</termName></status></useRestriction>

<physicalOccurrenceArray><fileUnitPhysicalOccurrence>

<copyStatus><termName>Preservation-Reproduction-Reference</termName> </copyStatus><referenceUnitArray><referenceUnit><termName>National Archives at Washington, DC - Textual Reference</termName> </referenceUnit></referenceUnitArray>

<locationArray><location><facility><termName>National Archives Building - Archives I (Washington, DC)</termName> </facility></location></locationArray>

<mediaOccurrenceArray><mediaOccurrence><specificMediaType><termName>Paper</termName></specificMediaType>

<generalMediaTypeArray><generalMediaType><termName>Loose Sheets</termName></generalMediaType></generalMediaTypeArray>
</mediaOccurrence></mediaOccurrenceArray>

</fileUnitPhysicalOccurrence></physicalOccurrenceArray>

<digitalObjectArray>

"""

				digital_objects = """<digitalObject><objectType><termName>Image (JPG)</termName></objectType><labelFlag>""" + label_flag + """</labelFlag>
<objectDesignator>Fold3 File #""" + id + """</objectDesignator>
<objectDescription>Image provided by Fold3.</objectDescription>
<accessFilename>https://NARAprodstorage.s3.amazonaws.com/""" + file_path + """</accessFilename><accessFileSize>""" + str(file_size) + """</accessFileSize>
<thumbnailFilename>http://media.nara.gov/dc-metro/jpg_t.jpg</thumbnailFilename><thumbnailFileSize>1234</thumbnailFileSize></digitalObject>

"""
				DASxml_bottom = """</digitalObjectArray>
</fileUnit>

"""

## The final code: (1) creates a file for the DAS XML output if one does not yet exist, (2) writes each unique title to a separate CSV, (3) checks the CSV and writes DAS_top and digital_objects if the title is unique (it's a new file unit) or just digital_objects if it is not (it's an additional page within the current file unit), and then (4) writes the end tags for each completed file unit. It also logs each file unit in a separate log.txt, which is easier to read for progress than the full XML document.

				with open('uniquetest.csv', 'r') as log :
					test = False
					readlog = csv.reader(log, delimiter= '\t', quoting=csv.QUOTE_ALL)
					for row in readlog:
						if title == row[0]:
							test = True
							f = open(file + '_output.xml', 'a')
							f.write(digital_objects) 
							f.close()
# 							f = open('log.txt', 'a')
# 							f.write( '	' + '	' + label_flag + str(id) + str(file_size) + file_path + """
# """) 
# 							f.close()
				if test is False:
					with open('uniquetest.csv', 'a') as write:
						writelog = csv.writer(write, delimiter= '\t', quoting=csv.QUOTE_ALL)
						writelog.writerow( (title, ) )

					try:
						f = open(file + '_output.xml', 'r')
						f = open(file + '_output.xml', 'a')
						f.write(DASxml_bottom + DASxml_top + digital_objects) 
						f.close()
						sequence_order = sequence_order + 1
# 						f = open('log.txt', 'a')
# 						f.write(title + str(roll) + label_flag + str(id) + str(file_size) + file_path + """
# """) 
# 						f.close()
					except IOError:
						f = open(file + '_output.xml', 'a')
						f.write(DASxml_top + digital_objects) 
						f.close()
						sequence_order = sequence_order + 1
# 						f = open('log.txt', 'a')
# 						f.write(title + str(roll) + label_flag + str(id) + str(file_size) + file_path + """
# """) 
# 						f.close()
		
	except IOError:
		print '   Error: OBJECTS NOT FOUND FOR ' + id
		pass
	f = open(file + '_output.xml', 'a')
	f.write(DASxml_bottom)
	f.close()
	x = x + 1
	os.remove(file + '_metadata_(reformatted).xml')
	f = open('uniquetest.csv', 'w')
	f.write('') 
	f.close()