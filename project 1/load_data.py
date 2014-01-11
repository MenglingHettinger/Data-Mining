#!/usr/bin/env python

## LOAD ##
##########

def load_log(inPath):
    counter = 0.
    with open(inPath, 'r') as inFile:
        for line in inFile:
            a,b,c,d = line.split()
            if c == "-1":
                counter += 1
        print counter


def load_user_profile(inPath):
    """ Reads in the user_profile data.
        Returns a dictionary.  Each key
        is a single user.  Each value contains
        [id, yearofbirth, gender, #Tweets]
    """
    counter = 0.
    dataDic = {}
    with open(inPath, 'r') as inFile:
        for line in inFile:
            userID, year, gender, tweets, tag = line.split()
            # ageGroup
            try:
                YearInt = int(year)
            except:
                pass
            age = 2012 - YearInt
            if age < 0:
                continue
            ageGroup = age / 10
            if ageGroup > 5:
                ageGroup = 5
            

            # Gender
            if int(gender) not in [1,2]:
                continue


            row = [int(userID), ageGroup, gender, int(tweets), tag]
            tags = tag.split(';')
            nTags = len(tags)
            dataDic[int(userID)] = row
    print counter
    return dataDic

def load_item(inPath):
    """ Reads in the item data.
        Returns a dictionary.  Each key
        is a single item.  Each value contains
        [id, category, keyword]
    """
    dataDic = {} 
    with open(inPath, 'r') as inFile:
        for line in inFile:
            name, category, keyword = line.split()
            keywords = [int(k) for k in keyword.split(';')]
            row = [category, keywords]
            dataDic[int(name)] = row
    return dataDic

def load_user_keyword(inPath):
    """ Reads in the user_key_word data.
        Returns a dictionary.  Each key
        is a single item.  Each value contains
        [id, keyword(with weight)]
    """
    dataDic = {} 
    with open(inPath, 'r') as inFile:
        for line in inFile:
            thisKeywordDic = {}
            name, keyword = line.split()
            keywords = keyword.split(';')
            for i in keywords:
                key, freq = i.split(':')
                thisKeywordDic[int(key)] = float(freq)
            dataDic[int(name)] = thisKeywordDic
    return dataDic

def load_user_sns(inPath):
    """ Reads in the user_sns data.
        Returns a dictionary.  Each key
        is a single item.  Each value contains
        [id, category, keyword]
    """
    dataDic = {} 
    with open(inPath, 'r') as inFile:
        for line in inFile:
            follower, followee = line.split()
            sns = [follower, followee]
    return sns

def load_user_action(inPath):
    """ Reads in the user_action data.
        Returns a dictionary.  Each key
        is a single item.  Each value contains
        [id, dest, #of at action, #of retweet, #of comments ]
    """
    dataDic = {} 
    with open(inPath, 'r') as inFile:
        for line in inFile:
            name, dest, action, retweet, comment = line.split()
            row = [int(name), int(dest), int(action), int(retweet), int(comment) ]
            dataDic[int(name)] = row
    return dataDic

## WRITE ##
###########

def write_data_1(inPath, userKeywordData, itemData, outPath):
    """Method 1: user_key_word and item are used to find the common user_keyword and item_keyword, and calculate the distance between 
       the keywords table (also take into account the weight). e.g. if IK2 = UK3, IK3 = UK6, then 
       the distance D = weight(UK3)+weight(UK6). 
    """
    outFile = open(outPath, 'w')
    outFile.write('#userid,itemid,{keyword:frequency},result\n')
    with open(inPath, 'r') as inFile:
        for line in inFile:
            freq = 0.
            thisMatchingKeywordDict = {}
            userID, itemID, result, timestamp = line.split()
            itemKeywordList = itemData[int(itemID)][1]
            for kw in itemKeywordList:
                if kw in userKeywordData[int(userID)]:
                    thisMatchingKeywordDict[kw] = userKeywordData[int(userID)][kw]
                    freq += float(thisMatchingKeywordDict[kw])

                        
            outFile.write('%d,%d,"%s",%f,%d\n' % (int(userID), int(itemID), thisMatchingKeywordDict, freq, int(result)))
    outFile.close()

def write_data_1_short(inPath, userKeywordData, itemData, outPath):
    """Method 1: user_key_word and item are used to find the common user_keyword and item_keyword, and calculate the distance between 
       the keywords table (also take into account the weight). e.g. if IK2 = UK3, IK3 = UK6, then 
       the distance D = weight(UK3)+weight(UK6). 
    """
    counter = 0
    outFile = open(outPath, 'w')
    outFile.write('#userid,itemid,{keyword:frequency},result\n')
    with open(inPath, 'r') as inFile:
        for line in inFile:
            freq = 0.
            thisMatchingKeywordDict = {}
            userID, itemID, result, timestamp = line.split()
            itemKeywordList = itemData[int(itemID)][1]
            for kw in itemKeywordList:
                if kw in userKeywordData[int(userID)]:
                    thisMatchingKeywordDict[kw] = userKeywordData[int(userID)][kw]
                    freq += float(thisMatchingKeywordDict[kw])
            counter += 1
            if counter % 500000 == 0:
                #sys.stdout.write("Finished checking %d followings.\n" % counter)
                print "Finished reading %d lines" % (counter)

            if freq != 0:            
                outFile.write('%d,%d,%f,%d\n' % (int(userID), int(itemID), freq, int(result)))
    outFile.close()

