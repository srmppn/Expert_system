import tkinter as tk
from tkinter import ttk
# ------------------------------------------
# I forgot what is this line responsible for..
class node:
    def __init__(self):
        self.truth = False
        self.link = []

# -------------------------------------------------------------
# this class responsible for receiving data/rules from the user
class get_rules:
    def __init__(self):
        self.rules = []
        self.rules_ipm = []
        self.truth = {}
        self.numb_r = int(input("Enter number of rules: "))
        for i in range(self.numb_r):
            self.rules.append(input("Enter rules: "))
            if "and" in self.rules[i] or "or" in self.rules[i]:
                # ---------------------------------------------
                # this just split a phrase into several phrases
                phrase = self.remov_it(self.rules[i]).split()
                pre = phrase[1].split('-')
                con = phrase[3].split('-')
                for n in pre:
                    for m in con:
                        self.rules_ipm += ["if " + n + " then " + m]
                        self.truth[n] = False
            else:
                self.rules_ipm += [ self.rules[i] ]
                self.truth[self.rules[i][3]] = False
    # ------------------------------------------------------
    # nothing just remove unnessary things that I don't want
    def remov_it(self, msg):
        return msg.replace(' and ','-').replace(' or ','-')
    # -----------------------------------------------------
    # returns all the things, ( should set to private )
    def get_rule_ipm(self):
        return self.rules_ipm
    def get_rule(self):
        return self.rules
    def get_truth(self):
        return self.truth

# ---------------------------------------------------
# knowledge_base system
class kb:
    def __init__(self):
        rule = get_rules()
        self.rulse = rule.get_rule()
        self.truth = rule.get_truth()
        self.rules_ipm = rule.get_rule_ipm()
        self.linkage = {}
        self.result = {}
    def remov_it(self,msg):
        return msg.replace('if ','').replace(' then ',' ')
    # ---------------------------------------
    # successfully estabish
    def estabish_link(self):
        for r in self.rules_ipm:
            conclusion = r.split()[3]
            for j in self.rules_ipm:
                if j is not r:
                    #premise = ['q','z']
                    premise = j.split()[1]
                    #link = ["x and y",'q']
                    link = r.split()[1]
                    if premise in conclusion:
                        try:
                            self.linkage[ premise ] += [ link ]
                            self.linkage[ premise ] = list(set(self.linkage[ premise ]))
                        except KeyError:
                            self.linkage[ premise ] = [ link ]
            else:
                if conclusion not in self.linkage:
                    try:
                        self.result[ conclusion ] += [ r.split()[1] ]
                        self.result[ conclusion ] = list(set(self.result[ conclusion ]))
                    except KeyError:
                        self.result[ conclusion ] = [ r.split()[1] ]
        # --------------------------------------
        # unnessary line just checking the result
        '''  
        print(self.linkage)
        print(self.truth)
        print(self.result)
        '''

    def remov_it(self, msg):
        return msg.replace(' and ','-').replace(' or ','-')
    def run(self):
        # ------------------------------------------------------------
        # another variable just for count the result
        numb_result = 0
        #-------------------------------------------------------------
        # Get the input from user if and only if it's the intermediate node
        prevent = []
        for R in self.rules_ipm:
            prev = R[3]
            if prev not in self.linkage and prev not in prevent :
                msg = "Is " + prev + " True or False? : "
                self.truth[prev] = input(msg) == "t"
                prevent.append(prev)
        #-------------------------------------------------------------
        # Traverse into the trees and check all the values in there
        for K in self.rulse:
            phrase = self.remov_it(K).split()
            temp = phrase[3].split('-')
            for check in temp:
                # ----------------------------------------------------
                # and-type checker
                if "and" in K:
                    if check in self.result:
                        count = 0
                        for re in self.result[check]:
                            if self.truth[re]:
                                count += 1
                        if count == len(self.result[check]):
                            print("Result:",check)
                            numb_result += 1
                    else:
                        count = 0
                        for re in self.linkage[check]:
                            if self.truth[re]:
                                count += 1
                        if count == len(self.linkage[check]):
                            self.truth[check] = True
                # ----------------------------------------------------
                # or-type checker
                elif "or" in K:
                    if check in self.result:
                        count = 0
                        for re in self.result[check]:
                            if self.truth[re]:
                                count += 1
                        if count > 0:
                            print("Result:",check)
                            numb_result += 1
                    else:
                        count = 0
                        for re in self.linkage[check]:
                            if self.truth[re]:
                                count += 1
                        if count > 0:
                            self.truth[check] = True
                # ----------------------------------------------------
                # otherwise checker
                else:
                    if check in self.result:
                        count = 0
                        for re in self.result[check]:
                            if self.truth[re]:
                                count += 1
                        if count == len(self.result[check]):
                            print("Result:",check)
                            numb_result += 1
                    else:
                        count = 0
                        for re in self.linkage[check]:
                            if self.truth[re]:
                                count += 1
                        if count == len(self.linkage[check]):
                            self.truth[check] = True
        # ----------------------------------------------------
        # The numb_result just count how many results are found
        # if it's zero that means result wasn't found
        if numb_result is 0:
            print("Result wasn't found")


#---Expert_System_Implementation---;
#-----------main-------------------;
t = kb()
t.estabish_link()
t.run()




#----------------------------------;
