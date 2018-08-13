## Bingyin Hu 20180302
## XML existing field moving tool
## =============================================================================
## This code moves existing fields to another field specified by the user in the
## designiated xml file. 

## =============================================================================
## Input:   
## 1] field to move from
##    keyCassFrom: a dict {'xml file 1': [[key cascade], [cascade]...],
##                         'xml file 2': [[key cascade], [cascade]...]}
## 2] field to move to
##    keyCassTo: a dict {'xml file 1': [[key cascade], [cascade]...],
##                       'xml file 2': [[key cascade], [cascade]...]}
## 3] index of field to move to
##    keyCassToIndex: a dict {'xml file 1': ['2', 'self'],
##                            'xml file 2': ['self', 'self']}
## The keys of the two dicts are all xml file directories
##
## =============================================================================
## Output:
## Void, but the xml file will be updated

## =============================================================================
import xml.etree.ElementTree as ET
import copy
import string

# The function to move fields in several xml files in a batch
def batchXmlFieldMove(keyCassFrom, keyCassTo, keyCassToIndex):
    for xmlDir in keyCassFrom: # equivalent to "for (xmlDir in keyCassTo):"
        singleXmlFieldMove(xmlDir, keyCassFrom, keyCassTo, keyCassToIndex)

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

# The function to find out the index of keyCasFrom if the tree exists more
# than one path that leads to the shared path of keyCasFrom and keyCasTo. For
# example, PolymerNanocomposite/MATERIALS/Filler/FillerComposition/ is a shared
# path between ".../volume" ".../mass" and ".../Fraction/volume"
# ".../Fraction/mass". The index of first occurence of keyCasFrom is returned.
def pathIndex(keyCasFrom, keyCasTo, tree):
    # print keyCasFrom
    # print keyCasTo
    ptr = 0 # a pointer used to find out the shared path, it will stop at the
    # first different string
    # print "keyCasFrom: " + str(keyCasFrom)
    # print "keyCasTo: " + str(keyCasTo)
    while ptr < len(keyCasFrom) and keyCasFrom[ptr] == keyCasTo[ptr]:
        ptr += 1
    if keyCasFrom[ptr-1] == 'ChooseParameter':
        ptr -= 1
    shared = keyCasFrom[0:ptr]
    sharedPath = string.join(shared, "/")
    matches = tree.findall(sharedPath)
    # print sharedPath
    # print matches
    # now we iterate through the matches of sharedPath to find the real match of
    # keyCasFrom
    index = 0 # the index of first occurence of keyCasFrom
    # print "========================"
    # print matches
    for match in matches:
        # inner loop
        for x in xrange(ptr, len(keyCasFrom)-1):
            # if keyCasFrom[x] is not a child
            if findMyParent(match, './', keyCasFrom[x+1]) is None:
                break
            # otherwise, update match to this child
            match = findMyParent(match, './', keyCasFrom[x+1])
            # if x moves all the way to the end of keyCasFrom
            if x == len(keyCasFrom) - 2:
                return (index, sharedPath, ptr)
        if ptr == len(keyCasFrom)-1:
            # if keyCasFrom[x] is not a child
            if match.find(keyCasFrom[ptr]) is not None:
                # match = match.find(keyCasFrom[ptr])
                return (index, sharedPath, ptr)
        # end of inner loop, add 1 to index
        index += 1
    return (-1, sharedPath, ptr)

# A helper function to find the furthest path that has at least given occurrence
# the search is done reversly
def occPath(keyCasTo, occurrence, tree):
    for x in xrange(len(keyCasTo),0,-1):
        trees = tree.findall(string.join(keyCasTo[0:x],'/'))
        if x < len(keyCasTo):
        # go into trees to find the ones with correct childtag
            realtrees = []
            for mytree in trees:
                for child in list(mytree):
                    if child.tag == keyCasTo[x]:
                        realtrees.append(mytree)
        else:
            realtrees = trees
        if len(realtrees) >= occurrence:
            return (x, string.join(keyCasTo[0:x],'/'), realtrees)
    return (-1, '', None)

# A function that help remove first empty field in an xml tree
def pinpointEmpty(tree):
    ## version 1
    # end = False
    # hardcap = 0 # run up to 1000 iterations
    # while not end and hardcap < 1000:
    #     end = True
    #     for field in tree.iter():
    #         # if we detect an empty field
    #         # print field
    #         if len(list(field)) == 0 and field.text is None:
    #             field.tag = "RRREEEMMOOOVVVEEEMMMEEE" # rename its tag
    #             treeStr = ET.tostring(tree.getroot()) # transform to string
    #             treeStr = treeStr.replace('<RRREEEMMOOOVVVEEEMMMEEE>', '') # remove leading tag
    #             treeStr = treeStr.replace('</RRREEEMMOOOVVVEEEMMMEEE>', '') # remove following tag
    #             treeStr = treeStr.replace('<RRREEEMMOOOVVVEEEMMMEEE />', '') # remove unpaired tag
    #             tree._setroot(ET.fromstring(treeStr)) # transform back to xml tree
    #             end = False
    #             break
    #     hardcap += 1
    # if hardcap == 1000:
    #     print tree.find('.//ID').text
    # return tree
    ## version 2
    end = False
    hardcap = 0 # run up to 1000 iterations
    treeStr = ET.tostring(tree.getroot()) # transform to string
    empty = '/><'
    while not end and hardcap < 1000:
        end = True
        if empty in treeStr:
            end = False
            right = treeStr.find(empty)
            left = treeStr.rfind('<',0,right) # find from right, start = 0, end = right
            treeStr = treeStr[0:left] + treeStr[right + len(empty) - 1:]
        hardcap += 1
    tree._setroot(ET.fromstring(treeStr)) # transform back to xml tree
    if hardcap == 1000:
        print tree.find('.//ID').text
    print empty in treeStr
    print tree.find('.//ID').text
    print '======================='
    return tree
