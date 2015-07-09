
import random
import GeneralSatTools as GST
import time
"""
BestClause is a class used to tracker the time elapsed and the highest number of clauses satisfied
"""
class BestClause():
    def __init__(self):
        self.c = 0
        self.S_Time = time.time()
#compares a newC value to the current highest value, if newC is larger replace self.c with newC
    def compare(self, newC):
        if newC > self.c:
            self.c=newC

    def getC(self):#get best number of clauses satisfied
        return self.c

    def getTimeElapsed(self):#find the time that has elapsed since creation of the BestClause
        return time.time() - self.S_Time

"""
cnf is the 2d array representing the problem to be solved
model is the currently assignmed symbols and their corresponding values
solvedClauses is an array of the index of the currently true clauses given the current model

This loops through all clauses in the cnf, if it is already in the solvedClause array, skip it
for every symbol in the model, if that symbol would make the clause true, add the clause to the solvedClauses array
"""

def SolvedClauses(cnf, model, solvedClause):
    if model:
        for j in range(len(cnf)):
            if j not in solvedClause:
                for i in range(len(model[0])):
                    if cnf[j][model[0][i]]*model[1][i] > 0:
                        solvedClause.append(j)

"""
symbols is the array of symbols that are not yet assigned in the model
sym is a symbol in the array to be removed
checks if the item is in symbols, if it is it is poped out
"""
def RemoveSymbol(symbols, sym):
    for i in range(len(symbols)):
        if symbols[i] == sym:
            symbols.pop(i)
            return True
    return False
"""
Debugging item used to see important values at different points in the function
"""
def printALL(model,symbols,Tracker):
    print("Model, Symbols, Tracker")
    print(model)
    print(symbols)
    print(Tracker.getC())
    print("")
"""
adds a symbol with a corresponding value (-1 or 1) to the given model array

first checks to see if the model has been initialized, if not initialize, otherwise append items into the correct part of the array
"""
def addToModel(model, sym, val):
    if model:
        #print("BEFORE AFTER APPEND")
        #print(model)
        model[0].append(sym)
        model[1].append(val)
        #print(model)
    else:
        hold1 = []
        hold2 = []
        hold1.append(sym)
        #print("HOLD HOLD MODEL")
        #print(hold1)
        model.append(hold1)
        hold2.append(val)
        #print(hold2)
        model.append(hold2)
        #print(model)

"""
Given the number of varaible and the model it will create an assignment. all variables not listed in the model will be assumed false
"""
def createAssignments(nbvar, model):
    boolvec = []
    for i in range(nbvar):#if there is nothing in the model everything is assumed false
        boolvec.append(-1)
    try: #try is incase model has not yet been created
        for i in range(len(model[0])):#for every index that there is a true false value specified
            boolvec[model[0][i]] = model[1][i]
    except IndexError:#the model has not yet been created
        pass

    return boolvec #return the assignment


"""
Given the 2d cnf array, the model array and the Tracker it tests to see if a solution has been found. and saves the C
value if it is higher than the previous highest
"""
def Check(cnf, model, Tracker):
    CurrentUnit = createAssignments(len(cnf[0]), model)
    newC = GST.testAssignments(cnf, CurrentUnit)
    Tracker.compare(newC)
    return newC

"""
given the cnf, available symbols array, the array representing the model, and the list of satisfied clauses to be ignored.
First the satisfied clauses list is updated, then it loops through every clause in the cnf that is not in the satisfied
clauses array (named ignoreList). It loops through every available symbols and counts how many there are. If there is only one then it
must be set to make that clause true and then recursively call UnitPropagate to update the clause search and the solved clauses array
"""
def UnitPropagate(cnf, symbols, model, ignoreList):
    SolvedClauses(cnf, model, ignoreList) #update ignoreList (list of solved clauses)
    for i in range(len(cnf)): #for every clause in the cnf
        if i not in ignoreList: #if not already solved
            count = 0 #reset count
            position = -1 # used to save position
            for unit in symbols: #for every symbol that has not already been determined
                if cnf[i][unit] != 0: #if the cnf has a variable in that position (it only checks clauses that are not satisfied and only symbols that are not already determined)
                    count += 1 #number of symbols in the clause that are not already determined
                    position = unit # saves position incase only one is found
            if count == 1:#Unit propagate success!!!
                RemoveSymbol(symbols, position)
                if cnf[i][position] > 0:
                    addToModel(model, position, 1)
                else:
                    addToModel(model, position, -1)
                UnitPropagate(cnf, symbols, model, ignoreList)#restart with updated ingoreList and model
                break

