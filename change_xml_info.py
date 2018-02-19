## Bingyin Hu 20171115
## XML existing field info changing tool
## =============================================================================
## This code updates the designiated xml file with update info specified by
## the user.

## =============================================================================
## Input:
## 1] field to update
##    keyCass: a dict {{xml file 1: [[key cascade], [cascade], [cascade]...]},
##                      xml file 2: [[key cascade], [cascade], [cascade]...]}}
## 2] updated info to put in the field
##    infos: a dict {{xml file 1: [info 1, info 2, info 3...]},
##                    xml file 2: [info 1, info 2, info 3...]}}
## The keys of the two dicts are all xml file directories
## 3] a directory for saving the modified xml files

## =============================================================================
## Output:
## Void, but the xml file will be updated

## =============================================================================
import xml.etree.ElementTree as ET

# The function to update infos in several xml files in a batch
def batchXmlInfoUpdate(keyCass, infos):
    for xmlDir in keyCass: # equivalent to "for (xmlDir in infos):"
        singleXmlInfoUpdate(xmlDir, keyCass, infos)
        
# The function to update infos in several fields in a single xml file
def singleXmlInfoUpdate(xmlDir, keyCass, infos):
    tree = ET.parse(xmlDir)
    root = tree.getroot()
    # unpack the two dicts keyCass and infos
    keylist = keyCass[xmlDir]
    infolist = infos[xmlDir]
    assert(len(keylist) == len(infolist))
    for x in xrange(len(keylist)):
        if (tree.find(keylist[x]) is None):
            # print '"' + keylist[x] + '"'
            # print "This field does not exist. No change done. Please check!"
            continue
        else:
            tree.find(keylist[x]).text = infolist[x]
    # newXmlDir = saveDir + "/" + xmlDir.split("/")[-1]
    # tree.write(newXmlDir)
    tree.write(xmlDir, encoding="UTF-8", xml_declaration=True)

## Test codes    
##xmlDir = "test2.xml"
##keyCass = {"test2.xml": ['.//DATA_SOURCE/Citation/CommonFields/Title',
##                         './/DATA_SOURCE/Citation/CommonFields/Publisher',
##                         './/MATERIALS/Filler/FillerComponent/ChemicalName']}
##infos = {"test2.xml": ['test title', 'test publisher', 'test chemical']}
##saveDir = "./test_xml"
##singleXmlInfoUpdate(xmlDir, keyCass, infos, saveDir)
