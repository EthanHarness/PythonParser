import sys

def program():
    global output
    global indent
    output = "<Program>\n"
    if(input_token in ["identifier", "read", "write", "$$"]):
        stmt_list()
        match("$$")
    else:
        raise Exception("Parse Error")
    output = output + "</Program>"    
    
        

def stmt_list():
    global output
    global indent
    indent = indent + "\t"
    output = output + indent + "<stmt_list>\n"
    if(input_token in ["identifier","read","write"]):
        stmt()
        stmt_list()
    elif(input_token == "$$"):
        #epsilon production
        1+1
    else:
        raise Exception("Parse Error")
    output = output + indent + "</stmt_list>\n"
    indent= indent[0:len(indent)-1]
        

def stmt():
    global output
    global indent
    indent = indent + "\t"
    output = output + indent + "<stmt>\n"
    if(input_token == "identifier"):
        match("identifier")
        match("assign")
        expr()
    elif(input_token == "read"):
        match("read")
        match("identifier")
    elif(input_token == "write"):
        match("write")
        expr()
    else:
        raise Exception("Parse Error")
    output = output + indent + "</stmt>\n"
    indent= indent[0:len(indent)-1]
        
def expr():
    global output
    global indent
    indent = indent + "\t"
    output = output + indent + "<expr>\n"
    if(input_token in ["identifier","number","lparen"]):
        term()
        term_tail()
    else:
        raise Exception("Parse Error")
    output = output + indent + "</expr>\n"
    indent= indent[0:len(indent)-1]
        
def term_tail():
    global output
    global indent
    indent = indent + "\t"
    output = output + indent + "<term_tail>\n"
    if(input_token in ["plus", "minus"]):
        add_op()
        term()
        term_tail()
    elif(input_token in ["rparen", "identifier", "read", "write", "$$"]):
        #epsilon production
        1+1
    else:
        raise Exception("Parse Error")
    output = output + indent + "</term_tail>\n"
    indent= indent[0:len(indent)-1]
        

def term():
    global output
    global indent
    indent = indent + "\t"
    output = output + indent + "<term>\n"
    if(input_token in ["identifier", "number", "lparen"]):
        factor()
        factor_tail()
    else:
        raise Exception("Parse Error")
    output = output + indent + "</term>\n"
    indent= indent[0:len(indent)-1]
        
def factor_tail():
    global output
    global indent
    indent = indent + "\t"
    output = output + indent + "<factor_tail>\n"
    if(input_token in ["times", "div"]):
        mult_op()
        factor()
        factor_tail()
        
    elif(input_token in ["plus","minus", "rparen", "identifier", "read", "write", "$$"]):
        #epsilon production
        1+1
    else:
        raise Exception("Parse Error")
    output = output + indent + "</factor_tail>\n"
    indent= indent[0:len(indent)-1]
        
def factor():
    global output
    global indent
    indent = indent + "\t"
    output = output + indent + "<factor>\n"
    if(input_token == "identifier"):
        match("identifier")
    elif(input_token == "number"):
        match("number")
    elif(input_token == "lparen"):
        match("lparen")
        expr()
        match("rparen")
    else:
        raise Exception("Parse Error")
    output = output + indent + "</factor>\n"
    indent= indent[0:len(indent)-1]
        

def add_op():
    global output
    global indent
    indent = indent + "\t"
    output = output + indent + "<add_op>\n"
    if(input_token == "plus"):
        match("plus")
    elif(input_token == "minus"):
        match("minus")
    else:
        raise Exception("Parse Error")
    output = output + indent + "</add_op>\n"
    indent= indent[0:len(indent)-1]
        
def mult_op():
    global output
    global indent
    indent = indent + "\t"
    output = output + indent + "<mult_op>\n"
    if(input_token == "times"):
        match("times")
    elif(input_token == "div"):
        match("div")
    else:
        raise Exception("Parse Error")
    output = output + indent + "</mult_op>\n"
    indent= indent[0:len(indent)-1]
        
        
def match(expected):
    global input_token
    global location
    if(input_token == expected):
        if(input_token == "$$"):
            return
        returnList = scan()
        while(returnList[0] == ''):
            if(returnList[1] == "$$"):
                returnList[0] = "$$"
            else:
                returnList = scan()
        if(returnList[1] == "$$"):
            input_token = "$$"
        else:
            input_token = returnList[0]
    else:
        raise Exception("Parse Error")
        
        
