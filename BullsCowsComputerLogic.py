import random
import itertools
from operator import pos
import operator

#===============================================================================
# FindMatches - A method solving the original assignment
#===============================================================================

def FindMatches(strAnswer,strGuess):
    """
    Finds how many bulls and cows are in a particular guess.
    Parameters
    ----------
    strAnswer : str
        The number to guess in string format
    strGuess : str
        The actual guess is string format
    Returns
    -------
        (int,int)
        A tuple of 2 integers - Number of bulls and the number of Cows
    """
    nrBulls, nrCows = 0,0
    for i in range(len(strGuess)):
        if strGuess[i] == strAnswer[i]:
            nrBulls+=1
        else:
            if strGuess[i] in strAnswer:
                nrCows+=1
    return nrBulls,nrCows 

#===============================================================================
# This part contains all the functions used in Algorithm nr.1
# 
# Some of the functions are being used in Algorithm nr.2
#===============================================================================


def EliminatePossiblePositions(dctPositions, strActNumber):
    """
    Elimination of impossible positions
    
    Example: guess 1234 returns 0 bulls, none of the digits can be on its actual position
        e.g. 1 cant be on position 0
    Parameters
    ----------
    dctPositions : dict
        A dictionary containing all 10 digits and their possible positions in the guessed number
    strActNumber : str
        A 4 digit guess
    Returns
    -------
    None    
    """
    for i in range(len(strActNumber)):
        dctPositions[int(strActNumber[i])][1][i] = False

def EliminateNumber(dctPositions, strActNumber):
    """
    Elimination of whole numbers
    
    This method eliminates all digits in the actual guess from the dictionary of possible digits
    
    Example: if a guess returns 0 bulls and 0 cows, none of the digits are present in the guessed number
    Parameters
    ----------
    dctPositions : dict
        A dictionary containing all 10 digits and their possible positions in the guessed number
    strActNumber : str
        must be a string containing only digits
    Returns
    -------
    None    
    """    
    for i in range(len(strActNumber)):
        dctPositions[int(strActNumber[i])][0] = False
        dctPositions[int(strActNumber[i])][1] = [False]*4

def UpdateEliminationState(lstNumbersEliminated,dctPositions):
    """
    Finds out if a digit is eliminated
    
    Loops through all digits in the dictionary of digits, and if finds a digit where every position is impossible (False), 
        sets the digit to false (cant be in the guessed number) and adds it to the list of eliminated digits
    Parameters
    ----------
    lstNumbersEliminated : list
        A list containing numbers that cant be present in the guessed number
    dctPositions : dict
        A dictionary containing all 10 digits and their possible positions in the guessed number
    Returns
    -------
    None   
    """        
    for number in dctPositions:
        if dctPositions[number][1] == [False]*4:
            dctPositions[number][0] = False
            if number not in lstNumbersEliminated: lstNumbersEliminated.append(number)

def NumberOfMatchingNumsInString(strNumber,dctPositions):
    """
    Finds out how many possible digits are present in the current guess
    
    If a digits 0-th element in the dictionary is True, it is certainly present in the guessed number 
    Parameters
    ----------
    strNumber : str
        A guess in string format
    dctPositions : dict
        A dictionary containing all 10 digits and their possible positions in the guessed number
    Returns
    -------
    intMatchingNum : int
        the number of digits that are certainly in the guessed number. Note: at the moment of execution, 
        not all digits from the guessed number are known
    """   
    intMatchingNum=0
    for i in [int(x) for x in strNumber]:
        if dctPositions[i][0]==True: intMatchingNum += 1
    return intMatchingNum

def NumberOfNonMatchingNumsInString(strNumber,dctPositions):
    """
    Finds out how many impossible digits are present in the current guess
    
    If a digits 0-th element in the dictionary is False, it is certainly not present in the guessed number 
    Parameters
    ----------
    strNumber : str
        A guess in string format
    dctPositions : dict
        A dictionary containing all 10 digits and their possible positions in the guessed number
    Returns
    -------
    intNonMatchingNum : int
        the number of digits that are certainly not present in the guessed number.
    """   
    intNonMatchingNum=0
    for i in [int(x) for x in strNumber]:
        if dctPositions[i][0]==False: intNonMatchingNum += 1
    return intNonMatchingNum

