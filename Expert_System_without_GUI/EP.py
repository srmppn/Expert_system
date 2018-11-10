from tkinter import *
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
        print("#-------------NUMBER OF RULES--------------#")
        self.numb_r = int(input("# Enter number of rules: "))
        print("#-----------------RULES--------------------#")
        for i in range(self.numb_r):
            self.rules.append(input("# Enter rules: "))
            # ---------------------------------------------
            # this just split a phrase into several phrases
            phrase = self.remov_it(self.rules[i][3:]).split(' then ')
            pre = phrase[0].split('-')
            con = phrase[1].split('-')
            for n in pre:
                for m in con:
                    self.rules_ipm += ["if " + n + " then " + m]
                    self.truth[n] = False
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
            conclusion = r[3:].split(' then ')[1]
            link = r[3:].split(' then ')[0]
            for j in self.rules_ipm:
                if j is not r:
                    #premise = ['q','z']
                    premise = j[3:].split(' then ')[0]
                    #link = ["x and y",'q']
                    if premise in conclusion:
                        try:
                            self.linkage[ premise ] += [ link ]
                            self.linkage[ premise ] = list(set(self.linkage[ premise ]))
                        except KeyError:
                            self.linkage[ premise ] = [ link ]
            else:
                if conclusion not in self.linkage:
                    try:
                        self.result[ conclusion ] += [ link ]
                        self.result[ conclusion ] = list(set(self.result[ conclusion ]))
                    except KeyError:
                        self.result[ conclusion ] = [ link ]
        # --------------------------------------
        # unnessary line just checking the result if it works properly
        '''
        print(self.rules_ipm)
        print(self.linkage)
        print(self.truth)
        print(self.result)
        '''
        #---------------------------------------
    def run(self):
        print("#---------------DIAGNOSING-----------------#")
        conclude = "Result: "
        # ------------------------------------------------------------
        # another variable just for count the result
        numb_result = 0
        #-------------------------------------------------------------
        # Get the input from user if and only if it's the intermediate node
        prevent = []
        for R in self.rules_ipm:
            prev = R[3:].split(' then ')[0]
            if prev not in self.linkage and prev not in prevent :
                msg = "# Is '" + prev + "' True or False? (t/f) : "
                self.truth[prev] = input(msg) == "t"
                prevent.append(prev)
        #-------------------------------------------------------------
        # Traverse into the trees and check all the values in there
        for K in self.rulse:
            # msg.replace('if ','').replace(' then ',' ')
            phrase = K.split(' then ')
            temp = phrase[1].replace(' and ','-').replace(' or ','-').split('-')
            for check in temp:
                # ----------------------------------------------------
                # and-type checker
                if "and" in phrase[0]:
                    if check in self.result:
                        count = 0
                        for re in self.result[check]:
                            if self.truth[re]:
                                count += 1
                        if count == len(self.result[check]):
                            conclude += ( check + ", " )
                            numb_result += 1
                    else:
                        count = 0
                        for re in self.linkage[check]:
                            if self.truth[re]:
                                count += 1
                        if count == len(self.linkage[check]) and check not in prevent:
                            msg = "# Is '" + check + "' True or False? (t/f) : "
                            self.truth[check] = input(msg) == "t"
                            prevent.append(check)
                # ----------------------------------------------------
                # or-type checker
                elif "or" in phrase[0]:
                    if check in self.result:
                        count = 0
                        for re in self.result[check]:
                            if self.truth[re]:
                                count += 1
                        if count > 0:
                            conclude += ( check + ", " )
                            numb_result += 1
                    else:
                        count = 0
                        for re in self.linkage[check]:
                            if self.truth[re]:
                                count += 1
                        if count > 0 and check not in prevent:
                            msg = "# Is '" + check + "' True or False? (t/f) : "
                            self.truth[check] = input(msg) == "t"
                            prevent.append(check)
                # ----------------------------------------------------
                # otherwise checker
                else:
                    if check in self.result:
                        count = 0
                        for re in self.result[check]:
                            if self.truth[re]:
                                count += 1
                        if count == len(self.result[check]):
                            conclude += ( check + ", " )
                            numb_result += 1
                    else:
                        count = 0
                        for re in self.linkage[check]:
                            if self.truth[re]:
                                count += 1
                        if count == len(self.linkage[check]) and check not in prevent:
                            msg = "# Is '" + check + "' True or False? (t/f) : "
                            self.truth[check] = input(msg) == "t"
                            prevent.append(check)
        # ----------------------------------------------------
        # The numb_result just count how many results are found
        # if it's zero that means result wasn't found
        print("#---------------CONCLUSION-----------------#")
        if numb_result is 0:
            print("# Result wasn't found")
        else:
            print('#',conclude[0:-2])
        # print result ----------------------------------------
        # end of statement ------------------------------------


#---Expert_System_Implementation---;
#-----------main-------------------;
#-------with_GUI-------------------;

'''
window = Tk()
window.title("Expert System")
Label(window,text="Enter number of rules: ").grid(column=0,row=0)

numb = StringVar()
numb_ent = Entry(window,width=6,textvariable=numb)
numb_ent.grid(column=1,row=0)
numb_ent.focus()

but1 = Button(window,text="Submit",click)
but1.grid(column=3,row=0)

window.config(width=500,height=500)
window.mainloop()
'''

#-------------Without_GUI----------;
print("#--------------EXPERT_SYSTEM---------------#")
print("#------------------------------------------#")
t = kb()
t.estabish_link()
t.run()
print("#------------------------------------------#")
print("#-------------------END--------------------#")
#----------------------------------;
