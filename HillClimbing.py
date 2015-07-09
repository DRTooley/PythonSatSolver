import GeneralSatTools as GST


"""
GetBestAssignment(cnf, assignment)

cnf is the 2d array containing the cnf that is to be solved
assignment is the assignment that is to be expanded and then the highest valued node will be followed

returns the best possible next assignment and the c value associated with that assignment
"""
def GetBestAssignment(cnf, assignment):
    BestAssign = GST.DeepCopy(assignment)
    BestC = GST.testAssignments(cnf,assignment)
    for i in range(len(assignment)):
        #change node
        assignment[i] *= -1
        tempC = GST.testAssignments(cnf,assignment)
        if(tempC > BestC):
            BestC = tempC
            BestAssign = GST.DeepCopy(assignment)
        #reverse node change, continue loop through with next node
        assignment[i] *= -1

    return BestAssign, BestC
"""
HillClimbing(cnf, assignment)

cnf is the 2d array containing the cnf that is to be solved
assignment is the assignment that is to be expanded and followed until a local maxium is reached
"""
def HillClimbing(cnf, assignment):
    CurrentEval = GST.testAssignments(cnf, assignment)
    NextAssignment, NextEval = GetBestAssignment(cnf, assignment)
    if(NextEval<=CurrentEval):
        #print(CurrentEval)
        return CurrentEval
    else:
        #print("dig")
        return HillClimbing(cnf, NextAssignment)
"""
Solve(cnf,s)

cnf is the 2d array containing the cnf that is to be solved
s is the number of local searches to perform until returning the highest found c value
"""
def Solve(cnf, s):
    AveC=[]
    HighC = -1
    for i in range(s):
        Best = -1
        #print("restart")
        MyAssignment = GST.GenerateRandomAssignment(len(cnf[0]))
        newC = HillClimbing(cnf, MyAssignment)
        if newC > Best:
            Best = newC
            if Best > HighC:
                HighC = Best
            if(Best == len(cnf)):
                print("Satisfiable")
                AveC.append(Best)
                return sum(AveC)/len(AveC), HighC
        AveC.append(Best)
    return sum(AveC)/len(AveC), HighC