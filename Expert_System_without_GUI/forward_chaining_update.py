import os
import pickle
# contributor srmppn @contact somrak.monpengpinit@g.swu.ac.th
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
        while(True):
            print("#--------------- MAIN MENU ----------------#")
            pickle_in = open("rule_list.pickle", "rb")
            try:
                self.list_of_rule = pickle.load(pickle_in)
            except EOFError:
                self.list_of_rule = []
            if len(self.list_of_rule) == 0:
                print("# No rules has been created yet")
                if input("# Do you want to create a rule? ( Y/N )? : ") == 'y':
                    self.make_rule()
            print("# 1. Rules manipulate")
            print("# 2. Run test")
            print("#------------------------------------------#")
            choice = int(input("# Select choice: "))
            if choice == 1:
                print("#------------RULES MANIPULATE--------------#")
                self.sub_menu()
            elif choice == 2:
                print("#---------------- RUN TEST ----------------#")
                self.show_rules()
                self.choose_rule()
                pickle_in.close()
                break
    def sub_menu(self):
        print("# 1. Add rule")
        print("# 2. Edit rule")
        print("# 3. Delete rule")
        print("# 4. Show rules")
        print("# 5. Back to main menu")
        print("#------------------------------------------#")
        choice = int(input("# Select choice: "))
        if choice == 1:
            self.Add_rule()
        elif choice == 2:
            self.Edit_rules()
        elif choice == 3:
            self.Delete_rule()
        elif choice == 4:
            self.show_each_rule()
    def Delete_rule(self):
        self.show_rules()
        choose = int(input("# Choose rule to delete:"))
        os.remove(self.list_of_rule[choose])
        pickle_list = open("rule_list.pickle", "wb")
        self.list_of_rule.pop(choose)
        pickle.dump(self.list_of_rule,pickle_list)
        pickle_list.close()
    def Add_rule(self):
        self.make_rule()
    def Edit_rules(self):
        self.show_rules()
        print("#------------------------------------------#")
        numb_rule = int(input("# Select the rule: "))
        print("#------------------------------------------#")
        self.open_rule(numb_rule)
        for j in self.rules:
            print('#',j)
        print("#------------------------------------------#")
        numb_each = int(input("# Which rule: "))
        print("#------------------------------------------#")
        if numb_each < len(self.rules):
            self.rules[numb_each] = input("# Enter new rule: ")
            self.save_rule(numb_rule)
        else:
            print("# Error occurs please try again..")
        print("#----RULE HAS BEEN EDITED SUCCESSFULLY-----#")
    def show_rules(self):
        print("#-------------- LIST OF RULES -------------#")
        for numb in range(len(self.list_of_rule)):
            print('#', 'Rule[' + str(numb) + ']:', self.list_of_rule[numb][:-7])
        print("#------------------------------------------#")
    def show_each_rule(self):
        self.show_rules()
        numb_rule = int(input("# Select the rule: "))
        self.open_rule(numb_rule)
        for j in self.rules:
            print('#',j)
    def choose_rule(self):
        select = int(input("# Select the rule that you want to test: "))
        if select < len(self.list_of_rule):
            pickle_take_rules = open(self.list_of_rule[select], "rb")
            self.rules = pickle.load(pickle_take_rules)
            pickle_take_rules.close()
        print("# ---------RULE HAS BEEN SELECTED----------#")
    def open_rule(self,numb):
        pickle_out = open(self.list_of_rule[numb],"rb")
        self.rules = pickle.load(pickle_out)
        pickle_out.close()
    def save_rule(self,numb):
        pickle_out = open(self.list_of_rule[numb], "wb")
        pickle.dump(self.rules,pickle_out)
        pickle_out.close()
    def make_rule(self):
        print("#-----------------RULES--------------------#")
        numb_r = int(input("Enter number of rules: "))
        for i in range(numb_r):
            self.rules.append(input("# Enter rules: "))
            # ---------------------------------------------
            # this just split a phrase into several phrases
        file_name = input("Name of rule: ") + ".pickle"
        self.list_of_rule.append(file_name)
        pickle_rule = open(file_name,"wb")
        pickle_list = open("rule_list.pickle","wb")
        pickle.dump(self.list_of_rule,pickle_list)
        pickle.dump(self.rules,pickle_rule)
        pickle_rule.close()
        pickle_list.close()
        print("#----RULE HAS BEEN ADDED SUCCESSFULLY-----#")
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
        self.truth = {}
        self.rules_ipm = []
        self.linkage = {}
        self.result = {}
    def remov_it(self, msg):
        return msg.replace(' and ','-').replace(' or ','-')
    def make_tr_ipm(self):
        for i in self.rulse:
            # ---------------------------------------------
            # this just split a phrase into several phrases
            phrase = self.remov_it(i[3:]).split(' then ')
            pre = phrase[0].split('-')
            con = phrase[1].split('-')
            for n in pre:
                for m in con:
                    self.rules_ipm += ["if " + n + " then " + m]
                    self.truth[n] = False
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

        #---------------------------------------
    def shuffle(self):
        implement = []
        for K in self.rulse:
            if K not in implement:
                implement.append(K)
            phrase1 = K.split(' then ')
            temp2 = phrase1[1].replace(' and ','-').replace(' or ','-').split('-')
            for J in self.rulse:
                if K is not J:
                    phrase2 = J.split(' then ')
                    temp1 = phrase2[0][3:].replace(' and ', '-').replace(' or ', '-').split('-')
                    for c in temp1:
                        if c in temp2 and J not in implement:
                            implement.append(J)
        return implement
    def run(self):

        print("# -----------------------------------------#")
        print("#---------------DIAGNOSING-----------------#")
        '''
        print(self.rules_ipm)
        print(self.linkage)
        print(self.truth)
        print(self.result)
        '''
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
        for K in self.shuffle():
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
                        if count == len(self.linkage[check]):
                            self.truth[check] = True
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
                            conclude += ( check + ", " )
                            numb_result += 1
                    else:
                        count = 0
                        for re in self.linkage[check]:
                            if self.truth[re]:
                                count += 1
                        if count == len(self.linkage[check]):
                            self.truth[check] = True
        '''
         # show up result type 1
                if numb_result > 0:
                    print("#---------------CONCLUSION-----------------#")
                    print('#',conclude[0:-2])
                    return
        else:
            print("#---------------CONCLUSION-----------------#")
            print("# Result wasn't found")
        '''
        # ----------------------------------------------------
        # The numb_result just count how many results are found
        # if it's zero that means result wasn't found
        # show up result type 2
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
t.make_tr_ipm()
t.estabish_link()
t.run()
print("#------------------------------------------#")
print("#-------------------END--------------------#")
#----------------------------------;
