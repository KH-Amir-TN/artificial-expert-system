
#Constants
FILES_ACCES_MODE = 'r'
RULES_PREM_CONC_SEP = "alors"
PREM_CONJONCTION = " et "
RULE_LBL_SEP = ':'
RULE_PREFIX = "si"
CON_SEP = " et "


def print_list(items,msg):
    print(msg)
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
    premises = split[0].split(PREM_CONJONCTION)
    conclusions = split[-1].split(CON_SEP)
    return {lbl:{"Premises":premises,"Conclusions":conclusions}}

def form_fact(line):
    return line.strip().lower()

def interfere_file(filename,form_line):
    res=[]
    with open(filename,FILES_ACCES_MODE) as file:
       lines = file.readlines()
       for line in lines:
         res.append(form_line(line))
    return res


def interfere(rules_db_filename,facts_db_filename):
 
  rules = interfere_file(rules_db_filename,form_rule)
  facts = interfere_file(facts_db_filename,form_fact)
  return [rules,facts]

   

def start():
  rules_db_filename = input("Please enter the filename of the rules database : ")
  facts_db_filename = input("Please enter the filename of the facts database : ")
  rules,facts=interfere(rules_db_filename,facts_db_filename)
  print_list(rules,"Rules")
  print_list(facts,"Facts")


#Main program
start()