"""
Given: cnf, available symbols array, the array representing the model, and the list of satisfied clauses to be ignored.
Begins by updating the satisfied clauses array and then loops through every available symbol. It then checks to
find the last looked location, which is the first clause not inside of the satisfied clauses array. Then it loops
through every clause and checks the next clause against the previous to see if they are the same. If one is found to
not be the same it stops and continues with the next symbol. It the loop completes, then the symbol was the same in
all unsatisfied clauses and can then be set to either true or false to make as many clauses true as possible. When
one is found FindPureSymbol must be called recursively to restart the search with an updated satisfied clauses array
and a reduced number of available symbols
"""
def FindPureSymbol(cnf, symbols, model, ignoreList):
    ignoreList = SolvedClauses(cnf, model, ignoreList)#updates ignoreList
    for sym in range(len(symbols)):#for every symbol not already assigned a value
        lastLook = -1#find the first clause which this symbol is used
        if not ignoreList:
            lastLook = 0
        elif 0 not in ignoreList:
            lastLook = 0

        same = True
        for i in range(1, len(cnf)):
            if not ignoreList:
                if lastLook == -1:
                    lastLook = i
                elif cnf[i][symbols[sym]] != cnf [lastLook][symbols[sym]]:#if the next usage of this symbol isnt the same as the last then it is not purely true or false
                    same = False
                    break
                else:
                    lastLook = i
            elif i not in ignoreList:#repeated twice in case ignorelist has yet to be created, which would cause an indexError here
                if lastLook == -1:
                    lastLook = i
                elif cnf[i][symbols[sym]] != cnf [lastLook][symbols[sym]]:
                    same = False
                    break
                else:
                    lastLook = i

        if same:#found a pure symbol!!
            if cnf[0][symbols[sym]] < 0:
                addToModel(model, symbols[sym], -1)
            else:
                addToModel(model, symbols[sym], 1)
            RemoveSymbol(symbols, symbols[sym])
            FindPureSymbol(cnf, symbols, model, ignoreList)#restart with updated ignorelist and model
            break

"""
Given: the 2d cnf array, symbols array, an empty model array, an empty satisfied clauses array and the Tracker.
First it creates a deep copy of all given arrays so that they may be manipulated without effecting the previous
calls to the function. Next Unit Propagate is called to update the model finding all single instance variables.
After that loop finishes it returns to DPLL where it calls FindPureSymbol which updates the model to find all instances
where a variable only appears in one form. Once this returns to DPLL Check is called which returns the number of
satisfied clauses. If the number of satisfied clauses returned matches the number of clauses  in the cnf we stop
because a solution has been found. Otherwise we check to see if there are any symbols remaining, ifthere are none
we back track. Last we check for timeout, which has been set to 70 seconds. If none of those conditionsare met it
makes a random choice for the next symbol and sets it to true. It the calls DPLL to see if that made aviable solution,
if not it guesses false and returns that result.
"""
def DPLL(cnf, symbols, model, ignoreList, Tracker):
    #Create all copies
    cnf1 = GST.DeepCopy(cnf)
    symbols1 = GST.DeepCopy(symbols)
    model1 = GST.DeepCopy(model)
    ignoreList1 = GST.DeepCopy(ignoreList)
    UnitPropagate(cnf1, symbols1, model1, ignoreList1)
    if symbols1: #Skip if no symbols are left
        FindPureSymbol(cnf1, symbols1, model1, ignoreList1)

    c = Check(cnf, model1, Tracker)#Check for solution
    if c == len(cnf):
        return True
    elif len(symbols1) == 0:
        return False
    elif Tracker.getTimeElapsed() > 70:
        return False


    #Take a guess
    symIndex = random.randint(0,len(symbols1)-1)
    addToModel(model1, symbols1[symIndex], 1)
    RemoveSymbol(symbols1,symbols1[symIndex])
    if DPLL(cnf1, symbols1, model1, ignoreList1, Tracker):
        return True
    #First guess wrong
    model1[1][len(model1[1])-1] = -1
    Guess = DPLL(cnf1, symbols1, model1, ignoreList1, Tracker)
    #print("FINAL GUESS", Guess)
    return Guess
"""
Function that creates the symbols array and send in empty arrays for the model and ignoreList
"""
def DpllSatisfiable(cnf, Tracker):#returns number of satisfiable clauses
    symbols = []
    symbols.extend(range(0,len(cnf[0])))#all of the available symbols to add to the model
    return DPLL(cnf,symbols,[], [], Tracker)
"""
Function for the user to call with the cnf to be solved
Creates the Tracker to be used for the timeout function
"""
def Solve(cnf):
    random.seed()
    Tracker = BestClause() #Used to find the highest number of clauses satisfied

    if DpllSatisfiable(cnf, Tracker): #True when a solution is reached
        print("satisfiable")
    return Tracker.getC()#returns the best solution found in all iterations
