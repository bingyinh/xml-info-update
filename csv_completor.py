## Bingyin Hu 20180216
## CSV completion tool
## =============================================================================
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
##
## =============================================================================
## Input:   
## A prompt will ask for the directory of the csv file. The format of the csv
## file please refer to README.txt. A prompt will ask for the directory
## of the xml file. Another prompt will ask for the schema ID.

## =============================================================================
## Output:
## Void. A completed csv file and backup of xml files.

## =============================================================================
import os
import shutil # for xml backups
import glob
import csv

def backup(xmlDir, schemaID):
    # create the new folder for xml backups
    backupDir = xmlDir.strip('/') + "_updated/"
    if os.path.exists(backupDir):
        cont = raw_input('"' + backupDir + '"' + "already exists. Do you want to clear and recreate the directory? [Y/N]")
        if cont.lower() not in ['y', 'yes']:
            return
        else:
            shutil.rmtree(backupDir)
    os.makedirs(backupDir)
    xml_files = glob.glob(xmlDir + '*.xml') # find all xml files in xmlDir
    for xml_file in xml_files:
        if schemaID in xml_file:
            shutil.copy2(xml_file, backupDir)
    return backupDir

def csvCompletor(csvDir, backupDir):
    if not backupDir: # if backupDir has a collision, do nothing
        return
    actions = [] # save the actions
    headers = [] # save the headers
    # read the incompleted csv file
    with open (csvDir, 'rt') as f_in:
        reader = csv.DictReader(f_in)
        actions = list(reader)
        headers = reader.fieldnames
    csvCompDir = csvDir.strip('.csv') + 'completed.csv'
##    os.makedirs(csvCompDir) # create a new csv file
    # writing
    xml_files = glob.glob(backupDir + '*.xml') # find all xml files in xmlDir
    with open(csvCompDir, 'wb') as f_out:
        writer = csv.DictWriter(f_out, fieldnames = headers)
        writer.writeheader()
        for xml_file in xml_files:
            for row in actions:
                row['xml directory'] = xml_file
                writer.writerow(row)
    return csvCompDir

# a method for external calling of the script
def runcsvCompletor(csvDir, xmlDir, schemaID):
    backupDir = backup(xmlDir, schemaID)
    csvCompDir = csvCompletor(csvDir, backupDir)
    return (backupDir, csvCompDir)

if __name__ == "__main__":
    csvDir = raw_input("Please type in the directory of the csv file:")
    while csvDir == "":
       csvDir = raw_input("Please type in the directory of the csv file:")
    xmlDir = raw_input("Please type in the directory of the xml files:")
    while xmlDir == "":
       xmlDir = raw_input("Please type in the directory of the xml files:")
    schemaID = raw_input("Please type in the schemaID:")
    while schemaID == "":
       schemaID = raw_input("Please type in the schemaID:")
##    csvDir = "E:/Dropbox/DIBBS/data_update/info_update_xml/schema/042917to010918.csv"
##    xmlDir = "E:/Dropbox/DIBBS/data_update/info_update_xml/schema/xmlForUpdate2018-02-16/"
##    schemaID = '5904922ce74a1d36e1b78b7f' # PNC_schema_042917
    backupDir = backup(xmlDir, schemaID)
    csvCompletor(csvDir, backupDir)