def CompareLast2Steps(intStep,lstGuesses,dctPositions,lstNumsFound,intNumsFound):
    """
    Compares the last 2 steps
    
    Calculates the sum of Bulls and Cows in the actual and the previous guess, but distracts the number of 
    certainly known digits in those guesses. Compares the obtained numbers - If the sums are not equal, we
    know that a digit is certainly in the guessed number
    
    Example: actual guess: 1234;Bulls: 0; Cows: 2    previous guess: 0123;Bulls: 0; Cows: 1 and none of the
        digits havent been found (none of the digits havent been recognized as possible digits in the guessed 
        number) Since the sum has changed from 1 to 2 - we know that 4 is in the guessed number, and 0 
        cant be in the guessed number (since 123 contains only one digit and 0123 contains 1 digit as well)
    Parameters
    ----------
    intStep : int
        An integer holding the number of actual step
    lstGuesses : list
        A list containing all guesses made together with the number of bulls and cows
    dctPositions : dict
        A dictionary containing all 10 digits and their possible positions in the guessed number
    lstNumsFound : list
        A list containing all digits, that are certainly in the guessed number
    intNumsFound : int
        How many digits have been recognized, that are certainly in the guessed number. 
        Note: its the same as the length of lstNumsFound 
        
    Returns
    -------
    intNumsFound: int
        How many digits have been recognized, that are certainly in the guessed number. 
        Note: its the same as the length of lstNumsFound 
    """
    intSumAct = sum(lstGuesses[intStep][1:]) - NumberOfMatchingNumsInString(lstGuesses[intStep][0],dctPositions)
    intSumPrev = sum(lstGuesses[intStep-1][1:]) - NumberOfMatchingNumsInString(lstGuesses[intStep-1][0],dctPositions)
    if intSumAct != intSumPrev:
            strMatch, guessA, guessB = None,None,None
            if intSumAct < intSumPrev:
                #lstNumbersFound.append(lstGuesses[intStep-1][0][0])
                #strMatch = lstGuesses[intStep-1][0].translate(None,"".join(lstNumsFound))[0]
                guessA = lstGuesses[intStep-1]
                guessB = lstGuesses[intStep]
            elif intSumAct > intSumPrev:
                #lstNumbersFound.append(lstGuesses[intStep][0][-1])
                #strMatch = lstGuesses[intStep][0].translate(None,"".join(lstNumsFound))[-1]
                guessA = lstGuesses[intStep]
                guessB = lstGuesses[intStep-1]
            #strMatch = guessA[0].translate(None,guessB[0]).translate(None,"".join(lstNumsFound))
            strMatch = guessA[0].translate(str.maketrans(dict.fromkeys(guessB[0]))).translate(str.maketrans(dict.fromkeys("".join(lstNumsFound))))
            if len(strMatch)==1:
                AddNewNumber(lstNumsFound,dctPositions,strMatch)
            if intNumsFound==0:
                CompareAndEliminate(strMatch, guessA, guessB, dctPositions, intNumsFound)
            intNumsFound+=1
    return intNumsFound

def GenerateNewNumber(strActGuess, lstNumbersFound,lstNumbersEliminated,dctPositions,lstGuesses):
        """
        Generates a new guess based on the actual guess
        
        A new guess is created as a combination of all digits, that are certainly in the guessed number
        (lstNumbersFound), than the unknown part of the number is shifted to the right. If the new guess is 
        already in the list of guesses a the unknown part is shifted further. This could lead to an infinite
        cycle, but in that case (intCycle>5) a totally new guess is created by combining numbers that are
        certainly in the guessed number, numbers that are certainly not present in the guessed number and 
        only one unknown digit (only if the sum of certainly known digits and eliminated digits is >=3)
    
        Parameters
        ----------
        strActGuess : str
            The actual guess in string format
        lstNumbersFound : list
            A list containing all digits, that are certainly in the guessed number
        lstNumbersEliminated : list
            A list containing numbers that cant be present in the guessed number
        dctPositions : dict
            A dictionary containing all 10 digits and their possible positions in the guessed number
        lstGuesses : list
            A list containing all guesses made together with the number of bulls and cows
            
        Returns
        -------
        strGuess: str
            The new guess
    
        """
        if len(lstNumbersFound) == 0:
            intNewDigit = int(strActGuess[3])+1 if int(strActGuess[3])<9 else 0
            return strActGuess[1:] + str(intNewDigit)
        else:
            strFixedPart = GenerateNewNumberFixedPart(lstNumbersFound, "X", dctPositions)
            strGuess = strActGuess
            intCycleCounter = 0
            while True:
                intCycleCounter += 1  
                strMovingPart = GenerateNewNumberMovingPart(strGuess, lstNumbersFound, dctPositions)
                strGuess = CombineFixedAndMovingPart(strFixedPart, strMovingPart, "X")
                if intCycleCounter>5:
                    strAllEliminated = "".join([str(x) for x in lstNumbersEliminated])
                    #strMissingNums = "0123456789".translate(None,"".join(lstNumbersFound + [str(x) for x in lstNumbersEliminated]))
                    strMissingNums = "0123456789".translate(str.maketrans(dict.fromkeys("".join(lstNumbersFound + [str(x) for x in lstNumbersEliminated]))))
                    lstMissingNums = [int(x) for x in strMissingNums]
                    if len(lstNumbersFound) + len(strAllEliminated)<4:
                        intLenToFill = 4-(len(lstNumbersFound) + len(strAllEliminated))
                        strMovingPart = strAllEliminated + "".join([str(x) for x in random.sample(lstMissingNums, intLenToFill)])
                        strGuess = CombineFixedAndMovingPart(strFixedPart, strMovingPart, "X")
                    else:
                        strGuess = ("".join(lstNumbersFound) + strAllEliminated)[:3] + "".join([str(x) for x in random.sample(lstMissingNums, 1)])         
                if strGuess not in [x[0] for x in lstGuesses] and ContainsUnknown(dctPositions,strGuess):
                    break
                else:
                    pass
            return strGuess
            
