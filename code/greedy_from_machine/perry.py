import regex

import latex_parsing_perry
import Connector_perry
import re

def remove_comments(doc):
    new_doc=[]
    begin_document_found=False
    for line in doc:
        if not begin_document_found:
            if line.startswith("\\begin{document}"):
                begin_document_found=True
            continue
        if line.find("%")!= -1:
            for char in line:
                if char==" ":
                    continue
                if char=="%":
                    break

                new_doc.append(line)
                break
        else:
            new_doc.append(line)
    return new_doc

def remove_unnecessary_stuff(doc): #working insane
    new_doc = []
    begin_document_found = False
    title_found = False
    for line in doc:
        if title_found == False and line.startswith("\\title"): ################################## adding title ###########################################
            new_doc.append(line)
            title_found = True
        if not begin_document_found:
            if line.startswith("\\begin{document}"):
                begin_document_found = True
            continue
        if line.find("%") != -1 and line.find("%") < line.find("\n"): #if we have a comment in the line
            new_line = ""
            for charindex in range(len(line)):
                if line[charindex] == "%" and line[charindex-1] == "\\":
                    new_line = line
                    break
                if line[charindex] == "%":
                    break

                new_line += line[charindex]
            new_doc.append(new_line)
        else:
            new_doc.append(line)
    return new_doc

def read_file(document_path):
    with open(document_path, encoding='UTF-8') as file:
        # doc = file.read()
        doc = [line for line in file]
    # return doc
    new_doc=remove_unnecessary_stuff(doc)
    return new_doc

def get_operators():
    # return ["\\section","\\begin{table}","\\end{table}",
    #         "\\begin{figure}","\\end{figure}","\\begin{abstract}",
    #         "\\end{abstract}","\\title","\\[","\\prob","\\begin{definition}",
    #         "\\end{definition}","\\begin{itemize}","\\end{itemize}","\\begin{equation}","\\end{equation}"]
    return ["\\section","\\begin{table}","\\end{table}",
            "\\begin{figure}","\\end{figure}","\\begin{abstract}",
            "\\end{abstract}","\\title","\\[","\\prob","\\begin{definition}",
            "\\end{definition}","\\begin{itemize}","\\end{itemize}","\\subsection",
            "\\begin{cases}","\\end{cases}","\\begin{subfigure}","\\end{subfigure}",
            "\\subsubsection","\\begin{enumerate}","\\end{enumerate}","\\item","\\noindent","\\end{equation}","\\begin{equation}"]

def get_objects():
    # return ["\\section","\\begin{table}","\\end{table}",
    #         "\\begin{figure}","\\end{figure}","\\begin{abstract}",
    #         "\\end{abstract}","\\title","\\[","\\prob","\\begin{definition}",
    #         "\\end{definition}","\\begin{itemize}","\\end{itemize}","\\begin{equation}","\\end{equation}"]
    return ["\\section","\\end{table}",
            "\\end{figure}","\\end{abstract}",
            "\\title","\\[","\\prob","\\end{definition}",
            "\\end{itemize}","\\subsection",
            "\\end{cases}","\\end{subfigure}",
            "\\subsubsection","\\end{enumerate}","\\item","\\noindent","\\end{equation}"]

def get_begins():
    return {
        "abstract":0,
        "figure":0,
        "vmatrix":0,
        "enumerate":0,
        "definition":0,
        "equation":0,
        "cases":0,
        "subfigure":0,
        "algorithmic":0,
        "algorithm":0,
        "section":0,
        "subsection":1,
        "subsubsection":0,
        "formula":0,
        "paragraph":0,
        "table":0
    }


def set_scope(new_line):
    if new_line == "abstract":
        return "abstract"
    if new_line == "subfigure":
        return "subfigure"
    if new_line == "figure":
        return "figure"
    if new_line == "algorithm":
        return "algorithm"
    if new_line == "abstract":
        return "abstract"
    if new_line == "abstract":
        return "abstract"
    if new_line == "abstract":
        return "abstract"
    if new_line == "abstract":
        return "abstract"
    if new_line == "abstract":
        return "abstract"
    if new_line=="table":
        return "table"
    if new_line=="paragraph":
        return "paragraph"


