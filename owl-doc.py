import os, re

def should_document(p):
    return b"#@owldoc" in open(p,"rb").read(8)

def listdir(directory):
    a = []
    l = os.listdir(directory)
    for n in l:
        if os.path.isfile(directory+"/"+n) and should_document(directory+"/"+n):
            a.append(directory+"/"+n)
        elif os.path.isdir(directory+"/"+n):
            a.extend(listdir(directory+"/"+n))
    return a

def document(p):
    doc_string = ''
    variables = []
    functions = []
    others = []
    classes = []
    regex = re.compile(r"'''@.+?@'''",re.DOTALL)
    data = open(p).read()
    matches = regex.findall(data)
    for match in matches:
        content = match[4:-4]
        if content.strip().startswith(":variable") :
            variables.append(content.strip()[9:].strip())
        elif content.strip().startswith(":function") :
            functions.append(content.strip()[9:].strip())
        elif content.strip().startswith(":class"):
            classes.append(content.strip()[6:].strip())
        else:
            others.append(content.strip())

    doc_string += "# "+f+"\n"+('\n'.join(others))
    doc_string += "\n-----------------------------\n"
    doc_string += "# Variables\n"+('\n'.join(variables))
    doc_string += "\n# Functions\n"+('\n'.join(functions))
    doc_string += "\n# Classes\n"+('\n'.join(classes))
    return doc_string.replace("\t","").replace("    ","")
for f in listdir("."):
    _dname = os.path.dirname(f)
    dname = "." if _dname == "" else _dname
    if not os.path.exists("./docs/"+dname):
        os.makedirs("./docs/"+dname)
    with open("./docs/"+".".join(f.split(".")[:-1])+".md","w") as file:
        file.write(document(f))