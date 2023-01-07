# This class finds the amount of funds that need to be spent on 3 different subcomponents
#  (Treasury, Nodes, Token) to maximize the probability of reaching KPI targets on a
#  certain date.
#
#  ________________________________________________________________________________
#  INPUT    :     Decision variables:
#                  + Funds to be spent on each subcomponent
#                 Cost:
#                   + KPI increment per dollar spent on each subcomponent
#                 Constraints:
#                   + Total Budget
#                   + maximum budget for each channel
#                   + minimum budget for each channel
#
#  OUTPUT   :       + USD that should be spent on each channel
#                   + Overall KPI completion score
#  _________________________________________________________________________________
import pulp as p
import json

class DCA:

    def __init__(self):
        self.LP = p.LpProblem('Max_KPI_completion', p.LpMaximize)

    def userInput(self):
        accepted = False;
        min = []
        max = []
        names = []
        targets = []
        states = []
        while not accepted:
            ans = input("(F)ile / (M)anual input? or (T)esting? (F or M or T): ")
            if ans == 'F' or 'M' or 'T':
                if ans == 'F':
                    data = json.loads("data.json")
                    # Read data.json to the arrays of names, min, max, targets, states, total_budget
                elif ans == 'M':
                    total_budget = float(input("What is the total revenue? $"))
                    for i in range(3):
                        names.append(input("Enter subcomponent " + str(i + 1) + " name: "))
                        max.append(float(input("What is the max allocation cap for " + names[i] + "? $")))
                        min.append(float(input("What is the min allocation required for " + names[i] + "? $")))
                        targets.append(float(input("What is the KPI target for " + names[i] + "? $")))
                        states.append(float(input("What is the KPI value for " + names[i] + "? $")))
                        print()
                elif ans == 'T':
                    min = [100, 200, 400]
                    max = [5000, 5000, 4000]
                    names = ["Treasury", "Nodes", "Token"]
                    targets = [94, 92, 13]
                    states = [24, 85, 6]
                    total_budget = 8000
                accepted = True;
                return names, min, max, targets, states, total_budget
            else:
                print("Enter either M or F or T")

    def preprocess(self, min, max, targets, states, total_budget):
        x = []
        c = []
        # Create problem Variables
        x.append(p.LpVariable(name="x1", lowBound=min[0], upBound=max[0]))  # Subcomponent 1
        x.append(p.LpVariable(name="x2", lowBound=min[1], upBound=max[1]))  # Subcomponent 2
        x.append(p.LpVariable(name="x3", lowBound=min[2], upBound=max[2]))  # Subcomponent 3
        # KPI increment per dollar spent for each subcomponent
        c.append(0.04)
        c.append(0.03)
        c.append(0.05)
        # Objective Function
        self.LP += (c[0] * x[0]) / (targets[0] - states[0]) + (c[1] * x[1]) / (targets[1] - states[1]) + (
                c[2] * x[2]) / (targets[2] - states[2])

        # Total Budget constraints
        self.LP += x[0] + x[1] + x[2] <= total_budget  # Total budget in USD
        return x

    def solve(self, names, x):
        # Display the problem print(LP)
        status = self.LP.solve()
        print(p.LpStatus[status])
        # Printing the final solution
        print("______________________________________________________________________________")
        for i in range(3):
            print(names[i] + " budget is $" + str(p.value(x[i])))
        print("------------------------------------------------------------------------------")
        print("Total KPI increment: " + str(p.value(self.LP.objective)))
        print("------------------------------------------------------------------------------")


if __name__ == '__main__':
    DCA = DCA()
    var = DCA.userInput()
    x = DCA.preprocess(var[1], var[2], var[3], var[4], var[5])
    DCA.solve(var[0], x)
