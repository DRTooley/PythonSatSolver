
import Genetic
import DPLL
import HillClimbing
import time
import glob
"""
is_int(s)

s is a string or char that is tested to see if it is an integer

returns True if it is an int, False if it is not
"""
def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
"""
main
loops through every *.cnf file that is in the same directory as main.py and opens that file.
it assumes every .cnf file is given in the correct format.
it will fun Hill Climbing and Genetic Algorithm ten times and DPLL once for each and give the best result from each

handles the file reading for the .cnf files and saves them in a 2d array
then calls hill climbing, genetic, and DPLL while timing each call and printing the most clauses satisfied
"""
if __name__ == '__main__':
    for filename in glob.glob("*.cnf"):
        print(filename)
        cnf = []
        nbclauses = -1
        nbvar = -1
        with open(filename) as file:
            content = file.readlines()
            curClause = -1
            for line in content:
                splitLine = line.split(' ')
                if splitLine[0] == 'p' and splitLine[1] == 'cnf':
                    nbvar = int(splitLine[2])
                    nbclauses = int(splitLine[3])
                    #print(nbvar)
                    #print(nbclauses)
                    #print("previous two nbvar, nbclauses")
                    cnf = [[0 for i in range(nbvar)] for j in range(nbclauses)]
                elif nbvar > 0 and nbclauses > 0 and splitLine[0] != 'c':
                    curClause += 1
                    for variable in splitLine:
                        if is_int(variable):
                            if int(variable) != 0:
                                cnf[curClause][abs(int(variable))-1] = int(variable)


        #for clause in cnf:
        #    print(clause)

        #number of iterations
        s = 10

        HillStart = time.time()
        cHillAve, HighHillc = HillClimbing.Solve(cnf, s)
        HillEnd = time.time()
        print("Ave case Hill Climbing:", cHillAve, "Highest:", HighHillc)
        print("Hill Climbing run time:", HillEnd - HillStart, "seconds")


        #Genetic variables
        P = 150
        R = 800
        m = 10 #mutates 10%

        GeneticStart = time.time()
        cGeneticAve, HighGeneticc = Genetic.Solve(cnf, P, R, m, s)
        GeneticEnd = time.time()
        print("Ave case Genetic:", cGeneticAve, "Highest:", HighGeneticc)
        print("Genetic run time:", GeneticEnd - GeneticStart, "seconds")

        #Currently set to time out after 1 minute
        DpllStart = time.time()
        cDPLL = DPLL.Solve(cnf)
        DpllEnd = time.time()

        print("Best case DPLL:", cDPLL)
        print("DPLL run time:", DpllEnd - DpllStart, "seconds")

        print('')