def scan():
  global location
  global fileStream
  tok = ""
  cur_char = ""
  image = ""
  remembered_chars = []
  cur_state = 0

  #repeat
  while(True):
    image = ""
    remembered_state = 0
    while(location < len(fileStream)):
      cur_char = fileStream[location]
      location = location + 1
  
      #Not at final state
      if(newStateTable[cur_state][getState(cur_char)] != -1):
        #Move
        if(tokenTab[cur_state] != 0):
          remembered_state = cur_state
          remembered_chars = []
        remembered_chars.append(cur_char)
        cur_state = newStateTable[cur_state][getState(cur_char)]
  
      #Recognize
      elif(tokenTab[cur_state] != 0):
        tok = tokenTab[cur_state]
        location = location - 1
        cur_char = fileStream[location]
        break
        
      #Error
      else:
        if(remembered_state != 0):
          tok = tokenTab[remembered_state]
          location = location - len(remembered_chars)
          image = image[0:len(image)-len(remembered_chars)]
          remembered_chars = ""
          break
        elif(cur_char == "$$"):
            1+1
        else:
          raise Exception("Scan Error")
      image += cur_char

    if (tok == "white_space" or tok == "comment"):
      #location += 1
      tok = ""
      break
    if (tok != "white_space" and tok != "comment"):
      break
  
  for i in keywordTab:
    if (image == i[0]):
      tok = i[1]
      break
  return [tok, image, location]




def getState(char):
  if(char == " " or char == "\t"):
      return 0
  elif(char == "\n"):
      return 1
  elif(char == "/"):
      return 2
  elif(char == "*"):
      return 3
  elif(char == "("):
      return 4
  elif(char == ")"):
      return 5
  elif(char == "+"):
      return 6
  elif(char == "-"):
      return 7
  elif(char == ":"):
      return 8
  elif(char == "="):
      return 9
  elif(char == "."):
      return 10
  elif(char.isdigit()):
      return 11
  elif(char.isalpha()):
      return 12
  else:
      return 13
  
        

newStateTable = [[],[],[],[],[],[],[],[],[],
             [],[],[],[],[],[],[],[],[]]
newStateTable[0] = [16,16,1,9,5,6,7,8,10,-1,12,13,15,-1] 
newStateTable[1] = [-1,-1,2,3,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1] #final state div
newStateTable[2] = [2,17,2,2,2,2,2,2,2,2,2,2,2,2]
newStateTable[3] = [3,3,3,4,3,3,3,3,3,3,3,3,3,3]
newStateTable[4] = [3,3,17,4,3,3,3,3,3,3,3,3,3,3]
newStateTable[5] = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1] #final state lparen
newStateTable[6] = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1] #final state rparen
newStateTable[7] = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1] #final state plus
newStateTable[8] = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1] #final state minus
newStateTable[9] = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1] #final state times
newStateTable[10] = [-1,-1,-1,-1,-1,-1,-1,-1,-1,11,-1,-1,-1,-1]
newStateTable[11] = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1] #final state assign
newStateTable[12] = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,14,-1,-1]
newStateTable[13] = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,14,13,-1,-1] #final state number
newStateTable[14] = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,14,-1,-1] #final state number
newStateTable[15] = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,15,15,-1] #final state identifier
newStateTable[16] = [16,16,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1] #final state white_space
newStateTable[17] = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1] #final state comment

#TokenTab = 0 indicates there is an error. Any other value indicates you are at final state
tokenTab = [0,"div",0,0,0,"lparen","rparen","plus","minus","times",0,"assign", 0,"number","number","identifier","white_space","comment"]
keywordTab = [["read","read"],["write","write"]]

global input_t
input_token = ""
global fileStream
fileStream = []
global location
location = 0
global output
output = ""
global indent
indent = ""

file = open(sys.argv[1], 'r')
while True:
    # read by character
    char = file.read(1)
    if not char:
        break
    fileStream.append(char)
        
fileStream.append(" ")
fileStream.append("$$")
    
#get the first token
input_token = (scan())[0]

try:
    program()
    print(output)
except:
    print("Dose not work")