def GenerateNewNumberFixedPart(lstNumbersFound, charMissing, dctPositions):
    """
    Generates 4-digit string containing certainly known digits, the unknown positions are filled with charMissing
    
    The output string contains the certainly known digits only on the positions that are possible for
    those digits. The possible positions are in the 1-st element of the dictionary
    
    Example: 2 digits are in lstNumbersFound: 2,3. These are certainly in the guessed number.
        The possible positions for 2 are: 2nd and 3rd - [False,True,True,False]
        The possible positions for 3 are: 2nd and 3rd - [False,True,True,False]
        charMissing is X. The following outputs are then possible X23X, X32X. The method outputs the first one
        it finds
    Parameters
    ----------
    lstNumbersFound : list
        A list containing all digits, that are certainly in the guessed number
    charMissing : str
        The unknown digits will be filled with this character
    dctPositions : dict
        A dictionary containing all 10 digits and their possible positions in the guessed number
        
    Returns
    -------
    "".join(num) : str
        The possible fixed part
    """
    lstPermutInit = lstNumbersFound + [charMissing]*(4-len(lstNumbersFound))
    for num in itertools.permutations(lstPermutInit,4):
        boolInnerCond = True
        for i in range(len(lstNumbersFound)):
            if lstNumbersFound[i] in [num[x] for x in range(4) if dctPositions[int(lstNumbersFound[i])][1][x]]:
                boolInnerCond = boolInnerCond and True
            else:
                boolInnerCond = boolInnerCond and False
        if boolInnerCond:
            return "".join(num)
        
def GenerateNewNumberMovingPart(strActGuess, lstNumbersFound,dctPositions):
    """
    Shifts the unknown part of the guess
    
    Subtracts the certainly present digits from the actual guess (unknown part). Then increases the highest 
    digit in the unknown part (until the new digit is not the list of digits certainly present in the guessed
    number), the rest of the unknown part stays untouched. The length of the output should be (4 - length of certainly present digits)
    
    Parameters
    ----------
    strActGuess : str
        The actual guess in string format
    lstNumbersFound : list
        A list containing all digits, that are certainly in the guessed number    
    dctPositions : dict
        A dictionary containing all 10 digits and their possible positions in the guessed number
        
    Returns
    -------
    strNewMovingPart : str
        The shifted unknown part
    """
    intLenToChange = 4-len(lstNumbersFound)
    #strPartToHold = strActGuess.translate(None,"".join(lstNumbersFound))[-intLenToChange:]
    strPartToHold = strActGuess.translate(str.maketrans(dict.fromkeys("".join(lstNumbersFound))))[-intLenToChange:]
    strNewDigit = ""
    intNewDigit = int(strPartToHold[-1])+1 if int(strPartToHold[-1])<9 else 0
    while True:        
        if dctPositions[intNewDigit][0]==False or dctPositions[intNewDigit][0]==None:
            strNewDigit = str(intNewDigit)
            break
        intNewDigit = intNewDigit + 1 if intNewDigit<9 else 0
    strNewMovingPart = strPartToHold[-(intLenToChange-1):] + strNewDigit if intLenToChange!=1 else strNewDigit
    return strNewMovingPart

def CombineFixedAndMovingPart(strFixedPart, strMovingPart, charMissing):
    cntX = 0
    strNewGuess = ""
    for pos in range(len(strFixedPart)):
        if strFixedPart[pos]==charMissing:
            cntX += 1
            strNewGuess += strMovingPart[cntX-1]
        else:
            strNewGuess += strFixedPart[pos]
    return strNewGuess

def ContainsUnknown(dctPositions,strGuess):
    """
    Determines whether a guess contains unknown digits
    
    If all 4 digits are either in the list of digits that are certainly in the guessed number or in the list 
    of digits that arent present in the guessed number - the function returns False.
    
    Parameters
    ----------
    dctPositions : dict
        A dictionary containing all 10 digits and their possible positions in the guessed number
    strGuess : str
        The actual guess in string format
        
    Returns
    -------
    Whether or not the the guess contains unknown digits
    """
    intNumOfMatches = NumberOfMatchingNumsInString(strGuess, dctPositions)
    intNumOfNonMatches = NumberOfNonMatchingNumsInString(strGuess, dctPositions)
    if intNumOfMatches + intNumOfNonMatches == 4:
        return False
    else:
        return True

