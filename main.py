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
LOG_AND_PRINT = False 

LOG_FILE = open(LOG_OUT + LOG_FILENAME , "w")


def preflight_checks(facts,goal):
    if goal in facts:
        MSG = "The given goal '"+ goal +"' is a fact." 
        log("#################",explicit_log_and_print=True)
        log(MSG,explicit_log_and_print=True)
        log("#############",explicit_log_and_print=True)
        print_completion(0)
        exit(0)

def log(msg,explicit_log_and_print=False):
    if LOG_FILE:
        LOG_FILE.writelines(str( msg ) + "\n")
    if LOG_AND_PRINT or explicit_log_and_print :
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

def print_completion(period):

    PERIOD_PRECISION = '.3f'

    log("##################################",explicit_log_and_print=True)
    log("Completed in " + format(period,PERIOD_PRECISION) + " seconds." ,explicit_log_and_print=True)
    log("##################################",explicit_log_and_print=True)

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


def reverse_chain(rules,facts,end_goal):
    
    log("#################")
    log("Reverse chaining the end goal: "+end_goal)
    log("#################")

    if(end_goal in facts):
        log("The end goal "+end_goal+" is a fact")
        return True

    log("#################")
    log("Extracting candidate rules for the end goal "+end_goal)
    log("#################")

    candidate_rules = []
    for rule in rules:
        log("Checking rule "+ rule['Rule'])
        conclusions = rule['Conclusions']
        if end_goal in conclusions:
            log("Rule "+rule['Rule']+" is a candidate rule.")
            candidate_rules.append(rule)
    
    log("#################")    
    log("Candidate rules for the end goal "+end_goal+":")
    log(candidate_rules)
    log("#################")

    if len(candidate_rules) == 0:
        log("#########################",explicit_log_and_print=True)
        log("[Error] The goal "+end_goal+" has no candidate rule.",explicit_log_and_print=True)
        log("#########################",explicit_log_and_print=True)
        return False
    
    candidate_rule = resolve_conflict(candidate_rules)
    log("Elected candidate rule:")
    log(candidate_rule)

    #Extract premises from candidate_rule
    
    candidate_rule_premises = candidate_rule['Premises']
    
    for premise in candidate_rule_premises:
       if not reverse_chain(rules,facts,premise):
           return False
     
    log("The end goal "+end_goal+" has been interfered by the rule:")
    log(candidate_rule)
    return True


def interfere(rules_db_filename,facts_db_filename,end_goal):
 
  init_rules = interfere_file(rules_db_filename,form_rule)
  init_facts = interfere_file(facts_db_filename,form_fact)

  log("######### INIT FACTS ##############",explicit_log_and_print=True)
  log(init_facts,explicit_log_and_print=True)
  log("######### INIT RULES ##############",explicit_log_and_print=True)
  log(init_rules,explicit_log_and_print=True)
  log("####################################",explicit_log_and_print=True)

  facts = init_facts
  rules = init_rules

  
  preflight_checks(facts,end_goal)
  
  start_time = time.time()
  if not LOG_AND_PRINT:
      print("Interfering ...")

  has_interfered_endgoal = reverse_chain(rules,facts,end_goal)

  
    
  end_time = time.time()

  return [rules,facts,end_time - start_time]

   

def start():
  rules_db_filename = input("Please enter the filename of the rules database : ")
  facts_db_filename = input("Please enter the filename of the facts database : ")
  end_goal = input("Please enter what you want to infere? ").lower().strip()
  while(len(end_goal) == 0):
   if len(end_goal) == 0:
      print("You did not provide an intended goal to interfere!")
   end_goal = input("Please enter what you want to infere? ").lower().strip()
  
  rules,facts,period = interfere(rules_db_filename,facts_db_filename,end_goal)
  log("--- END RULES ---")
  print_list(rules,"Rules")
  log("--- END FACTS ---")
  print_list(facts,"Facts")

  print_completion(period)

#Main program
start()
LOG_FILE.close()

