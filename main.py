
#Constants
FILES_ACCES_MODE = 'r'
RULES_PREM_CONC_SEP = '>'
PREM_CONJONCTION = '^'


def form_rule(line):
    line = line.strip()
    split = line.split(RULES_PREM_CONC_SEP)
    premises = split[0].split(PREM_CONJONCTION)
    conclusion = split[-1]
    return [premises,conclusion]

def form_fact(line):
    return line.strip()

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
  return [{"Rules":rules},{"Facts":facts}]

   

def start():
  rules_db_filename = input("Please enter the filename of the rules database : ")
  facts_db_filename = input("Please enter the filename of the facts database : ")
  rules,facts=interfere(rules_db_filename,facts_db_filename)
  print(rules)
  print(facts)


#Main program
start()

