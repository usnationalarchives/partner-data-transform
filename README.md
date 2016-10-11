# partner-data-transform
This repo contains the files necessary to transform the data from partner digitization projects into a format compliant with the data scheme to import to the Description and Authority Service (DAS) for inclusion in the [National Archives Catalog](https://catalog.archives.gov).

Download this repo as it exists for a working directory: 
* Partner XML files will need to be placed in the /metadata folder
* S3 Manifester CSV file will need to be placed in the /objects folder
* Python scripts will need to be modified for each new instance

## /metadata
Partner XML metadata for each microfilm publicaton must go in the metadata folder. Samples for a publication can be found in the [metadata folder here](https://github.com/usnationalarchives/partner-data-transform/tree/master/metadata).

## /objects
The CSV file generated by the S3 Manifester must go in the objects folder. Samples for a publication can be found in the [objects folder here](https://github.com/usnationalarchives/partner-data-transform/tree/master/objects).

## Python scripts
Python scripts must be modified for each new instance. Notes for where to modify scripts can be found in the comments of each.

Python scripts must be run in the following order:

1. [s3_csv_split.py](https://github.com/usnationalarchives/partner-data-transform/blob/master/s3_csv_split.py)
  * This script takes the CSV file we get with all the digital image filepaths from the Amazon S3 cloud and breaks them out per microfilm roll.
2. [reformat_partner_xml.py](https://github.com/usnationalarchives/partner-data-transform/blob/master/reformat_partner_xml.py)
  * This script reformats the partner xml into a DAS xml format, then marries the xml with the digital object filepaths.
3. [combine_xml.py](https://github.com/usnationalarchives/partner-data-transform/blob/master/combine_xml.py)
  * This script combines multiple xml files for each microfilm roll into one for bulk import

*All scripts in this repo are written in [Python 2.7](https://www.python.org/download/releases/2.7/).*

## Other files
The following files must be in the working directory as they exist here:
* .DS_store
* .gitignore
* log.txt - *must be empty*
* uniquetest.csv - *must be empty*