def AddNewNumber(lstNumbersFound,dctPositions,strActNumber):
    """
    Adds a digit to the list of certainly present digits
    
    Parameters
    ----------
    lstNumbersFound : list
        A list containing all digits, that are certainly in the guessed number  
    dctPositions : dict
        A dictionary containing all 10 digits and their possible positions in the guessed number
    strActNumber : str
        A string containing any number of digits. Doesn't need to be 4 digit long
        
    Returns
    -------
    None
    """
    if strActNumber not in lstNumbersFound:
        lstNumbersFound.append(strActNumber)
        dctPositions[int(strActNumber)][0] = True
        for i in range(len(dctPositions[int(strActNumber)][1])):
            if dctPositions[int(strActNumber)][1][i]==None:
                dctPositions[int(strActNumber)][1][i] = True

def CompareAndEliminate(strMatch, guessA, guessB, dctPositions, intNumberFound):
    """
    Compares 2 guesses and finds the digits which are only in one of them
    
    I.e. Union of 2 guesses minus the intersection of the guesses. If we get only one digit, that digit
    can be eliminated - cant be present in the guessed number. Note: this function is used only when the
    first certainly present digit is found
    
    Example: actual guess: 1234;Bulls: 0; Cows: 2    previous guess: 0123;Bulls: 0; Cows: 1 and none of the
        digits havent been found (none of the digits havent been recognized as possible digits in the guessed 
        number) Since the sum has changed from 1 to 2 - we know that 4 is in the guessed number, and 0 
        cant be in the guessed number (since 123 contains only one digit and 0123 contains 1 digit as well)
        This method eliminates 0
    
    Parameters
    ----------
    strMatch : str
        The digit found in guessA
    guessA : [str,int,int]
        a list containing 4-digit guess, its number of Bulls, its number of Cows
    guessB : [str,int,int]
        a list containing 4-digit guess, its number of Bulls, its number of Cows 
    dctPositions : dict
        A dictionary containing all 10 digits and their possible positions in the guessed number
    intNumberFound : int
        How many digits have been recognized, that are certainly in the guessed number. 
        Note: its the same as the length of lstNumsFound 
        
    Returns
    -------
    None
    """
    # diffChar = list(set(guessB[0]) - set(guessA[0].translate(None,strMatch)))
    diffChar = list(set(guessB[0]) - set(guessA[0].translate(str.maketrans(dict.fromkeys(strMatch)))))
    if len(diffChar)!=1: return
    intAWoCurMatch = sum(guessA[1:]) - 1
    intBAllMatch = sum(guessB[1:])
    if intAWoCurMatch == intBAllMatch:
        EliminateNumber(dctPositions,diffChar[0])

def CompareNumberOfMatchAndSum(actGuess,lstNumbersFound,dctPositions,lstNumbersEliminated):
    """
    Compares the sum of bulls and cows with the number of certainly present digits in a guess
    returns True if the sum equals to the number of certainly present digits. Additionally it eliminates
    impossible digits (if there is any)
    
    Parameters
    ----------
    actGuess : str
        The actual guess in string format
    lstNumbersFound : list
        A list containing all digits, that are certainly in the guessed number
    dctPositions : dict
        A dictionary containing all 10 digits and their possible positions in the guessed number
    lstNumbersEliminated : list
        A list containing numbers that cant be present in the guessed number
        
    Returns
    -------
    returns True if the sum equals to the number of certainly present digits, else it returns false
    """    
    intActMatch = NumberOfMatchingNumsInString(actGuess[0], dctPositions)
    intActSum = sum(actGuess[1:])
    if intActMatch==intActSum:
        #strNumsToEliminate = actGuess[0].translate(None,"".join(lstNumbersFound))
        strNumsToEliminate = actGuess[0].translate(str.maketrans(dict.fromkeys("".join(lstNumbersFound))))
        EliminateNumber(dctPositions, strNumsToEliminate)
        UpdateEliminationState(lstNumbersEliminated, dctPositions)
        return True
    else:
        return False
    
def UpdateExactPosition(strActGuess,lstNumbersFound,dctPositions):
    """
    Updates the exact position for a digit
    
    We can determine the exact position for a digit, when the 1st element in the dictionary of possible
    positions contains only one True, and its 0th element is True as well (i.e. its in the list of certainly
    present digits). If the exact position for a certainly present digit has been found, than none of the 
    other 9 digits can have that position occupied. This function updates that position for all other digits
    
    Parameters
    ----------
    strActGuess : str
        The actual guess in string format
    lstNumbersFound : list
        A list containing all digits, that are certainly in the guessed number
    dctPositions : dict
        A dictionary containing all 10 digits and their possible positions in the guessed number
            
    Returns
    -------
    None
    """
    for strDigit in lstNumbersFound:
        if strDigit in strActGuess:
            if dctPositions[int(strDigit)][1].count(True)!=1:
                position = strActGuess.find(strDigit)
                dctPositions[int(strDigit)][1] = [False]*4
                dctPositions[int(strDigit)][1][position] = True
                for i in range(10):
                    if i!=int(strDigit):
                        dctPositions[i][1][position] = False

