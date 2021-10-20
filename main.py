import itertools

#Constants
FILES_ACCES_MODE = 'r'
RULES_PREM_CONC_SEP = "alors"
PREM_CONJONCTION = " et "
RULE_LBL_SEP = ':'
RULE_PREFIX = "si"
CON_SEP = " et "

def gen_list_of_combinations(items):
    res = []
    for index in range(1,len(items) + 1 ):
        res.append([list(comb) for comb in list(itertools.combinations(items, index))])
    return res

def is_condidate(rule,fact):
    return ( len(list( set(rule["Premises"]) - set(fact) )) == 0 ) and ( len(list( set(fact) - set(rule["Premises"]) )) == 0 )

def strip_list(items):
    return [ item.strip() for item in items]

def print_list(items,msg):
    print(msg)
    if len(items) == 0:
        print("empty list.")
    for item in items:
        print(item)

def form_rule(line):
    line = line.strip().lower()
    split = line.split(RULE_LBL_SEP)
    lbl = split[0]
    rule = split[-1]
    split = rule.split(RULE_PREFIX)
    rule = split[-1]
    split = rule.split(RULES_PREM_CONC_SEP)
    premises = strip_list(split[0].split(PREM_CONJONCTION))
    conclusions = strip_list(split[-1].split(CON_SEP))
    return {"Rule":lbl,"Premises":premises,"Conclusions":conclusions}

def form_fact(line):
    return line.strip().lower()

def interfere_file(filename,form_line):
    res=[]
    with open(filename,FILES_ACCES_MODE) as file:
       lines = file.readlines()
       for line in lines:
         res.append(form_line(line))
    return res


def interfere(rules_db_filename,facts_db_filename,end_goal):
 
  rules = interfere_file(rules_db_filename,form_rule)
  facts = interfere_file(facts_db_filename,form_fact)
  
  print(facts)
  print(rules)

  while len(rules) > 0 :
    print("-----------")
    print("Facts in this iteration : ")
    print(facts)
    print("------------")

    condidate_rules = []
    facts_combinitions_stages = gen_list_of_combinations(facts)
    new_facts = []
    for rule in rules:
        print("-----------")
        print("Rule to check : ")
        print(rule)
        print("------------")
        for stage in facts_combinitions_stages:
        
            for fact_combinition in stage:
                print("------")
                print("FACT COMBINATION: ")
                print("------")
                print(fact_combinition)
                if is_condidate(rule,fact_combinition):
                    condidate_rules.append(rule)
                    rules.remove(rule)
                    new_fact_rule =  condidate_rules[0]
                    new_fact = new_fact_rule["Conclusions"][0]
                    new_facts.append(condidate_rules[0]["Conclusions"][0])
                    print("^^^^ SELECTED RULE IS CANDIDATE FOR FACT COMBINATION ^^^^")
                    print("THE CANDIDATE RULES : ")
                    print(condidate_rules)
                    print("------")
                    print("RULES : ")
                    print(rules)
                    print("------")
                     #Check if goal is interfered?
                    if end_goal == new_fact  :
                        print("####################")
                        print("'" + end_goal + "'" + " has been interfered by rule : ")
                        print(condidate_rules[0])
                        print("RULES : ")
                        print(rules)
                        print("Facts : ")
                        print(facts)
                        exit(0)

    if len(condidate_rules) == 0 :
        print("#############")
        print("[ERROR] : No candidate rule for the given facts :( ")
        print("#####FACTS#######")
        print(facts)
        exit(1)
    
    print("-----------")
    print("Learnt facts in this iteration : ")
    print(new_facts)
    print("------------")

    facts = list( set( facts + new_facts ) ) 
    


  return [rules,facts]

   

def start():
  rules_db_filename = input("Please enter the filename of the rules database : ")
  facts_db_filename = input("Please enter the filename of the facts database : ")
  end_goal = input("Please enter what you want to infere? ").lower().strip()
  if len(end_goal) == 0:
      print("You did not provide an intended goal to interfere,therefore the program will interfere until it reaches a dead end.")
 
  rules,facts = interfere(rules_db_filename,facts_db_filename,end_goal)
  print_list(rules,"Rules")
  print_list(facts,"Facts")


#Main program
start()