def receive_lines_version_1(lines):
    begins=get_begins()
    order = []
    scope = ""
    i = -1
    for line in lines:
        new_line = line.lstrip(" ")
        i += 1
        #print(new_line)

        if new_line.startswith("\\begin") or new_line.startswith("$\\begin"):

            definition_line =new_line[new_line.find("}")+1:].lstrip(" ")
            original_line = new_line
            new_line = new_line.split("{")[1].split("}")[0]

            if begins.get(new_line,-1) != -1:
                if new_line == "enumerate" or new_line == "cases":
                    continue
                if new_line == "table":
                    addings=""
                    if original_line.find("[")!=-1:
                        addings=original_line.split("[")[1].split("]")[0]

                    order.append([new_line, ("Table", str(begins[new_line]),addings), i])
                    begins[new_line] +=1
                    scope = set_scope(new_line)
                    continue
                if new_line == "subfigure":
                    begins[new_line] += 1
                    if order[-1][0] == "figure":
                        begins["figure"] -= 1
                        order.pop()
                    addings=""
                    if original_line.find("[")!=-1:
                        addings=original_line.split("[")[1].split("]")[0]
                    order.append([new_line, ("Figure", str(begins[new_line] + begins["figure"]),addings), i])
                    scope = set_scope(new_line)
                    continue
                if scope == "algorithm" and new_line == "algorithmic":
                    continue
                begins[new_line] +=1
                if new_line == "abstract":
                    order.append([new_line, ("AbstractSection", "","",""), ("AbstractSection", new_line[0].upper() + new_line[1:]), i])
                    scope = set_scope(new_line)
                    continue
                if new_line == "figure":
                    addings=""
                    if original_line.find("[")!=-1:
                        addings=original_line.split("[")[1].split("]")[0]

                    order.append([new_line, ("Figure", str(begins["figure"] + begins["subfigure"]),addings), i])
                    scope = set_scope(new_line)
                    continue
                if new_line == "vmatrix":
                    order.append([new_line, ("Matrix", str(begins["vmatrix"]),"",new_line), i])
                    scope = set_scope(new_line)
                    continue
                if new_line == "equation":
                    begins["formula"] += 1
                    order.append(["formula", ("Formula", str(begins["formula"]),"",new_line), i])
                    scope = set_scope(new_line)
                    continue
                if new_line == "definition":

                    order.append([new_line, ("Definition", definition_line[:40], definition_line[-40:-1],definition_line.replace("\n", " ")), ("Definition", "Definition "+ definition_line[:40], definition_line[-40:-1]), i])
                    scope = set_scope(new_line)
                    continue
                if new_line == "algorithmic" or new_line == "algorithm":
                    addings=""
                    if original_line.find("[")!=-1:
                        addings=original_line.split("[")[1].split("]")[0]

                    order.append([new_line, ("Algorithm", str(begins["algorithmic"] + begins["algorithm"]),addings), i])
                    scope = set_scope(new_line)
                    continue
                order.append([new_line, begins[new_line], i])
                scope = set_scope(new_line)
                continue
        elif new_line.startswith("\\caption"):
            brace_count = new_line.count("{") - new_line.count("}")
            caption_index = i + 1
            while brace_count > 0:
                new_line += lines[caption_index]
                brace_count = new_line.count("{") - new_line.count("}")
                caption_index +=1
            if scope == "algorithm":
                continue
            elif scope=="figure":
                new_line = "Figure" + new_line.split("{", 1)[1].rsplit("}", 1)[0]
                order.append([new_line, ("CaptionFigure", new_line[:40], new_line[-40:-1],new_line.replace("\n", " ")),
                                ("CaptionFigure", "Figure " + new_line[:40], new_line[-40:-1]), i])
            elif scope=="table":
                new_line = "Table" + new_line.split("{", 1)[1].rsplit("}", 1)[0]
                order.append([new_line, ("CaptionTable", new_line[:40], new_line[-40:-1],new_line.replace("\n", " ")),
                                ("CaptionTable", "Table " + new_line[:40], new_line[-40:-1]), i])
            elif scope=="subfigure":
                new_line = "Figure" + new_line.split("{", 1)[1].rsplit("}", 1)[0]
                order.append([new_line, ("CaptionFigure", new_line[:40], new_line[-40:-1], new_line.replace("\n", " ")),
                                ("CaptionFigure", "Figure " + new_line[:40], new_line[-40:-1]), i]) 
        if new_line.startswith("\\item"):
            new_line = new_line[6:]
            order.append([new_line[:30], ("Enum",new_line[:40],new_line[-40:-1],new_line.replace("\n", " ")), ("Enum",new_line[:40],new_line[-40:-1]),i])
        if new_line.startswith("\\["):
            begins["formula"] += 1
            order.append(["formula", ("Formula", str(begins["formula"]),"",new_line),i])
        if new_line.startswith("\\section"):
            begins["section"] += 1
            new_line = new_line.split("{")[1].split("}")[0]
            begins["subsection"] = 1
            order.append([str(begins["section"]) + " " + new_line, ("Section", new_line,new_line,new_line),("Section", new_line,new_line), i])
        if new_line.startswith("\\subsection"):
            new_line = new_line.split("{")[1].split("}")[0]
            order.append([str(begins["section"]) + "." + str(begins["subsection"]) + " " + new_line, ("SubSection",new_line,new_line,new_line), ("SubSection",new_line,new_line), i])
            begins["subsection"] += 1

        if new_line.startswith("\\subsubsection"):
            new_line = new_line.split("{")[1].split("}")[0]
            order.append([str(begins["section"]) + "." + str(begins["subsection"]) + " " + new_line,
                          ("Subsubsection", new_line, new_line, new_line), ("Subsubsection", new_line, new_line), i])
            begins["subsubsection"] += 1
        if new_line.startswith("\\paragraph"):
            scope = set_scope(new_line)
            new_line = new_line.split("{")[1].split("}")[0]
            order.append([new_line, ("Paragraph",new_line,new_line,new_line), ("Paragraph",new_line,new_line), i])
            begins["paragraph"] += 1

        if new_line.startswith("\\title"):
            new_line = new_line.split("{")[1].split("}")[0]
            order.append([new_line, ("Title", new_line,new_line,new_line) ,("Title", new_line),i])
        # if scope == "abstract" and new_line != "":
        #     order.append([new_line[:30], ("AbstractPar",new_line[:30],new_line[-30:-1]), i])
        #     scope = ""
    return order