def CheckAllPreviousSteps(lstGuesses,lstNumbersFound,lstNumbersEliminated,dctPositions):
    """
    Checks all the previous steps, in order to find certainly present digits or eliminate impossible digits
    
    This method is a complex one, and uses the newest information obtained from the current guess to deduct
    information from all previous steps
    
    Parameters
    ----------
    lstGuesses : list
        A list containing all guesses made together with the number of bulls and cows
    lstNumbersFound : list
        A list containing all digits, that are certainly in the guessed number
    lstNumbersEliminated : list
        A list containing numbers that cant be present in the guessed number
    dctPositions : dict
        A dictionary containing all 10 digits and their possible positions in the guessed number
            
    Returns
    -------
    None
    """
    # Looks for guesses where number of cows is zero - i.e. the exact (final) position of a digit can be determined
    CheckForExactPositions(lstGuesses,lstNumbersFound,dctPositions) 
    # List of digits that are on their exact position
    lstDigitsOnPosition = FindDigitsOnPosition(lstNumbersFound,dctPositions)
    # Eliminating the position for digits other than digits that are on position
    UpdateExactPositionsForDigitsOnPosition(lstDigitsOnPosition,dctPositions)
    # Checks every guess and compares sum of bulls and cows with number of certainly present digits in the guess
    CheckForEliminationAndMatch(lstGuesses,lstNumbersFound,lstNumbersEliminated,dctPositions)
    # looks for every guess where a certainly present digit is on its exact position, than its possible to eliminate 
    # possible positions for the other certainly present digits
    CheckForNonMatchPositions(lstGuesses,lstDigitsOnPosition,dctPositions)

def CheckForExactPositions(lstGuesses,lstNumbersFound,dctPositions):
    """
    Looks for guesses where number of bulls is non-zero and number of cows is zero
    
    If these type of guesses contain digits from the list of certainly present digits, than the exact position
    of those digits is their position in those guesses (non-zero bulls, zero cows)
    
    Parameters
    ----------
    lstGuesses : list
        A list containing all guesses made together with the number of bulls and cows
    lstNumbersFound : list
        A list containing all digits, that are certainly in the guessed number
    dctPositions : dict
        A dictionary containing all 10 digits and their possible positions in the guessed number
            
    Returns
    -------
    None
    """
    for guess in lstGuesses:
        if False in [True if dctPositions[int(x)][1].count(True)==1 else False for x in lstNumbersFound]:
            if guess[1]!=0 and guess[2]==0:
                UpdateExactPosition(guess[0], lstNumbersFound, dctPositions)

def FindDigitsOnPosition(lstNumbersFound,dctPositions):
    """
    Creates a list of digits, for those their exact position has been found
    
    The exact position is found, when the digit is in the list of certainly present numbers and the 1st element
    of the possible positions contains only one True
    
    Parameters
    ----------
    lstNumbersFound : list
        A list containing all digits, that are certainly in the guessed number
    dctPositions : dict
        A dictionary containing all 10 digits and their possible positions in the guessed number
            
    Returns
    -------
    lstResult : list
        list of digits, for those their exact position has been found
    """
    lstResult = list()
    for i in [int(x) for x in lstNumbersFound]:
        if dctPositions[i][1].count(True)==1:
            lstResult.append(i)
    return lstResult

def UpdateExactPositionsForDigitsOnPosition(lstDigitsOnPosition,dctPositions):
    """
    Eliminates positions occupied by digits for those their exact position have been found
    
    If the exact position for a certainly present digit has been found, than none of the other 9 digits 
    can have that position occupied. This function updates that position for all other digits.
    
    Parameters
    ----------
    lstDigitsOnPosition : list
        list of digits, for those their exact position has been found
    dctPositions : dict
        A dictionary containing all 10 digits and their possible positions in the guessed number
            
    Returns
    -------
    None
    """
    for digit in lstDigitsOnPosition:
        position = dctPositions[digit][1].index(True)
        for i in range(10):
            if i!=digit:
                dctPositions[i][1][position] = False

