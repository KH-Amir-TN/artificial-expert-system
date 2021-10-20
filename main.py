import itertools,time

#Constants
FILES_ACCES_MODE = 'r'
RULES_PREM_CONC_SEP = "alors"
PREM_CONJONCTION = " et "
RULE_LBL_SEP = ':'
RULE_PREFIX = "si"
CON_SEP = " et "
LOG_OUT = "./logs/"
LOG_FILENAME = str( time.time() ) + ".log"

LOG_FILE = open(LOG_OUT + LOG_FILENAME , "w")



def log(msg):
    if LOG_FILE:
        LOG_FILE.writelines(str( msg ) + "\n")
    print(msg)

def resolve_conflict(rules):
    return rules[0]
    

def gen_list_of_combinations(items):
    res = []
    for index in range(1,len(items) + 1 ):
        res.append([list(comb) for comb in list(itertools.combinations(items, index))])
    return res

def is_candidate(rule,fact):
    return ( len(list( set(rule["Premises"]) - set(fact) )) == 0 ) and ( len(list( set(fact) - set(rule["Premises"]) )) == 0 )

def strip_list(items):
    return [ item.strip() for item in items]

def print_list(items,msg):
    log(msg)
    if len(items) == 0:
        log("empty list.")
    for item in items:
        log(item)

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
 
  init_rules = interfere_file(rules_db_filename,form_rule)
  init_facts = interfere_file(facts_db_filename,form_fact)
  facts = init_facts
  rules = init_rules
  log(facts)
  log(rules)


  while len(rules) > 0 :

    log("#####")
    log("NEW ITERATION")
    log("#####")

    log("-----------")
    log("Facts in this iteration : ")
    log(facts)
    log("------------")

    log("------")
    log("RULES : ")
    log(rules)
    log("------")

 

    facts_combinitions_stages = gen_list_of_combinations(facts)


    new_facts = []
    init_rules_len = len(rules)
    for stage in facts_combinitions_stages:
        
        for fact_combinition in stage:
            log("------")
            log("FACT COMBINATION: ")
            log("------")
            log(fact_combinition)
            candidate_rules = []
            for rule in rules:
                log("-----------")
                log("Rule to check : ")
                log(rule)
                log("------------")

                if is_candidate(rule,fact_combinition):
                    candidate_rules.append(rule)
                    log("---------")
                    log("^^^^ SELECTED RULE IS CANDIDATE FOR FACT COMBINATION ^^^^")
                    log("THE CANDIDATE RULES BECOMES : ")
                    log(candidate_rules)
                    log("---------")


            if  len(candidate_rules) > 0 :
                new_fact_rule = resolve_conflict(candidate_rules)
                new_fact = new_fact_rule["Conclusions"]
                new_facts += new_fact
                rules.remove(new_fact_rule)
                #Check if goal is interfered?
                if end_goal in new_fact  :
                    log("####################")
                    log("'" + end_goal + "'" + " has been interfered by rule : ")
                    log(new_fact_rule)
                    log("RULES : ")
                    log(rules)
                    log("Facts : ")
                    log(facts)
                    exit(0)

    if len(rules) == init_rules_len :

        log("#############")
        log("[ERROR] : No candidate rule for the given facts :( ")
        log("#####FACTS#######")
        log(facts)
        log("#####RULES#######")
        log(rules)
        
        exit(1)
                  
    log("-----------")
    log("Learnt facts in this iteration : ")
    log(new_facts)
    log("------------")
    facts = list( set( facts + new_facts ) ) 

    
    


  return [rules,facts,candidate_rules]

   

def start():
  rules_db_filename = input("Please enter the filename of the rules database : ")
  facts_db_filename = input("Please enter the filename of the facts database : ")
  end_goal = input("Please enter what you want to infere? ").lower().strip()
  if len(end_goal) == 0:
      print("You did not provide an intended goal to interfere,therefore the program will interfere until it reaches a dead end.")
 
  rules,facts,candidate_rules = interfere(rules_db_filename,facts_db_filename,end_goal)
  log("-----")
  print_list(rules,"Rules")
  log("-----")
  print_list(facts,"Facts")
  log("-----")
  print_list(candidate_rules,"Candidate rules")   

#Main program
start()
LOG_FILE.close()