def combine(order, result11):

    for i in result11:
        rng = i[1]
        chosen=0
        definition_flag = False
        for j in range(len(order)):
            if type(order[j][-1]) == list:
                if rng[0] >= order[j][-1][0]:
                    chosen = j
                else:
                    break
            else:
                if rng[0] >= order[j][-1]:
                    chosen = j
                else:
                    break
        i[0] = i[0].strip().strip("\n")
        if order[chosen][1][0] == "Definition":
            if i[0].find(order[chosen][1][2][-20:-1]) != -1:
                popped = order.pop(chosen)
                definition_flag = True

        if definition_flag == True:
            removed_definition="Definition"+i[0].split("begin{paragraph}")[1].replace("\n", "")
            order.insert(chosen ,[removed_definition[:40],
                                  ("Definition", removed_definition[:40].replace("\n", " "),
                                   removed_definition[-40:-1].replace("\n", " "),removed_definition.replace("\n", " ")),
                                  ("Definition", removed_definition[:40].replace("\n", " "),
                                   removed_definition[-40:-1].replace("\n", " ")),
                                  i[1]])
        elif definition_flag == False and i[0] != "definition":
            order.insert(chosen + 1,
                         [i[0][:40], ("Par", i[0][:40].replace("\n", " "), i[0][-40:-1].replace("\n", " "),i[0].replace("\n", " ")), ("Par", i[0][:40].replace("\n", " "), i[0][-40:-1].replace("\n", " ")), i[1]])
    return order


