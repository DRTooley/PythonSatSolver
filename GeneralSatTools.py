import random
import copy
random.seed()

"""
testAssignments(cnf, myAssign)

cnf is the 2d array that contains the cnf formula that you want to compare the assignment myAssign against

returns the number of clauses that is satisfied by the given assignment in the given cnf
"""
def testAssignments(cnf, myAssign):
    goodClause = 0
    for clause in cnf:
        for i in range(len(myAssign)):
            if myAssign[i]*clause[i]>0:
                goodClause+=1
                break
    return goodClause
"""
GenerateRandomAssignment(nbvar)

nbvar is the number of variables that are in the cnf, which the assignment is being created for

returns an array of length nbvar that has the value -1(false) or 1(true)
"""
def GenerateRandomAssignment(nbvar):
    boolvec = []
    for i in range(nbvar):
        boolvec.append(random.randrange(-1,2,2))
    return boolvec

"""
DeepCopy(CopyFrom)

CopyFrom is an array that a deep copy will be made from

returns the new array that is the same as the CopyFrom array

**Note**
This is an unnecessary function where I originally implemented it myself, found that the way i had attempted to make a deep copy
was incorrect and also found that there is a much simpler way. I kept it in to eliminate the work or finding all deep
copies made in the three algorithms and replacing with the built in function.
"""
def DeepCopy(CopyFrom):
    return copy.deepcopy(CopyFrom)