def CheckForEliminationAndMatch(lstGuesses,lstNumbersFound,lstNumbersEliminated,dctPositions):
    """
    Checks every guess and compares sum of bulls and cows with number of certainly present digits in the guess
    
    If the number of certainly present digits is the same as the sum of bulls and cows for the particular 
    guess, than all the other digits cant be present in the guessed number (they need to be eliminated)
    If the difference between the sum of bulls and cows and the number of certainly present digits is 1, then
    that particular digit needs to be added to the list of certainly present digits
    
    Example: guess is 5287, Bulls:1 , Cows: 1 . Certainly present numbers: 4,2,8 - Then 5 and 7 cant be
        present in the guessed number
            guess is 8934, Bulls:2 , Cows: 1 . Certainly present numbers: 4,3 . Numbers, that cant be
        present in the guessed number: 8,5 - Then 9 must be present in the guessed number
    
    Parameters
    ----------
    lstGuesses : list
        A list containing all guesses made together with the number of bulls and cows
    lstNumbersFound : list
        A list containing all digits, that are certainly in the guessed number
    lstNumbersEliminated : list
        A list containing numbers that cant be present in the guessed number
    dctPositions : dict
        A dictionary containing all 10 digits and their possible positions in the guessed number
            
    Returns
    -------
    None
    """    
    if not lstNumbersFound:
        return
    else:
        for guess in lstGuesses:
            lstDigitsPresent = [strDigit for strDigit in lstNumbersFound if strDigit in guess[0]]
            if not lstDigitsPresent:
                continue
            #strUnknownDigits = guess[0].translate(None,"".join(lstNumbersFound+[str(x) for x in lstNumbersEliminated]))
            this_text = "".join(lstNumbersFound+[str(x) for x in lstNumbersEliminated])
            trans_table = str.maketrans(dict.fromkeys(this_text))
            strUnknownDigits = guess[0].translate(trans_table)
            if strUnknownDigits=="":
                continue
            if len(lstDigitsPresent) - sum(guess[1:]) == 0:
                #EliminateNumber(dctPositions, guess[0].translate(None,"".join(lstDigitsPresent)))
                EliminateNumber(dctPositions, guess[0].translate(str.maketrans(dict.fromkeys("".join(lstDigitsPresent)))))
                UpdateEliminationState(lstNumbersEliminated, dctPositions)
            elif len(strUnknownDigits) == 1:
                AddNewNumber(lstNumbersFound, dctPositions, strUnknownDigits)
                
def CheckForNonMatchPositions(lstGuesses,lstDigitsOnPosition,dctPositions):
    """
    looks for every guess where a certainly present digit is on its exact position
    
    1. a guess should have non-zero bulls and non-zero cows
    2. checks how many of the digits are on their final position
    3. if we know the final position for all bulls in the guess, 
        than all the other digits from the guess can be eliminated from their position
        in the guess 
    
    Parameters
    ----------
    lstGuesses : list
        A list containing all guesses made together with the number of bulls and cows
    lstDigitsOnPosition : list
        list of digits, for those their exact position has been found
    dctPositions : dict
        A dictionary containing all 10 digits and their possible positions in the guessed number
            
    Returns
    -------
    None
    """  
    if not lstDigitsOnPosition:
        return
    for guess in lstGuesses:
        #print guess, lstDigitsOnPosition
        if guess[1] != 0 and guess[2] != 0:
            intNumExactMatches = 0
            lstExactMatches = list()
            for digit in lstDigitsOnPosition:
                digitPosition = dctPositions[digit][1].index(True)
                if guess[0][digitPosition]==str(digit):
                    intNumExactMatches += 1
                    lstExactMatches.append(str(digit))
            if guess[1]-intNumExactMatches == 0:
                #EliminatePartialPositions(dctPositions, guess[0].translate(None,"".join(lstExactMatches)), guess[0])
                EliminatePartialPositions(dctPositions, guess[0].translate(str.maketrans(dict.fromkeys("".join(lstExactMatches)))), guess[0])
    

def EliminatePartialPositions(dctPositions, digitsToChange, actGuess):
    """
    Eliminates the positions for digits in digitsToChange based on their position in actGuess
    
    Parameters
    ----------
    dctPositions : dict
        A dictionary containing all 10 digits and their possible positions in the guessed number
    digitsToChange : str
        a string containing digits, those position should be eliminated
    actGuess : str
        The actual guess in string format
            
    Returns
    -------
    None
    """     
    for digit in digitsToChange:
        position = actGuess.find(digit)
        dctPositions[int(digit)][1][position] = False
  
def CreateInitialPermutations(lstNumbersFound,dctPositions):
    """
    Creates list of permutations from all certainly present digits, based on their possible positions
    
    Parameters
    ----------
    lstNumbersFound : list
        A list containing all digits, that are certainly in the guessed number
    dctPositions : dict
        A dictionary containing all 10 digits and their possible positions in the guessed number
            
    Returns
    -------
    lstPossiblePermutations : list
        List of all possible permutations created from the certainly present digits
    """ 
    lstPossiblePermutations = list()
    for num in itertools.permutations(lstNumbersFound,4):
        boolInnerCond = True
        for i in range(len(lstNumbersFound)):
            if lstNumbersFound[i] in [num[x] for x in range(4) if dctPositions[int(lstNumbersFound[i])][1][x]]:
                boolInnerCond = boolInnerCond and True
            else:
                boolInnerCond = boolInnerCond and False
        if boolInnerCond:
            lstPossiblePermutations.append("".join(num))
    return lstPossiblePermutations

def CreateAllPermutations(lstNumbersFound):
    """
    Creates list of permutations from all certainly present digits
    
    Parameters
    ----------
    lstNumbersFound : list
        A list containing all digits, that are certainly in the guessed number
    dctPositions : dict
        A dictionary containing all 10 digits and their possible positions in the guessed number
            
    Returns
    -------
    lstPossiblePermutations : list
        List of all possible permutations created from the certainly present digits
    """ 
    lstPossiblePermutations = list()
    for num in itertools.permutations(lstNumbersFound,4):
        lstPossiblePermutations.append("".join(num))
    return lstPossiblePermutations
              
