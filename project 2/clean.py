def clean_meta(inPath):
    """
    """
    #outFile = open(outPath, 'w')
    dataDic = {}
    thisID = -1
    with open(inPath, 'r') as inFile:
        for line in inFile:
            if line.startswith('Id:'):
                thisID = int(line.split()[1])
                #print thisID
                dataDic[thisID] = None
            elif line.lstrip().startswith('group:'):
                dataDic[thisID] = line.split()[1]
            #elif line.lstrip().startswith('categories: '):
                #dataDic[thisID] += ', '+ line.split()[1]
                

    #print dataDic[42]
    #print len(dataDic)

    cleanMetaDataDic = {}
    for key in dataDic:
        if dataDic[key] is None:
            continue
        else:
            cleanMetaDataDic[key] = dataDic[key]
            #outFile.write('%s:%s\n' % (key, cleanMetaDataDic[key]))
    return cleanMetaDataDic
    

    #outFile.close()

def load_group(inPath,outPath):
    outFile = open(outPath,'w')
    with open(inPath, 'r') as inFile:
        for line in inFile:
            v = line.split(", ")
            for i in v:
                i = i.strip().strip(',')

                try:
                    outFile.write('%s\n' % int(i))
                except:
                    print i
    outFile.close()
    #return v
    

def write_clean_transaction(inPath, groupPath, cleanMetaDataDic, outPath):
    outFile = open(outPath, 'w')
    group = []
    with open(groupPath, 'r') as groupFile:
        for line in groupFile:
            if len(line) == 0:
                continue
            try:
                group.append(int(line.strip()))
            except:
                print line

        #group = [int(line.strip()) for line in groupFile.readlines()]


    with open(inPath, 'r') as inFile:
        counter = 0
        for line in inFile:
            if len(line) == 0: continue
            v1, v2 = line.split()
            if (int(v1) not in cleanMetaDataDic) or (int(v2) not in cleanMetaDataDic) or (int(v1) not in group) or (int(v2) not in group):
                continue
            counter += 1
            print counter
            
            outFile.write('%s %s\n' % (v1, v2))

    outFile.close()


def assign_weight(inPath, outPath):
    outFile = open(outPath, 'w')
    with open(inPath, 'r') as inFile:
        for line in inFile:
            v1, v2 = line.split()
            outFile.write('%s %s %s\n' % (v1, v2, 1) )


def customer_dictionary(inPath):
    customerDict = {}
    #outFile = open(outPath, 'w')
    with open(inPath, 'r') as inFile:
        for line in inFile:
            if line.startswith("Id:"):
                itemId, itemIdNum = line.split()
                itemIdNum = int(itemIdNum)
            else:
                date, cutomer, customerId, rating, rateNum, votes,votesNum, helpful, helpfulNum = line.split()
                if customerId in customerDict:
                    customerDict[customerId].append(itemIdNum)
                else:
                    customerDict[customerId] =  [itemIdNum]
        print customerDict




def item_dictionary(inPath):
    itemDict = {}
    #outFile = open(outPath, 'w')
    with open(inPath, 'r') as inFile:
        for line in inFile:
            if line.startswith("Id:"):
                itemId, itemIdNum = line.split()
                itemIdNum = int(itemIdNum)
                itemDict[itemIdNum] = []
            else:
                try:
                    stringTuples = line.split()
                    customerId = stringTuples[2]
                except:
                    print line
   
                itemDict[itemIdNum].append(customerId)

        return itemDict

def update_weight(inPath, itemDict, outPath):
    outFile = open(outPath, 'w')
    with open(inPath,'r') as inFile:
        for line in inFile:
            v1, v2, weight = line.split()
            v1 = int(v1)
            v2 = int(v2)
            weight = int(weight)
            try:
                for i in itemDict[v1]:
                    if i in itemDict[v2]:
                        weight = weight + 1
            except:
                continue

            outFile.write('%s %s %s\n' % (v1, v2, weight) )
    outFile.close()


def read_transaction(inPath):
    counter  = 0 
    prodList = []
    with open(inPath,'r') as inFile:
        for line in inFile:
            v1, v2 = line.split()
            v1 = int(v1)
            v2 = int(v2)
            if (v1 in prodList) and (v2 in prodList):
                continue
            elif (v1 not in prodList) and (v2 not in prodList):
                prodList.append(v1)
                prodList.append(v2)
            elif v1 not in prodList and (v2 in prodList):
                prodList.append(v1)
            elif v2 not in prodList and (v1 in prodList):
                prodList.append(v2)
            
            counter += 1
            print counter
    return prodList

def read_transaction2(inPath):
    counter  = 0 
    productDictionary = {}
    with open(inPath,'r') as inFile:
        for line in inFile:
            v1, v2 = line.split()
            v1 = int(v1)
            v2 = int(v2)
            productDictionary[v1] = None
            productDictionary[v2] = None
            counter += 1
            if counter % 100000 == 0:
                print counter
    return productDictionary


def get_groundtruth(inPath, productDictionary, outPath):
    outFile = open(outPath, 'w')
    with open(inPath,'r') as inFile:
        for line in inFile:
            product, group = line.split(":")
            product = int(product)
            if product in productDictionary:
                outFile.write('%d %s\n' % (product, group.strip()))
    outFile.close()

def count_accuracy(inPath, outPath):
    outFile = open(outPath,'w')
    count1 = 0
    count2 = 0
    with open(inPath,'r') as inFile:
        for line in inFile:
            productNum, group, result1, result2 =  line.split()
            if group == "Book":
                groupNum = 1
            if group == "Music":
                groupNum = 2
            if group == "Video":
                groupNum = 4
            if group == "DVD":
                groupNum = 3
            if group == "Toy":
                groupNum = 5
            if group == "CE":
                groupNum = 6
            if group == "Software":
                groupNum = 7
            if group == "Baby":
                groupNum = 8
            if group == "Sports":
                groupNum = 9
            if group == "Video Games":
                groupNum = 10
            outFile.write('%s %s %s %s %s\n' %(productNum, group, groupNum, result1, result2))
            if int(groupNum) == int(result1):
                count1 += 1
            if int(groupNum) ==  int(result2):
                count2 += 1
    outFile.close()
    print count1
    print count2






def main():
    #cleanMetaDataDic = clean_meta('amazon-meta.txt')
    #load_group("groups_clean.txt","groups_clean_test.txt")
    #write_clean_transaction('Amazon0601.txt', "groups_clean_test.txt", cleanMetaDataDic, 'Amazon0601_clean.txt')
    #assign_weight("Amazon0601_clean.txt", "Amazon0601_weighted.txt")
    #customer_dictionary("amazon-meta-small-clean.txt")
    #itemDictionary = item_dictionary("amazon-meta-customer.txt")
    #update_weight("Amazon0601_weighted.txt", itemDictionary, "weight_update.txt" )
    #productDictionary = read_transaction2("Amazon0601_clean.txt")
    #get_groundtruth("amazon_meta_clean", productDictionary, "groundtruth.txt")
    count_accuracy("result", "accuracy")

if __name__ == "__main__":
    main()
