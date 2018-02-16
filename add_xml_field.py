## Bingyin Hu 20171115
## XML new field adding tool
## =============================================================================
## This code add new fields with infos specified by the user to the designiated
## xml file.

## =============================================================================
## Input:   
## 1] field to add
##    keyCass: a dict {{xml file 1: [[key cascade], [cascade], [cascade]...]},
##                      xml file 2: [[key cascade], [cascade], [cascade]...]}}
## 2] info to put in the new field, could be an empty string ''
##    infos: a dict {{xml file 1: [info 1, info 2, info 3...]},
##                    xml file 2: [info 1, info 2, info 3...]}}
## The keys of the two dicts are all xml file directories
## 3] a directory for saving the modified xml files

## =============================================================================
## Output:
## Void, but the xml file will be updated

## =============================================================================
import xml.etree.ElementTree as ET

# The function to add fields in several xml files in a batch
def batchXmlFieldAdd(keyCass, infos, saveDir):
    for xmlDir in keyCass: # equivalent to "for (xmlDir in infos):"
        singleXmlFieldAdd(xmlDir, keyCass, infos, saveDir)
        
# The function to add several fields in a single xml file
def singleXmlFieldAdd(xmlDir, keyCass, infos, saveDir):
    tree = ET.parse(xmlDir)
    root = tree.getroot()
    # unpack the two dicts keyCass and infos
    keylist = keyCass[xmlDir]
    infolist = infos[xmlDir]
    assert(len(keylist) == len(infolist))
    for x in xrange(len(keylist)):
        keyCas = keylist[x].split("/")
        pathExist = "./"
        for y in xrange(2, len(keyCas)):
            if (tree.find(pathExist + "/" + keyCas[y]) is None):
                newtree = tree.find(pathExist)
                ET.SubElement(newtree, keyCas[y])
                pathExist = pathExist + "/" + keyCas[y]
                # last node add info
                if (y == len(keyCas) - 1):
                    if (infolist[x] != ""):
                        newtree.find(keyCas[y]).text = infolist[x]
            else:
                pathExist = pathExist + "/" + keyCas[y]
    newXmlDir = saveDir + "/" + xmlDir.split("/")[-1]
    tree.write(newXmlDir)

## Test code
##xmlDir = "test2.xml"
##keyCass = {"test2.xml": ['.//DATA_SOURCE/Citation/CommonFields/Issue',
##                         './/DATA_SOURCE/Citation/CommonFields/AddTest1/AddTest2/AddTest3',
##                         './/MATERIALS/Filler/FillerComponent/ChemicalName/AddTest4']}
##infos = {"test2.xml": ['test issue', '', 'test chemical']}
##saveDir = "./test_xml"
##singleXmlFieldAdd(xmlDir, keyCass, infos, saveDir)