def GuessPermutation(lstPossiblePermutations,lstGuesses):
    """
    Eliminates all impossible permutations
    
    Loops through all permutations and checks the number of Bulls and Cows of guesses in the permutation.
    If the number of bulls and cows doesn't equal to the number of original bulls and cows (coming from the 
    guessed number), the permutation can't be a solution and is eliminated from the list of permutations.
    
    Parameters
    ----------
    lstPossiblePermutations : list
        List of possible permutations
    lstGuesses : list
        A list containing all guesses made together with the number of bulls and cows
            
    Returns
    -------
    lstTempPermutations : list
        list of the reduced permutations
    """
    lstTempPermutations = lstPossiblePermutations[:]
    boolJumpOver = False
    for permutation in lstPossiblePermutations:
        #print permutation, boolJumpOver                
        for guess in lstGuesses:
            if not boolJumpOver:
                actBull,actCow = FindMatches(permutation,guess[0])
                if actBull != guess[1] or actCow!=guess[2]:
                    lstTempPermutations.remove(permutation)
                    boolJumpOver=True
            else:
                break
        boolJumpOver = False
    return lstTempPermutations        

#===============================================================================
# Computer guessing algorithm nr.1
#===============================================================================
def ComputerGuessAlgorithm1(strNumToGuess,strInitialGuess):
    """
    ALgorithm nr. 1
    
    The steps are the following:
    1. Starts with initialguess
    2. Shifts the guess to the right, if the sum of Bulls and cows changing between guesses, we have a new digit in the guessed number
    3. If both bulls and cows are 0, none of the digits will be present in the guessed number
    4. if only the bull is zero, then none of the digits will the actual position in the guessed number (eg 1234 return 0,2 - Then 1 cant be in the 0-th position)
    5. New guesses always contain maximum number of digits found (digits that certainly will be in the guessed number)
    6. If 1 or more digits have been found, it loops through all previous steps in order to find certainly 
    present digits or eliminate impossible digits
    7. The program loops until it finds all 4 digits
    8. Then it creates Permutations from those 4 digits and filters out guesses with impossible positions
    9. Loops until a guess returns 4 bulls and 0 cows
    
    Parameters
    ----------
    strNumToguess : str
        the number we are looking for in string format
    strInitialGuess : str
        The first guess asked by the software
            
    Returns
    -------
    lstGuesses : list
        A list containing all guesses made together with the number of bulls and cows
    """
    dctPossiblePositions = dict((number, [None,[None for x in range(4)]]) for number in range(10))
    intNumberFound = 0
    lstNumbersFound = list()
    lstNumbersEliminated = list()
    lstGuesses = list()
    intStep = -1
    intNumberOfSteps = 0
    
    strActGuess=strInitialGuess
      
    while intNumberFound!=4:
        intStep+=1
        tplActMatch = FindMatches(strNumToGuess,strActGuess)
        lstGuesses.append([strActGuess,tplActMatch[0],tplActMatch[1]])
        if tplActMatch[0] == 0:
            EliminatePossiblePositions(dctPossiblePositions, strActGuess)
            if tplActMatch == (0,0):
                EliminateNumber(dctPossiblePositions,strActGuess)
            UpdateEliminationState(lstNumbersEliminated, dctPossiblePositions)
        elif tplActMatch[0]!=0 and tplActMatch[1]==0:
            UpdateExactPosition(strActGuess,lstNumbersFound,dctPossiblePositions)
        
        if sum(tplActMatch)==4:
            for strDigit in strActGuess:
                AddNewNumber(lstNumbersFound, dctPossiblePositions, strDigit)
            intNumberFound = len(lstNumbersFound)
            #EliminateNumber(dctPossiblePositions, "0123456789".translate(None,strActGuess))
            EliminateNumber(dctPossiblePositions, "0123456789".translate(str.maketrans(dict.fromkeys(strActGuess))))
            UpdateEliminationState(lstNumbersEliminated, dctPossiblePositions)
            break
        if intStep>0:
            if not CompareNumberOfMatchAndSum(lstGuesses[intStep],lstNumbersFound,dctPossiblePositions,lstNumbersEliminated):
                intNumberFound = CompareLast2Steps(intStep,lstGuesses,dctPossiblePositions,lstNumbersFound,intNumberFound)
            if intNumberFound>0:
                CheckAllPreviousSteps(lstGuesses,lstNumbersFound,lstNumbersEliminated,dctPossiblePositions)
                intNumberFound = len(lstNumbersFound)   
        
        UpdateEliminationState(lstNumbersEliminated, dctPossiblePositions)                  
        if intNumberFound!=4:
            strActGuess = GenerateNewNumber(strActGuess, lstNumbersFound,lstNumbersEliminated,dctPossiblePositions,lstGuesses)
    
    if lstGuesses[-1][1]==4:
        pass
    else:
        lstPossiblePermutations = CreateInitialPermutations(lstNumbersFound, dctPossiblePositions)
        lstPossiblePermutations = GuessPermutation(lstPossiblePermutations,lstGuesses)
        actBull=0
        while True:
            actBull, actCow = FindMatches(strNumToGuess,lstPossiblePermutations[0])
            
            lstGuesses.append([lstPossiblePermutations[0],actBull,actCow])
            lstPossiblePermutations = GuessPermutation(lstPossiblePermutations,lstGuesses)
            if actBull == 4:
                break
    
            
    return lstGuesses


