#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6


import time


def bruteForce(pzl, lookup, chars, count, constraints):
    # print("bF:")
    # printString(pzl)
    # places, newPzl = makeDeductions(lookup, pzl, chars)
    newChar, syms, pzl = findPlacesforSymbols(lookup, pzl, constraints)
    newIndex, places = findSymbolsForPlaces(lookup, pzl, chars)
    # print("newIndex: {}, places: {}".format(newIndex, places))
    # if len(places) == 0: return pzl
    # print("bf:")
    # printString(pzl)
    # print("newIndex:",newIndex)
    if newChar == "done" or newIndex < 0: return pzl
    # print("newChar: {}, syms: {}".format(newChar, syms))
    # print("places[newIndex]:", places[newIndex])
    # print("newChar:", newChar)
    # print("syms:", syms)
    # print("syms[newChar]:", syms[newChar])
    if len(places[newIndex]) <= len(syms[newChar]):
        for char in places[newIndex]:
            subPzl = pzl[:newIndex] + char + pzl[newIndex + 1:]
            bF = bruteForce(subPzl, lookup, chars, count, constraints)
            if bF: return bF
    else:
        for index in syms[newChar]:
            subPzl = pzl[:index] + newChar + pzl[index + 1:]
            # print("index:", index)
            # print("newChars:", newChar)
            # print("syms[chars]:", syms[newChar])
            # print("subPzl:")
            # printString(subPzl)
            bF = bruteForce(subPzl, lookup, chars, count, constraints)
            if bF: return bF
    return ""


def findPlacesforSymbols(lookup, pzl, constraints):
    # symbolsToPlaces = {char: {i for i in range(len(pzl))} for char in "123456789"}
    # for index in range(len(pzl)):
    #     if pzl[index] != ".":
    #         for key in symbolsToPlaces:
    #             symbolsToPlaces[key].discard(index)
    #         # symbolsToPlaces[pzl[index]].discard(index)
    #         for place in lookup[index]:
    #             symbolsToPlaces[pzl[index]].discard(place)
    #         if len(symbolsToPlaces[pzl[index]]) == 0:
    #             symbolsToPlaces.pop(pzl[index])
    # smallestChar = list(symbolsToPlaces.keys())[0]
    # for key in symbolsToPlaces:
    #     if len(symbolsToPlaces[smallestChar]) > len(symbolsToPlaces[key]):
    #         smallestChar = key
    # print("findPlacesForSymbols<")
    finalBlankMatch = dict()
    for s in constraints:
        blanks = set()
        possibles = {i for i in "123456789"}
        blankMatch = dict()
        for index in s:
            if pzl[index] != ".":
                possibles.discard(pzl[index])
            else:
                blanks.add(index)
        if len(possibles) == 0: continue
        blankMatch = {char: set(blanks) for char in possibles}
        for index in blanks:
            # print("blanks:", blanks)
            for neigh in lookup[index]:
                if pzl[neigh] in blankMatch:
                    blankMatch[pzl[neigh]].discard(index)
        #     print("blanksAfter:", blanks)
        # print("blankMatch:", blankMatch)
        blankMatch, pzl, isA = findMin(blankMatch, pzl)
        while isA:
            blankMatch, pzl, isA = findMin(blankMatch, pzl)
        finalBlankMatch.update(blankMatch)
    l = [char for char in finalBlankMatch]
    # print("l:",l)
    if len(l) == 0:
        return "done", finalBlankMatch, pzl
    smallestChar = l.pop(0)
    # print("firstSmall:", smallestChar)
    # print("finalBlankMatch:", finalBlankMatch)
    for key in finalBlankMatch:
        if len(finalBlankMatch[smallestChar]) > len(finalBlankMatch[key]):
            smallestChar = key
    # print("smallestChar:", smallestChar)
    return smallestChar, finalBlankMatch, pzl


