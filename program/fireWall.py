import re
NUM_ALP = re.compile("^(?!\d+$)[\da-zA-Z_]+$")
def anti_xss(string:str)->str:
    new_str = ""
    for i in string:
        if i == '&':
            i = '&amp;'
        elif i == '<':
            i = '&lt;'
        elif i == '>':
            i = '&gt;'
        new_str+=i
    return new_str

def anti_sql(password:str) -> bool: #only can use num + alph
    if NUM_ALP.search(password):
        return True
    return False

a = "123132dsfsd123"
print(anti_sql(a))
print(type("1111"))