def write_data_1_veryshort(inPath, userKeywordData, itemData, outPath):
    """Method 1: user_key_word and item are used to find the common user_keyword and item_keyword, and calculate the distance between 
       the keywords table (also take into account the weight). e.g. if IK2 = UK3, IK3 = UK6, then 
       the distance D = weight(UK3)+weight(UK6). 
    """
    counter = 0
    outFile = open(outPath, 'w')
    outFile.write('#freq,freqsq,result\n')
    with open(inPath, 'r') as inFile:
        for line in inFile:
            freq = 0.
            thisMatchingKeywordDict = {}
            userID, itemID, result, timestamp = line.split()
            itemKeywordList = itemData[int(itemID)][1]
            for kw in itemKeywordList:
                if kw in userKeywordData[int(userID)]:
                    thisMatchingKeywordDict[kw] = userKeywordData[int(userID)][kw]
                    freq += float(thisMatchingKeywordDict[kw])
            counter += 1
            if counter % 500000 == 0:
                #sys.stdout.write("Finished checking %d followings.\n" % counter)
                print "Finished reading %d lines" % (counter)

            if freq != 0:            
                outFile.write('%f,%f,%f,%d\n' % (freq, freq**2., freq**3., int(result)))
    outFile.close()


def write_data_2(inPath, itemData, outPath):
    """Method 2: item_data is used. Sort items by their categories, and see if some 
       categories are more likely to be accepted by others when recommended to the users.
    """
    outFile = open(outPath, 'w')
    outFile.write('@relation 1d_data\n@attribute Category numeric\n@attribute CategorySq numeric\n@attribute class {1,-1}\n@data\n')
    with open(inPath, 'r') as inFile:
        for line in inFile:
            userID, itemID, result, timestamp = line.split()
            thisItemData = itemData[int(itemID)]
            outFile.write('%d,%d,%d\n' % (int(thisItemData[0][0]), int(thisItemData[0][0])**2., int(result)))
    outFile.close()

def write_data_3(inPath, userProfileData, itemData, outPath):
    """Method 3: user_profile. Use attributes: age, gender.
       Gender = {1 = male,2 = female}
       age = {0 = <10, 1 = [10-19], 2 = [20-29], ...}
    """
    counter = 0
    outFile = open(outPath, 'w')
    outFile.write('@relation 2d_data\n@attribute age {0,1,2,3,4,5}\n@attribute gender {1,2}\n@attribute class {1,-1}\n@data\n')
    c = 0 
    with open(inPath, 'r') as inFile:
        for line in inFile:
            userID, itemID, result, timestamp = line.split()
            if int(userID) not in userProfileData:
                c += 1
                continue
            thisUserData = userProfileData[int(userID)]
            thisItemData = itemData[int(itemID)]
            outFile.write('%d,%d,"%s",%d\n' % (int(thisUserData[1]), int(thisUserData[2]), thisItemData[0], int(result)))
            counter += 1
            if counter % 500000 == 0:
                #sys.stdout.write("Finished checking %d followings.\n" % counter)
                print "Finished reading %d lines" % (counter)
    outFile.close()
    print c
    #print len(userProfileData)

def write_data_4(inPath, userProfileData, itemData, outPath):
    """Method 4: Use user_profile and item. Find correlation between (item_keyword)_i and (user_tag)_j, and compute the relation 
       between the correlation and the result for each user and item pair.
    """
    outFile = open(outPath, 'w')
    outFile.write('@relation 1d_data\n@attribute Yea numeric\n@attribute Sex numeric\n@attribute Tweets numeric\n@attribute TweetSq numeric\n@attribute class {1,-1}\n@data\n')
    counter = 0
    with open(inPath, 'r') as inFile:
        for line in inFile:
            userID, itemID, result, timestamp = line.split()
            try:
                thisUserData = userProfileData[int(userID)]
                thisItemData = itemData[int(itemID)]
            except KeyError:
                counter += 1
                continue
            outFile.write('%d,%d,"%s","%s",%d\n' % (int(userID), int(itemID), thisUserData[4], thisItemData[2], int(result)))
    print '%d method_4 lines skipped in %s' % (counter, outPath)
    outFile.close()

## MAIN ##
##########

def main():
    #load_log('rec_log_train.txt')
    userProfileData = load_user_profile('user_profile.txt')
    #userKeywordData = load_user_keyword('user_key_word.txt')
    itemData = load_item('item.txt')
    #write_data_1_short('rec_log_train.txt', userKeywordData, itemData, 'data_method_1_short.csv')
    #write_data_1_veryshort('rec_log_test_sample.txt', userKeywordData, itemData, 'data_test.csv')
    #write_data_2('rec_log_test_sample.txt', itemData, 'data_method_2_train.arff')
    #write_data_3('rec_log_train.txt', userProfileData, 'data_method_3_train.arff')
    write_data_3('rec_log_test_sample.txt', userProfileData, itemData, 'data_method_3_test.arff')
    #write_data_4('rec_log_test_sample.txt', userProfileData, itemData, 'data_method_4.csv')
 

if __name__ == "__main__":
    main()
