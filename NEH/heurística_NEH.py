

from itertools import permutations  # Library for set permutations
import numpy as np
from prettytable import PrettyTable


### FUNCTIONS ###

def makespan(sequencia, Tij):  # Function to calculate the makespan
    global m
    global n
    m = len(sequencia)  # Number of jobs;
    n = len(Tij[0])  # Number of machines

    # Seq: Time Matrix organized according to the sequence
    global Seq
    Seq = [[Tij[i][j] for j in range(n)] for i in sequencia]

    # Cij: Matrix of Completion times, initially started on 0
    global Cij
    Cij = [[0 for j in range(n)] for i in range(m)]

    Cij[0][0] = Seq[0][0]  # Comp. time for the first job at the first machine

    for i in range(1, m):
        for j in range(1, n):
            Cij[i][0] = Cij[i - 1][0] + Seq[i][0]  # Completion time in first machine
            Cij[0][j] = Cij[0][j - 1] + Seq[0][j]  # Completion of the first job on machine j

    for i in range(1, m):
        for j in range(1, n):
            if Cij[i - 1][j] > Cij[i][j - 1]:  # If the machine is free
                Cij[i][j] = Cij[i - 1][j] + Seq[i][j]
            else:
                Cij[i][j] = Cij[i][j - 1] + Seq[i][j]

    return Cij[-1][-1]  # Makespan = Cmn


def Sort_Tuple(tup):  # Function to sort tuples according second position
    # reverse = None (Sorts in Ascending order)/ True (Sorts in Descending order)
    # key is set to sort using second element of
    # sublist lambda has been used
    tup.sort(key=lambda x: x[1], reverse=True)
    return tup


# Functions to exchange numbers following an order
def _permute(L, nexts, numbers, begin, end):
    if end == begin + 1:
        yield L
    else:
        for i in range(begin, end):
            c = L[i]
            if nexts[c][0] == numbers[c]:
                nexts[c][0] += 1
                L[begin], L[i] = L[i], L[begin]
                for p in _permute(L, nexts, numbers, begin + 1, end):
                    yield p
                L[begin], L[i] = L[i], L[begin]
                nexts[c][0] -= 1


def constrained_permutations(L, constraints):
    # warning: assumes that L has unique, hashable elements
    # constraints is a list of constraints, where each constraint is a list of elements which should appear
    # in the permutation in that order
    # warning: constraints may not overlap!
    nexts = dict((a, [0]) for a in L)
    numbers = dict.fromkeys(L, 0)  # number of each element in its constraint
    for constraint in constraints:
        for i, pos in enumerate(constraint):
            nexts[pos] = nexts[constraint[0]]
            numbers[pos] = i

    for p in _permute(L, nexts, numbers, 0, len(L)):
        yield p


### READING THE FILE WITH PROCESS TIMES ###

file = open('dados_NEH.txt','r')  # Open file named work03_NEH.txt
lines = file.readlines()  # Read all file
file.close()  # Close file

Tij = []  # Array to receive the time processes from job i at machine j

for i in range(len(lines)):
    # For each line i from lines, split the content to separator '\t'
    row = lines[i].split()
    row = [int(j) for j in row]  # Convert each character j in row from string to int
    Tij.append(row)  # Append the row i to matrix Tij

print (" The data are: ",Tij)
### NEH ALGORITHM ###

## STEP 1: Calculate the total processing time of each job al all machines ##

Pi = []  # Array to receive the sum_j Tij for all i
A = []  # Array to receive the copy of vector Pi with the time and position
initial_seq = []  # Array to receive the initial sequence

for i in range(len(Tij)):
    Pi.append(sum(Tij[i]))  # Total processing time of each job at all machines

for i in range(len(Tij)):
    x = (i, Pi[i])  # Creates a tuple with the job i and total time processing Pi
    A.append(x)  # Creates an array of tuples

A = Sort_Tuple(A)  # Sort the array A in descending order of Pi

for i in range(len(A)):
    initial_seq.append(A[i][0])  # Takes the position of each job after sorted

## STEP 2: ##
# Evaluate two partial sequences {J1,J2} and {J2, J1} and chosse the one with samaller makespan
#  to be 2-partial sequence ##

Makespan = []  # Array to calculate makespan for each partial sequence
l = list(permutations([initial_seq[0], initial_seq[1]]))  # exchanges two firsts elements of initial_seq
l = [list(i) for i in l]  # list of lists

for i in range(len(l)):
    Makespan.append(makespan(l[i], Tij))  # Calculate makespan for the partial sequences

constraints = [l[Makespan.index(min(Makespan))]]  # Array to maintain the order of the jobs

S = (l[Makespan.index(min(Makespan))])  # 2-partial sequence
S1 = S.copy()

## STEP 3: ##
# As for ( 3,..., ) k J k = n , insert it to k possible places of the (k−1) -partial solution,
# evaluate the k partial sequences, and choose the one with the smallest makespan
# to be the k partial solution.

for i in range(2, len(initial_seq)):

    S1.insert(1, initial_seq[i])  # Insert k element at the second position of the array S1
    A = list(p[:] for p in constrained_permutations(S1, constraints))  # copy the permutation if you want to keep it
    Makespan = []

    for i in range(len(A)):
        Makespan.append(makespan(A[i], Tij))  # Calculate makespan for the partial sequences

    constraints.append(A[Makespan.index(min(Makespan))])  # Array to maintain the order of the jobs

### Results ###
print("Sequence: ", constraints[-1], "\n")  # The last sequence of constraint is the NEH-sequence
print("Makespan: ", min(Makespan))  # Minimum makespan
print("Completion time: ")
pt = PrettyTable(["M1", "M2", "M3"])
for i in Cij:
    pt.add_row(i)
print(pt)

