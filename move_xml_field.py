## Bingyin Hu 20171116
## XML existing field moving tool
## =============================================================================
## This code moves existing fields to another field specified by the user in the
## designiated xml file. 

## =============================================================================
## Input:   
## 1] field to move from
##    keyCassFrom: a dict {{xml file 1: [[key cascade], [cascade]...]},
##                          xml file 2: [[key cascade], [cascade]...]}}
## 2] field to move to
##    keyCassTo: a dict {{xml file 1: [[key cascade], [cascade]...]},
##                        xml file 2: [[key cascade], [cascade]...]}}
## The keys of the two dicts are all xml file directories
## 3] a directory for saving the modified xml files

## =============================================================================
## Output:
## Void, but the xml file will be updated

## =============================================================================
import xml.etree.ElementTree as ET
import copy

# The function to move fields in several xml files in a batch
def batchXmlFieldMove(keyCassFrom, keyCassTo, saveDir):
    for xmlDir in keyCassFrom: # equivalent to "for (xmlDir in keyCassTo):"
        singleXmlFieldMove(xmlDir, keyCassFrom, keyCassTo, saveDir)

# The function to find the first correctly matched fields with specified child
def findMyParent(tree, path, childTag):
    if tree.find(path) is None:
        # .find() finds the first match, if it's None then there isn't a match
        return None
    else:
        parents = tree.findall(path)
        for parent in parents:
            for child in list(parent):
                if child.tag == childTag:
                    return parent
    return None