# The function to move fields in a single xml file
def singleXmlFieldMove(xmlDir, keyCassFrom, keyCassTo, keyCassToIndex):
    # first insert (duplicate), then remove
    tree = ET.parse(xmlDir)
    root = tree.getroot()
    # unpack the two dicts keyCass and infos
    keyFromList = keyCassFrom[xmlDir]
    keyToList = keyCassTo[xmlDir]
    keyToIndexList = keyCassToIndex[xmlDir]
    assert(len(keyFromList) == len(keyToList) == len(keyToIndexList))
    for x in xrange(len(keyFromList)): # equivalent to xrange(len(keyToList)),
    # which stands for how many fields we'd like to move
        keyCasFrom = keyFromList[x].split("/")
        print keyFromList[x]
        keyCasTo = keyToList[x].split("/")
        keyCasToIndex = keyToIndexList[x].lower()
        # default substitution of unspecified index is "self"
        if keyCasToIndex == '':
            keyCasToIndex = 'self'
        # Let's confirm whether the field to move exists or not
        pathExist = string.join(keyCasFrom, '/')
        # a flag for field existence
        exist = True
        if tree.find(pathExist) is None:
            exist = False
            continue
        # for z in xrange(2, len(keyCasFrom)):
        #     if (tree.find(pathExist + "/" + keyCasFrom[z]) is None):
        #         # print '"' + pathExist + "/" + keyCasFrom[z] + '"'
        #         # print "This field does not exist. No moving done. Please check!"
        #         exist = False
        #         break
        #     else:
        #         pathExist = pathExist + "/" + keyCasFrom[z]

        # Now we have constructed the path of move-from field, let's find out
        # the occurrence of them in the xml
        occur = len(tree.findall(pathExist))
        # if not exist:
        #     occur = 0
        # print tree.findall(pathExist)
        # Case 1: "self"
        if keyCasToIndex == 'self':
            dupPath = '' # to save the path to the last duplicated tag s.t. we can change its tag name
            realTag = '' # to save the real tag name for temporary tags
            for field in xrange(occur): # If occur is 0, we won't enter the loop
                # find out the index of keyCasFrom in the tree.findall() outputs
                (index, sharedPath, ptr) = pathIndex(keyCasFrom, keyCasTo, tree)
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
                    dup = ptr - 1 # the index of last duplicated tag in the keyCasTo
                    dupKeyCasTo[dup] = 'ATempTagThatWantsNoSimilarity' + str(field)
                    pathExist = string.join(dupKeyCasTo[0:dup], '/')
                    # create the move-to field with a temporary parent tag name
                    for y in xrange(dup, len(dupKeyCasTo) - 1):
                        if findMyParent(tree, pathExist, dupKeyCasTo[y]) is None:
                            newtree = tree.find(pathExist)
                            if y == dup:
                                newtree = findMyParent(tree, pathExist, keyCasFrom[y])
                            ET.SubElement(newtree, dupKeyCasTo[y])
                            pathExist = pathExist + "/" + dupKeyCasTo[y]
                        else:
                            pathExist = pathExist + "/" + dupKeyCasTo[y]
                        if y == dup:
                            dupPath = pathExist
                    # Element (./.../ChooseParameter/ATempTagThatWantsNoSimilarity
                    destParent = tree.find(pathExist)
                    # Now extract the element to be moved
                    destParentTempCas = string.join(keyCasFrom[0:dup], '/')
                    realTag = keyCasFrom[-1] # the tag to replace 'ATempTagThatWantsNoSimilarity'
                    
                    for z in xrange(dup, len(keyCasFrom)):
                        # print destParentTempCas
                        if (z == len(keyCasFrom) - 1):
                            # find the parent node of the field to remove
                            parent = findMyParent(tree, destParentTempCas, keyCasFrom[-1]) # Element (./.../ChooseParameter)
                            # Element (./.../ChooseParameter/Solvent)
                            child = tree.find(destParentTempCas + "/" + keyCasFrom[z])
                            child.tag = keyCasTo[-1] # rename the tag according to the specification of the user from Solvent to SolventName
                            destParent.insert(len(destParent), child) # now destParent is Element (./.../ChooseParameter/ATempTagThatWantsNoSimilarity/SolventName)
                            # call remove(subfield)
                            parent.remove(child)
                        destParentTempCas = destParentTempCas + "/" + keyCasFrom[z]
                else:
                    # If the field we'd like to move will not be moved to the
                    # sublevel of a field that has the same tag
                    # Let's find the destination, if it does not exist, we create it
                    pathExist = sharedPath
                    treeNow = tree.findall(pathExist)[index]
                    for y in xrange(ptr, len(keyCasTo) - 1):
                        if (len(treeNow.findall(keyCasTo[y])) == 0):
                        # if (len(tree.findall(pathExist + "/" + keyCasTo[y])) < index+1):
                            # newtree = tree.findall(pathExist)[index]
                            ET.SubElement(treeNow, keyCasTo[y])
                        #     pathExist = pathExist + "/" + keyCasTo[y]
                        # else:
                        #     pathExist = pathExist + "/" + keyCasTo[y]
                        pathExist = pathExist + "/" + keyCasTo[y]
                        treeNow = treeNow.find(keyCasTo[y])
                    # last node, save the node as the destination parent node
                    # destParent = tree.findall(pathExist)[index]
                    destParent = treeNow
                    # Let's find the field to move, insert it to the destination, and remove
                    # the original field
                    pathExist = sharedPath
                    treeNow = tree.findall(pathExist)[index]
                    for z in xrange(ptr, len(keyCasFrom)):
                        # this if statement should not be entered anymore
                        if (treeNow.find(keyCasFrom[z]) is None):
                            break
                        else:
                            # last node then insert
                            if (z == len(keyCasFrom) - 1):
                                # print treeNow
                                # find the parent node of the field to remove
                                # parent = findMyParent(tree, pathExist, keyCasFrom[-1])
                                parent = treeNow
                                child = treeNow.find(keyCasFrom[z])
                                child.tag = keyCasTo[-1] # rename the tag according to the specification of the user
                                destParent.insert(len(destParent), child)
                                # call remove(subfield)
                                parent.remove(child)
                            pathExist = pathExist + "/" + keyCasFrom[z]
                            treeNow = treeNow.find(keyCasFrom[z])
            # rename the 'ATempTagThatWantsNoSimilarity' all at once
            lastField = field
            for field in xrange(occur):
                if len(dupPath) > 0:
                    tempTag = tree.find(dupPath[:len(dupPath) - len(str(lastField))] + str(field))
                    tempTag.tag = realTag
        # Case 2: index
        elif keyCasToIndex.isdigit():
            for field in xrange(occur): # If occur is 0, we won't enter the loop
                (index, sharedPath, ptr) = pathIndex(keyCasFrom, keyCasTo, tree)
                # get the correct destination tree
                treeTo = tree.findall(sharedPath)[index]
                kCTI = int(keyCasToIndex) # convert to int
                # Find the furthest path that has at least "keyCasToIndex" occurrence
                (occPtr, pathExist, trees) = occPath(keyCasTo[ptr:-1], kCTI, treeTo)
                if occPtr <= 0:
                    continue
                # create fields by keyCasTo if they are not existed
                # print trees
                treeNow = trees[kCTI-1]
                for y in xrange(ptr+occPtr, len(keyCasTo) - 1):
                    # print keyCasTo[y]
                    if (len(treeNow.findall(keyCasTo[y])) == 0):
                        ET.SubElement(treeNow, keyCasTo[y])
                    # pathExist = pathExist + "/" + keyCasTo[y]
                    treeNow = treeNow.find(keyCasTo[y])
                # last node, save the node as the destination parent node
                destParent = treeNow
                # Let's find the field to move, insert it to the destination, and remove
                # the original field
                pathExist = sharedPath
                treeFrom = tree.findall(pathExist)[index]
                for z in xrange(ptr, len(keyCasFrom)-1):
                    pathExist = pathExist + "/" + keyCasFrom[z]
                    treeFrom = findMyParent(treeFrom,'./',keyCasFrom[z+1])
                    # last node then insert
                    if (z == len(keyCasFrom) - 2):
                        # find the parent node of the field to remove
                        # parent = findMyParent(tree, pathExist, keyCasFrom[-1])
                        parent = treeFrom
                        child = treeFrom.find(keyCasFrom[-1])
                        child.tag = keyCasTo[-1] # rename the tag according to the specification of the user
                        destParent.insert(len(destParent), child) # by default insert to the end of the branch
                        # call remove(subfield)
                        parent.remove(child)
                print "under construction"

    # END OF THE LOOP
    # Final check of empty fields
    # tree = pinpointEmpty(tree)
    # newXmlDir = saveDir + "/" + xmlDir.split("/")[-1]
    # tree.write(newXmlDir)
    tree.write(xmlDir, encoding="UTF-8", xml_declaration=True)
    # tree.write(xmlDir + 'new.xml', encoding="UTF-8", xml_declaration=True)

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