#===============================================================================
# Computer guessing algorithm nr.2
#===============================================================================
def ComputerGuessAlgorithm2(strNumToGuess):
    """
    ALgorithm nr. 2
    
    The steps are the following:
    1. It creates all the possible permutations (for 4-digit numbers its 5040)
    2. makes guesses and deducts the impossible permutations (if a permutation returns a wrong number of of bulls and cows for the same guess,
        then it should be removed)
    3. Picks the first permutation and makes it as a guess
    4. Loops until it returns 4 bulls and 0 cows
    
    Parameters
    ----------
    strNumToguess : str
        the number we are looking for in string format
            
    Returns
    -------
    lstGuesses : list
        A list containing all guesses made together with the number of bulls and cows
    """
    lstGuesses = list()
    lstDigits = [str(x) for x in range(10)]
    lstPossiblePermutations = CreateAllPermutations(lstDigits)
    lstStaticGuesses = ["0123","4567"]
    boolGoStatic = True
    
    intStepNr = 0
    
    while True:
        strActGuess = ""
        if boolGoStatic:
            strActGuess = lstStaticGuesses[intStepNr]
        else:
            #strActGuess = random.choice(lstPossiblePermutations)
            strActGuess = lstPossiblePermutations[0]
        
        actBull,actCow = FindMatches(strNumToGuess,strActGuess)  
        lstGuesses.append([strActGuess,actBull,actCow])
        lstPossiblePermutations = GuessPermutation(lstPossiblePermutations,lstGuesses)
        
        if (actBull,actCow) == (4,0):
            return lstGuesses
        
        intStepNr += 1
        if intStepNr>1:
            boolGoStatic = False
        elif intStepNr == 1:
            #print intStepNr
            if actBull + actCow > 2:
                #print "here"
                boolGoStatic = False
            else:
                boolGoStatic = True

#===============================================================================
# User guess
#===============================================================================

def UserGuess(strUserNum):
    """
    User guessing
    
    This method handles the user guessing - The user is needs to make guesses until he finds the right solution
    
    Parameters
    ----------
    strNumToguess : str
        the number we are looking for in string format
            
    Returns
    -------
    lstGuesses : list
        A list containing all guesses made together with the number of bulls and cows
    """
    intGuessCounter = 0
    intCorrectGuessCounter  = 0
    #print "If You want to exit, type exit instead of a guess"
    while True:
        strUserNum = input("Enter your guess and press enter: ")
        intGuessCounter += 1
        if strUserNum.lower() == "exit":
            return -1,-1
        if not strUserNum.isdigit() or len(strUserNum)!=4:
            #print "Wrong input"
            continue
        else:
            if len(set(strUserNum))!=4: 
                #print "The digits aren't unique"
                continue
            else:
                tplMatch = FindMatches(strNumToGuess,strUserNum)
                if tplMatch[0] == 4:
                    #print "Guess nr. {0}: {1}, Bulls: {2}, Cows: {3}".format(intGuessCounter,strUserNum,tplMatch[0],tplMatch[1])
                    intCorrectGuessCounter+=1
                    return intGuessCounter, intCorrectGuessCounter
                else:
                    intCorrectGuessCounter += 1
                    #print "Guess nr. {0}: {1}, Bulls: {2}, Cows: {3}".format(intGuessCounter,strUserNum,tplMatch[0],tplMatch[1])
                

#===============================================================================
# Main loop
#===============================================================================
# The Main loop generates a random number, then the two algorithms finds that number and at the end the user should guess the number
# After finding the number, The program ranks the user and the computer algorithms based on the number of guesses needed to find the right solution

if __name__ == '__main__':
    RoundNr = 1
    StrHorizontal = "#==============================================================================="
    
    dctResults = dict()
    strNumToGuess =  "".join([str(x) for x in random.sample(range(10), 4)])
    lstComputerSolution = [ComputerGuessAlgorithm1(strNumToGuess, "0123"),ComputerGuessAlgorithm2(strNumToGuess)]
    dctResults["Player1"] = len(lstComputerSolution[0])
    dctResults["Player2"] = len(lstComputerSolution[1])
    
    print ("{0}\nI've generated a random 4-digit number.\nPlayer {1} (Computer) has found it in {2} steps.\nPlayer {3} (Computer) has found it in {4} steps.\nCan You find it in less guesses?\n{5}\n".format(
        StrHorizontal,1,len(lstComputerSolution[0]),2,len(lstComputerSolution[1]),StrHorizontal))