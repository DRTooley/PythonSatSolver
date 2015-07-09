import random
import GeneralSatTools as GST

"""
createAssignments(nbvar, iterations)

nbvar is the number of variables in the cnf
iterations in the number of randomly assigned solutions to create

returns all randomly created assignments as an array
"""
def createAssignments(nbvar, iterations):
    assignments = []
    for assignNum in range(iterations):
        assignments.append(GST.GenerateRandomAssignment(nbvar))
    return assignments

"""
testAssignments(cnf, myAssign)

cnf is the 2d array containing the cnf that is to be solved
myAssign are all of the assignments currently alive in the genetic algorithm

returns an array of ints that is their level of fitness (number of clauses satisfied)
"""
def testAssignments(cnf, myAssign):
    fitness = []
    for assignment in myAssign:
        fitness.append(GST.testAssignments(cnf,assignment))
    return fitness

"""
Reproduce(assignment, R)

assignment is all possible assignments to solve the cnf
R is an int that is the number of times the

this returns the extended list of assignments with the reproduced items appended onto it
"""
def Reproduce(assignment, R):
    for i in range(R):
        newAssign = []
        mate1 = random.randint(0,len(assignment)-1)
        mate2 = random.randint(0,len(assignment)-1)
        while(mate1 == mate2 and len(assignment) > 1):  #No Asexual reproduction unless it is the last one alive
            mate1 = random.randint(0,len(assignment)-1)
            mate2 = random.randint(0,len(assignment)-1)
        for j in range(len(assignment[0])):
            trait = random.randint(0,1)
            if(trait == 0):
                newAssign.append(assignment[mate1][j])
            else:
                newAssign.append(assignment[mate2][j])
        assignment.append(newAssign)  #yes, newly created assignments have a chance to reproduce immediatley
    return assignment

"""
Mutate(assignment, m)

assignment is all possible assignments to solve the cnf
m is an int between 0 and 100 where it is the percent of 'genes' (assigned values in the selected assignment(s)) that will be changed

this returns the list of assignments with a random percent of the assignments changed by m%
"""
def Mutate(assignment, m):
    MutateNum = int(len(assignment)*m/100)  #number of assignments to mutate
    assignSelector = []
    for i in range(MutateNum):
        candidate = random.randint(0,len(assignment)-1)
        if candidate not in assignSelector:
            assignSelector.append(candidate) # creates list of index numbers in assignment to mutate
        else:
            i -= 1

    GenesToMutate = [int(len(assignment[0])/10), int(len(assignment[0])/2)]  #Mutate 10-50% on the genes

    for assignNumber in assignSelector:
        HowManyGenes = random.randint(GenesToMutate[0],GenesToMutate[1]) #Selects exact number of genes to mutate
        for j in range(HowManyGenes):
            selector = random.randint(0,len(assignment[0])-1)
            assignment[assignNumber][selector] = random.randrange(-1,2,2) #random mutation

    return assignment
"""
NaturalSelection(assignment, fitness, nbclauses)

assignment is all possible assignments to solve the cnf
fitness is the fitness array returned by test assignments, it is the given fitness correlating to the assignment with the same index
nbclauses is the number of clauses in the cnf

this returns the shortened list of assignments where some were killed, weighted by not killing the most 'fit'
"""
def NaturalSelection(assignment, fitness, nbclauses):
    killNum = random.randint(int(len(assignment)/10), int(len(assignment)/3))  #number to kill
    unfit = []
    for val in fitness:
        unfit.append(nbclauses-val)  #counts number of clauses that were not satisfied
    for i in range(killNum):
        totalUnfit = sum(unfit)
        killed = random.randint(0,totalUnfit)
        for j in range(len(unfit)):
            killed -= unfit[j]
            if killed < 0:
                unfit.pop(j)
                assignment.pop(j)
                break
    return assignment
"""
Solve(cnf, P, R, m, s)

cnf is the 2d array containing the cnf that is to be solved
P is an int that represents the number of inital random assignments to create
R is an int that represents the number of assignments that should be 'reproduced' in every iteration
m is an int 0 to 100 that represents the percentage of 'genes'(items in an assignment) to change when selected to mutate
s is the number of iterations the genetic algorithm completes

"""
def Solve(cnf, P, R, m, s):
    nbclauses = len(cnf)
    nbvar = len(cnf[0])
    HighC = 0
    random.seed()
    myAssign = createAssignments(nbvar, P)
    AveC = []
    for run in range(s):
        c = 0
        fitness = testAssignments(cnf, myAssign)
        for i in fitness:
            #print("my i", i)
            if i > c:
                c = i
                if c > HighC:
                    HighC = c
                #print("New c", c)
        if c == len(cnf):
            print("Satisfiable")
            AveC.append(c)
            return sum(AveC)/len(AveC), HighC
        #print("Original", len(myAssign),"Run", run)
        #print(myAssign)
        myAssign = NaturalSelection(myAssign, fitness, nbclauses)
        if not myAssign:
            myAssign = createAssignments(nbvar, P)
        #print("After NS", len(myAssign))
        #print(myAssign)
        myAssign = Reproduce(myAssign, R)
        #print("After Reproduction", len(myAssign))
        #print(myAssign)
        myAssign = Mutate(myAssign, m)
        AveC.append(c)
    return sum(AveC)/len(AveC), HighC