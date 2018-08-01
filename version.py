#!/usr/bin/env python3

###
# To run this program, you need python 3.6.5 or higher.
###

import os
import re
import subprocess

major = 0  # release
minor = 0  # feature
patch = 0  # hotfix
uniqueVersionTag = "UNIQUE_VERSION_IDENTIFIER"


def getStdoutFromBashCommand(command):
    return subprocess.check_output(command, shell=True).decode('utf-8')


def findAllFilePathsContainingAStringReturnedFromAGrepCall(searchString):
    return getStdoutFromBashCommand("grep -R --exclude-dir=.git --exclude-dir=.vscode --exclude=version.py '" + searchString + "' .")


def storeInAnArray(searchString):
    return findAllFilePathsContainingAStringReturnedFromAGrepCall(searchString).split('\n')


def findAllUniqueFilePathsContainingAString(searchString):
    allFilePathsContainingTheSearchString = storeInAnArray(
        searchString)
    temporaryArrayUsedStoreTheFilteredGrepCallFilePathResults = []
    for aSingleFilePath in allFilePathsContainingTheSearchString:
        if stringIsInTheFile(searchString, aSingleFilePath) and not stringIsInTheFile("version.py", aSingleFilePath):
            lengthOfFilePathString = aSingleFilePath.find(':')
            temporaryArrayUsedStoreTheFilteredGrepCallFilePathResults += aSingleFilePath[:lengthOfFilePathString].split(
                "\n")
    return set(temporaryArrayUsedStoreTheFilteredGrepCallFilePathResults)


def stringIsInTheFile(searchString, filePath):
    return searchString in filePath


def setVersion(maj, min, pat):
    content = getStdoutFromBashCommand(f'cat {filePathToVersionTag}')
    newContent = re.sub(uniqueVersionTag, f"{maj}.{min}.{pat}", content)
    os.system(f"echo \'{newContent}\' > {filePathToVersionTag}")


def findAndReplace(find, replace):
    aSetOfFilesContainingTheSearchString = findAllUniqueFilePathsContainingAString(
        find)
    for filePath in aSetOfFilesContainingTheSearchString:
        content = getStdoutFromBashCommand(f'cat {filePath}')
        replaceCode = content.replace(find, replace).replace("'", "\'\"\'\"\'")
        os.system(f"echo \'{replaceCode}\' > {filePath}")


def getAllHotfixFeatureReleaseMerges():
    stdout = getStdoutFromBashCommand(f"git log --date=raw")
    array = re.findall(r"Date:   .{22}Merged in hotfix/.*?\n",
                       stdout, re.MULTILINE | re.DOTALL)
    array += re.findall(r"Date:   .{22}Merged in feature/.*?\n",
                        stdout, re.MULTILINE | re.DOTALL)
    array += re.findall(r"Date:   .{22}Merged in release/.*?\n",
                        stdout, re.MULTILINE | re.DOTALL)

    epochArray = toIntsList(array)
    quickSort(epochArray)
    sortedArray = matchArrayPositions(epochArray, array)
    return sortedArray


def toIntsList(array):
    result = []
    for item in array:
        result.append(int(re.findall(r"\d{10}", item)[0]))
    return result


def quickSort(alist):
    quickSortHelper(alist, 0, len(alist)-1)


def quickSortHelper(alist, first, last):
    if first < last:

        splitpoint = partition(alist, first, last)

        quickSortHelper(alist, first, splitpoint-1)
        quickSortHelper(alist, splitpoint+1, last)


def partition(alist, first, last):
    pivotvalue = alist[first]

    leftmark = first+1
    rightmark = last

    done = False
    while not done:

        while leftmark <= rightmark and alist[leftmark] <= pivotvalue:
            leftmark = leftmark + 1

        while alist[rightmark] >= pivotvalue and rightmark >= leftmark:
            rightmark = rightmark - 1

        if rightmark < leftmark:
            done = True
        else:
            temp = alist[leftmark]
            alist[leftmark] = alist[rightmark]
            alist[rightmark] = temp

    temp = alist[first]
    alist[first] = alist[rightmark]
    alist[rightmark] = temp
    return rightmark


def matchArrayPositions(sortedArray, array):
    result = []
    for epoch in sortedArray:
        for item in array:
            epoch2 = int(re.findall(r"\d{10}", item)[0])
            if epoch2 == epoch:
                result.append(item)
                break
            else:
                continue

    return result


def calculateVersion():
    global patch
    global minor
    global major

    sortedArray = getAllHotfixFeatureReleaseMerges()
    for item in sortedArray:
        if re.findall(r"Merged in hotfix/", item) != []:
            patch += 1
        elif re.findall(r"Merged in feature/", item) != []:
            patch = 0
            minor += 1
        elif re.findall(r"Merged in release/", item) != []:
            patch = 0
            minor = 0
            major += 1
        else:
            print("Something's wrong...")
    #setVersion(major, minor, patch)


def main():
    global filePathToVersionTag
    global uniqueVersionTag

    calculateVersion()

    findAndReplace(uniqueVersionTag, f"{major}.{minor}.{patch}")

    print("Calculated Version: " + str(major) +
          "." + str(minor) + "." + str(patch))


main()
