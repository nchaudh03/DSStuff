import re
def clean_str(string):
    string = string.strip().lower()

    #Word Replacements
    string = re.sub("word", "newword" , string)  
    string = re.sub("word 2", "new word 2" , string)  

    #String Cleaning
    string = re.sub(r"\n", " ", string)
    string = re.sub(r"\r", " ", string)
    string = re.sub(r"[0-9]", " ", string)
    string = re.sub(r"\'", " ", string)
    string = re.sub(r"\"", " ", string)
    string = re.sub(r"/", " ", string)
    string = re.sub(r"#", " ", string)
    string = re.sub(r",", " ", string)
    string = re.sub(r"-", " ", string)
    string = re.sub(r"\.", " ", string)
    string = re.sub(r"!", " ", string)
    string = re.sub(r" looking ", " ", string) 
    string = re.sub(r" like ", " ", string)
    string = re.sub(r" https: ", " ", string) #web
    string = re.sub(r" com ", " ", string) #web
    string = re.sub(r" www ", " ", string) #web
    string = re.sub(r" email ", " ", string) #web
    return string.strip()