def createTags(combined_res):
    lst = []
    current_par=True
    lne=""
    lne_number=0
    for i in combined_res:

        if i[1][0]==("Paragraph"):
            current_par=True
            lne=i[1][1]
            lne_number=i[3]
            # lst.append((i[1],i[3]))

        elif i[1][0]==("Par"):
            if current_par==True:
                helper=list(i[1])
                helper[0]="Paragraph"
                helper[1]=lne+" "+helper[1]
                helper[3]=lne+" "+helper[3]
                linearr=i[3]
                linearr[0]=lne_number
                lst.append((tuple(helper), linearr))
                current_par=False
            else:
                lst.append((i[1], i[3]))
        elif i[1][0].startswith("Caption"):
            lst.append((i[1], i[3]))
            current_par=False
        else:
            lst.append((i[1], i[2]))
            current_par=False

    return lst


def createLinesToSearch(combined_res):
    lst = []
    current_par = True
    lne = ""
    for i in combined_res:
        if len(i) >=2:
            if type(i[2]) == tuple:
                if i[2][0] == ("Paragraph"):
                    current_par = True
                    lne = i[2][1]
                    # lst.append((i[1],i[3]))

                elif i[2][0] == ("Par"):
                    if current_par == True:
                        helper = list(i[2])
                        helper[0] = "Paragraph"
                        helper[1] = lne + " " + helper[1]
                        lst.append(tuple(helper))
                        current_par = False
                    else:
                        lst.append(i[2])
                else:
                    current_par = False
                    lst.append(i[2])
    lst.append(("END", "END", "END"))
    return lst

def read_first(lines, first_object_location):
    first_line_object=min(first_object_location,len(lines)-1)
    res=[]
    from_index=0
    to_index=0
    current_paragraph=False
    helper_str=""
    for i in range(0,first_line_object):
        line=lines[i]
        if line=="\n":
            if current_paragraph==False:
                continue
            else:
                # order.insert(chosen + 1,
                #              [i[0][:40], ("Par", i[0][:40].replace("\n", " "), i[0][-40:-1].replace("\n", " "),
                #                           i[0].replace("\n", " ")),
                #               ("Par", i[0][:40].replace("\n", " "), i[0][-40:-1].replace("\n", " ")), i[1]])

                res.append([helper_str[:40],('Par',helper_str[:30].replace("\n", " "),helper_str[-30:-1].replace("\n", " "),helper_str.replace("\n", " ")),
                           ('Par',helper_str[:30].replace("\n", " "),helper_str[-30:-1].replace("\n", " "),helper_str.replace("\n", " ")),helper_str])
                from_index=0
                to_index=0
                helper_str = ""
                current_paragraph=False
        else:
            if current_paragraph==False:
                from_index=i
                to_index=i
                current_paragraph=True
                helper_str=line
            else:
                to_index+=1
                helper_str+=line

    return res


def parse(path, lines= None):
    if lines != None:
        file = lines
    else:
        file = read_file(path)
    # title=False
    # if file[0].startswith("\\title"):
    #     title=True
    # if title==False:
    file.insert(0,"\\section{demo}")
    order = receive_lines_version_1(file)
    latex, tree, lines = latex_parsing_perry.parse(lines)
    result11,first_object_location = Connector_perry.connect(latex, lines)
    combined_res = combine(order,result11)
    # first_res = read_first(lines,first_object_location)
    # first_res.extend(combined_res)
    # combined_res=first_res
    create_tag = createTags(combined_res)[1:]
    create_lines_to_search = createLinesToSearch(combined_res)[1:]



    return create_tag, create_lines_to_search


