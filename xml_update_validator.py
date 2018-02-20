## Bingyin Hu 20180216
## XML update validator
## =============================================================================
## This code follows the xml updating codes to check whether the updated xml
## files are validate under the new xsd schema.

## =============================================================================
## Input:   
## A prompt will ask for the directory of the folder of the updated xml files.
## Another prompt will ask for the directory of the new xsd schema file. This
## script can also be imported as a function.

## =============================================================================
## Output:
## An error log.

## =============================================================================
from lxml import etree
import glob
from datetime import date
import csv

# A function that takes in the directory of the xml folder and the schema file,
# run the validation one by one and generate an error log.
def runValidation(xmlDir, xsdDir):
    xmlschema = etree.XMLSchema(etree.parse(xsdDir)) # parse the schema
    xml_files = glob.glob(xmlDir + '*.xml') # find all xml files in xmlDir
    errors = [] # a list of xml files that fail validation
    for xml_file in xml_files:
        xml = etree.parse(xml_file)
        if not xmlschema.validate(xml):
            errorInfo = str(xmlschema.error_log.last_error)
            errorInfo = errorInfo[errorInfo.rfind('SCHEMAV_ELEMENT_CONTENT:')+len('SCHEMAV_ELEMENT_CONTENT:'):-1]
            errors.append({'xml directory': xml_file.split("\\")[-1],
                           'error': errorInfo})
    logName = 'xml_validation_error_log_' + date.today().isoformat() + '.csv'
    with open(logName, 'wb') as f:
        writer = csv.DictWriter(f, fieldnames = ['xml directory', 'error'])
        writer.writerow({'xml directory':"Date: " + date.today().isoformat()})
        for error in errors:
            writer.writerow(error)
    return logName

if __name__ == "__main__":
    xmlDir = raw_input("Please type in the directory of the folder of the xml files:")
    while xmlDir == "":
        xmlDir = raw_input("Please type in the directory of the folder of the xml files:")
    xsdDir = raw_input("Please type in the directory of the xsd schema file:")
    while xsdDir == "":
        xsdDir = raw_input("Please type in the directory of the xsd schema file:")
    logName = runValidation(xmlDir, xsdDir)
    print "Errors are saved in the log: " + logName