def findMin(blankMatch, pzl):
    for char in blankMatch:
        if len(blankMatch[char]) == 1:
            r = blankMatch[char].pop()
            pzl = pzl[:r] + char + pzl[r + 1:]
            blankMatch.pop(char)
            for otherChar in blankMatch:
                blankMatch[otherChar].discard(r)
            return blankMatch, pzl, True
    return blankMatch, pzl, False


def findSymbolsForPlaces(lookup, pzl, chars):
    places = dict()
    smallestIndex = pzl.find(".")
    for index in range(len(pzl)):
        if pzl[index] == ".":
            possibles = set(chars)
            for i in lookup[index]:
                if pzl[i] in possibles:
                    possibles.discard(pzl[i])
            places[index] = possibles
            if len(possibles) < len(places[smallestIndex]):
                smallestIndex = index
            if len(places[smallestIndex]) == 1:
                return smallestIndex, places
    return smallestIndex, places


def makeBoard(bigSides, littleSides):
    affectLookup = dict()
    constraint = list()
    rows, constraint = makeRows(bigSides, constraint)
    cols, constraint = makeCols(bigSides, constraint)
    boxes, constraint = makeBoxes(littleSides, littleSides, bigSides, constraint)
    for indexr in range(bigSides):
        for indexc in range(bigSides):
            affects = set().union(rows[(indexr, indexc)], cols[(indexr, indexc)], boxes[(indexr, indexc)])
            affects.remove((indexr, indexc))
            affectLookup[(indexr, indexc)] = affects
    newLookup = matchBoardWithString(affectLookup, bigSides)
    return newLookup, convertConstraints(constraint, bigSides)


def convertConstraints(constraint, bigSides):
    new = list()
    for aSet in constraint:
        newSet = set()
        for row, col in aSet:
            newSet.add(row * bigSides + col)
        new.append(newSet)
    return new


def matchBoardWithString(boardLookup, bigSides):
    newLookup = dict()
    for key in boardLookup.keys():
        aSet = set()
        for matches in boardLookup[key]:
            aSet.add(matches[0] * bigSides + matches[1])
        newLookup[key[0] * bigSides + key[1]] = aSet
    return newLookup


def makeRows(bigSides, constraint):
    rows = dict()
    for col in range(bigSides):
        aRow = set()
        for row in range(bigSides):
            aRow.add((row, col))
        for index in aRow:
            rows[index] = aRow
        constraint.append(aRow)
    return rows, constraint


def makeCols(bigSides, constraint):
    cols = dict()
    for row in range(bigSides):
        aCol = set()
        for col in range(bigSides):
            aCol.add((row, col))
        for index in aCol:
            cols[index] = aCol
        constraint.append(aCol)
    return cols, constraint


def makeBoxes(width, height, bigSides, constraint):
    boxes = dict()
    row = 0
    col = 0
    while row < bigSides:
        while col < bigSides:
            box = set()
            for indexr in range(row, row + width):
                for indexc in range(col, col + height):
                    box.add((indexr, indexc))
            for pair in box:
                boxes[pair] = box
            constraint.append(box)
            col += height
        row += width
        col = 0
    return boxes, constraint


def printString(board):
    for num in range(9):
        print(list(board[num * 9: num * 9 + 9]))
    print()


sTime = time.clock()
pzls = [line.rstrip() for line in open("puzzles.txt")]
bigSides = 9
littleSides = 3
# sTime = time.clock()
lookup, constraints = makeBoard(bigSides, littleSides)
# print(constraints)
startTime = time.clock()
count = 0
for pzl in pzls:
    count += 1
    # if count == 60: break
    print("Number",count)
    printString(pzl)
    start = time.clock()
    printString(bruteForce(pzl, lookup, {"1", "2", "3", "4", "5", "6", "7", "8", "9"}, count, constraints))
    print("Time for Pzl:", time.clock() - start)
    print("Time so far:", time.clock() - sTime)
print("Total Time:", time.clock() - startTime)