# The function to move fields in a single xml file
def singleXmlFieldMove(xmlDir, keyCassFrom, keyCassTo, saveDir):
    # first insert (duplicate), then remove
    tree = ET.parse(xmlDir)
    root = tree.getroot()
    # unpack the two dicts keyCass and infos
    keyFromList = keyCassFrom[xmlDir]
    keyToList = keyCassTo[xmlDir]
    assert(len(keyFromList) == len(keyToList))
    for x in xrange(len(keyFromList)): # equivalent to xrange(len(keyToList)),
    # which stands for how many fields we'd like to move
        keyCasFrom = keyFromList[x].split("/")
        keyCasTo = keyToList[x].split("/")
        # Let's confirm whether the field to move exists or not
        pathExist = "./"
        # a flag for field existence
        exist = True
        for z in xrange(2, len(keyCasFrom)):
            if (tree.find(pathExist + "/" + keyCasFrom[z]) is None):
                print '"' + pathExist + "/" + keyCasFrom[z] + '"'
                print "This field does not exist. No moving done. Please check!"
                exist = False
                break
            else:
                pathExist = pathExist + "/" + keyCasFrom[z]
        # Now we have constructed the path of move-from field, let's find out
        # the occurrence of them in the xml
        occur = len(tree.findall(pathExist))
        if not exist:
            occur = 0
        print tree.findall(pathExist)
        dupPath = '' # to save the path to the last duplicated tag s.t. we can change its tag name
        realTag = '' # to save the real tag name for temporary tags
        for field in xrange(occur): # If occur is 0, we won't enter the loop
            # The way we move a field is to 1) copy the node 2) insert to the new
            # parent node 3) remove the original node
            # If the original node is one of the parent nodes of the moved node,
            # step 3) will remove the moved node together, so we need to identify
            # this case by comparing keyFromList[x] and keyToList[x].
            if keyFromList[x] in keyToList[x]:
                # Example:
                # keyFromList[x]: PolymerNanocomposite/PROCESSING/SolutionProcessing/ChooseParameter/Solvent
                # keyToList[x]: PolymerNanocomposite/PROCESSING/SolutionProcessing/ChooseParameter/Solvent/SolventName
                # destParent: Element (PolymerNanocomposite/PROCESSING/SolutionProcessing/ChooseParameter/ATempTagThatWantsNoSimilarity)
                # destParentTempCas: PolymerNanocomposite/PROCESSING/SolutionProcessing/ChooseParameter/
                dupKeyCasTo = copy.deepcopy(keyCasTo)
                dup = len(keyCasFrom) - 1 # the index of last duplicated tag in the keyCasTo
                dupKeyCasTo[dup] = 'ATempTagThatWantsNoSimilarity' + str(field)
                pathExist = "./"
                # create the move-to field with a temporary parent tag name
                for y in xrange(2, len(dupKeyCasTo) - 1):
                    if (findMyParent(tree, pathExist, dupKeyCasTo[y]) is None):
                        newtree = tree.find(pathExist)
                        if y == dup:
                            newtree = findMyParent(tree, pathExist, keyCasFrom[y])
                            print 'Line 98: ' + pathExist
                            print 'Line 99: ' + keyCasFrom[y]
                        ET.SubElement(newtree, dupKeyCasTo[y])
                        pathExist = pathExist + "/" + dupKeyCasTo[y]
                    else:
                        pathExist = pathExist + "/" + dupKeyCasTo[y]
                    if y == dup:
                        dupPath = pathExist
                # Element (./.../ChooseParameter/ATempTagThatWantsNoSimilarity
                destParent = tree.find(pathExist)
                # Now extract the element to be moved
                destParentTempCas = "./"
                realTag = keyCasFrom[-1] # the tag to replace 'ATempTagThatWantsNoSimilarity'
                
                for z in xrange(2, len(keyCasFrom)):
                    if (z == len(keyCasFrom) - 1):
                        # find the parent node of the field to remove
                        parent = findMyParent(tree, destParentTempCas, keyCasFrom[-1]) # Element (./.../ChooseParameter)
                        # Element (./.../ChooseParameter/Solvent)
                        child = tree.find(destParentTempCas + "/" + keyCasFrom[z])
                        child.tag = keyCasTo[-1] # rename the tag according to the specification of the user from Solvent to SolventName
                        destParent.insert(0, child) # now destParent is Element (./.../ChooseParameter/ATempTagThatWantsNoSimilarity/SolventName)
                        print 'Line 119: ' + ET.tostring(destParent)
                        print 'Line 120: ' + ET.tostring(parent)
                        # call remove(subfield)
                        parent.remove(child)
                    destParentTempCas = destParentTempCas + "/" + keyCasFrom[z]
            else:
                # If the field we'd like to move exists
                # Let's find the destination, if it does not exist, we create it
                pathExist = "./"
                for y in xrange(2, len(keyCasTo) - 1):
                    if (tree.find(pathExist + "/" + keyCasTo[y]) is None):
                        newtree = tree.find(pathExist)
                        ET.SubElement(newtree, keyCasTo[y])
                        pathExist = pathExist + "/" + keyCasTo[y]
                    else:
                        pathExist = pathExist + "/" + keyCasTo[y]
                # last node, save the node as the destination parent node
                destParent = tree.find(pathExist)
                # Let's find the field to move, insert it to the destination, and remove
                # the original field
                pathExist = "./"
                for z in xrange(2, len(keyCasFrom)):
                    # this if statement should not be entered anymore
                    if (tree.find(pathExist + "/" + keyCasFrom[z]) is None):
                        print '"' + pathExist + "/" + keyCasFrom[z] + '"'
                        print "This field does not exist. No moving done. Please check!"
                        break
                    else:
                        # last node then insert
                        if (z == len(keyCasFrom) - 1):
                            # find the parent node of the field to remove
                            parent = tree.find(pathExist)
##                            print pathExist
##                            print parent
##                            print '===='
                            child = tree.find(pathExist + "/" + keyCasFrom[z])
                            child.tag = keyCasTo[-1] # rename the tag according to the specification of the user
##                            print child
                            destParent.insert(0, child)
                            # call remove(subfield)
                            parent.remove(child)
                        pathExist = pathExist + "/" + keyCasFrom[z]
        # rename the 'ATempTagThatWantsNoSimilarity' all at once
        for field in xrange(occur):
            if len(dupPath) > 0:
                tempTag = tree.find(dupPath[:len(dupPath) - len(str(occur))] + str(field))
                tempTag.tag = realTag

    newXmlDir = saveDir + "/" + xmlDir.split("/")[-1]
    tree.write(newXmlDir)


## Test code
##xmlDir = "test2.xml"
##keyCassFrom = {"test2.xml": ['.//DATA_SOURCE/Citation/CommonFields/Title',
##                         './/DATA_SOURCE/Citation/CommonFields/AddTest1/AddTest2/AddTest3',
##                         './/DATA_SOURCE/Citation/CommonFields']}
##keyCassTo = {"test2.xml": ['.//DATA_SOURCE',
##                         './/DATA_SOURCE',
##                         './/MATERIALS/NewField']}
##saveDir = "./test_xml"
##singleXmlFieldMove(xmlDir, keyCassFrom, keyCassTo, saveDir)
