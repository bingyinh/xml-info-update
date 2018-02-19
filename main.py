## Bingyin Hu 20180217
## main script for xml file updates according to the updated xsd schema. 
## =============================================================================
## This code will call three scripts to finish the process. The first call is made
## to csv_completor.py, the description of the script:
## -----------------------------------------------------------------------------
## Users are required to prepare for a correctly formatted csv file that
## specifies all the actions required for transfering one xml from previous
## version of the xsd schema to the latest version in order. In other word,
## translate the change in schema into a series of "move", "rename", "add", or
## "remove" in the csv file. This code will automatically scan all xml files in
## the given directory and apply the same actions to them based on that csv file
## prepared by the user. Basically this code multiplies the actions for 
## [# of xml files] times to complete the csv file.
##
## This code also makes backup for the provided xml directory and the updated
## xml files are saved in a new directory with "_updated" attached to the given
## xml directory. For example: given xml directory "./xml/" then the updated
## xmls will be stored in "./xml_updated/".
## -----------------------------------------------------------------------------
## The second call is made to info_update_master.py, the description:
## -----------------------------------------------------------------------------
## This code asks for the csv file that contains all the actions required by the
## user and conduct those actions accordingly by calling the tools.
## -----------------------------------------------------------------------------
## The third call is made to xml_update_validator.py, the description:
## -----------------------------------------------------------------------------
## This code follows the xml updating codes to check whether the updated xml
## files are validate under the new xsd schema.
## -----------------------------------------------------------------------------
## When the code finishes running, the local xml files will be updated to fit
## the latest schema. The updated files will be validated with the xsd file. An
## error log will be generated.
##
## =============================================================================
## Input:   
## A prompt will ask for the directory of the csv file. The format of the csv
## file please refer to README.txt. A prompt will ask for the directory of the
## folder of the xml files. A prompt will ask for the schema ID. Another prompt
## will ask for the directory of the xsd schema file.

## =============================================================================
## Output:
## Void. A completed csv file, backup of xml files, updated xml files, and an
## error log of all wrongly updated xml files.

## =============================================================================
from csv_completor import runcsvCompletor
from info_update_master import runInfoUpdate
from xml_update_validator import runValidation

if __name__ == "__main__":
    csvDir = raw_input("Please type in the directory of the csv file:")
    while csvDir == "":
       csvDir = raw_input("Please type in the directory of the csv file:")
    xmlDir = raw_input("Please type in the directory of the folder of the xml files:")
    while xmlDir == "":
       xmlDir = raw_input("Please type in the directory of the folder of the xml files:")
    schemaID = raw_input("Please type in the schemaID:")
    while schemaID == "":
       schemaID = raw_input("Please type in the schemaID:")
    xsdDir = raw_input("Please type in the directory of the xsd schema file:")
    while xsdDir == "":
        xsdDir = raw_input("Please type in the directory of the xsd schema file:")
##    csvDir = "E:/Dropbox/DIBBS/data_update/info_update_xml/schema/042917to021918.csv"
##    xmlDir = "E:/Dropbox/DIBBS/data_update/info_update_xml/schema/xmlForUpdate2018-02-16/"
##    schemaID = '5904922ce74a1d36e1b78b7f' # PNC_schema_042917
##    xsdDir = "./schema/PNC_schema_021918.xsd"
    (backupDir, csvCompDir) = runcsvCompletor(csvDir, xmlDir, schemaID)
    if csvCompDir is not None and backupDir is not None:
        runInfoUpdate(csvCompDir)
        print "================================================================"
        print "Update completed!"
        print "================================================================"
        print "The completed csv file is stored in: \n" + csvCompDir
        print "----------------------------------------------------------------"
        print "Your updated xml files are stored in: \n" + backupDir
        print "================================================================"
    if backupDir is None:
        print "xml files backup failure! Please check for naming collision."
    elif csvCompDir is None:
        print "csv file completion failure! Please check your csv file."
    print "================================================================"
    print "Validation started!"
    logName = runValidation(xmlDir, xsdDir)
    print "================================================================"

