from collections import deque
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
    for line in doc:
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

def receive_lines_version_1(lines):
    i=1
    parsing_tree={}
    operators=get_operators()
    objects=get_objects()
    for ob in objects:
        parsing_tree[ob]=[]

    brackets_list=["begin","end"]
    no_brackets_list=["\\[","\\item","\\noindent","\\section","\\subsection","\\subsubsection"]
    stack = deque()
    section_stack=deque()
    equation_list=-1
    new_dict={}
    for line in lines:
        str_line = str(line)

        if str_line.startswith(f"\\"):

            if str_line.find(f"\\begin") != -1:
                op = str_line.split("}")[0] + "}"
                if op in operators:
                    if str_line.startswith("\\begin{definition}"):
                        stack.append((i-1,op))
                    else:
                        stack.append((i,op))



            if str_line.find(f"\\end") != -1:
                op = str_line.split("}")[0] + "}"
                if op in operators:
                    obj = stack.pop()
                    parsing_tree[op].append((obj[0],i))
                    new_dict[obj[0]]=(i,op)

            if str_line.startswith("\\section") or str_line.startswith("\\subsection") or  str_line.find("\\subsubsection") != -1 :
                op = str_line.split("{")[0]
                if section_stack:
                    obj = section_stack.pop()
                    parsing_tree[obj[1]].append((obj[0], i-1))
                    new_dict[obj[0]]=(i-1,obj[1])

                section_stack.append((i, op))

            # for item in no_brackets_list:
            #     if str_line.find(item)!=-1:
            #         parsing_tree[item].append(i)
            #         break
        if str_line.startswith("\\["):
            if str_line.find("\\]") !=-1:
                parsing_tree["\\["].append((i,i))
                new_dict[i] = (i, "\\[")

            else:
                equation_list=i
        else:
            if str_line.find("\\]") != -1:
                if equation_list!=-1:
                    parsing_tree["\\["].append((equation_list, i))
                    new_dict[equation_list] = (i, "\\[")
                    equation_list=-1

        i+=1
    if section_stack:
        obj = section_stack.pop()
        parsing_tree[obj[1]].append((obj[0], i - 2))
        new_dict[obj[0]]=(i-2,obj[1])

    return parsing_tree,new_dict


def get_definition_par(lines, line_number, count):
    counter = {}
    is_in_begin = 0
    doneFlag = False
    firstTimeFlag = True
    original_Line_Number = line_number
    while not lines[line_number].startswith("\\end{definition}"):
        if lines[line_number].startswith("\\begin") or lines[line_number].startswith("$\\begin"):
            if firstTimeFlag == True:
                counter[count] = [line_number]
                line_number += 1
                firstTimeFlag = False
                continue
            if len(counter[count]) == 1:
                counter[count].append(line_number)
                doneFlag = True
            is_in_begin += 1
            line_number += 1
            continue
        if line_number == original_Line_Number+1 and lines[line_number].startswith("\\"):
            counter[count].append(line_number)
            doneFlag = True
            line_number += 1
            count+=1
            continue

        if is_in_begin > 0:
            if lines[line_number].startswith("\\end"):
                is_in_begin -= 1
                line_number += 1
                continue
            else:
                line_number += 1
                continue
        else:
            if not lines[line_number].startswith("\\"):
                if doneFlag == True:
                    doneFlag=False
                    count += 1
                    counter[count]=[line_number]
                line_number += 1
                continue
            else:
                counter[count].append(line_number)
                count+=1

        line_number+=1
    if counter.get(count,-1) != -1:
        counter[count].append(line_number)
    new_counter={}
    for tup in counter:
        if counter[tup][1]- counter[tup][0]==1:
            continue
        else:
            new_counter[tup]= counter[tup]
    return count, new_counter


def count_paragraphs(lines,ans,new_dict):


    sections=ans["\\section"]+ans["\\subsection"]+ans["\\subsubsection"]+ans["\\end{abstract}"]+ans["\\end{definition}"]
    flow={}
    for section in sections:
        counter={}
        count = 0
        flag=False
        is_in_begin = 0
        par_start = 0
        definition_flag = False
        for line_number in range(section[0],section[1]+1):
            str_line = str(lines[line_number])
            if str_line.startswith("\\begin") or str_line.startswith("$\\begin"):
                if str_line.startswith("\\begin{definition}"):
                    count_def, counter_def = get_definition_par(lines, line_number, count+1)
                    count = count_def
                    counter.update(counter_def)
                if flag:
                    counter[count].append(line_number)
                    flag=False
                is_in_begin+=1
                continue
            if is_in_begin>0:
                if str_line.startswith("\\end"):
                    is_in_begin-=1
                else:
                    continue

            if str_line.startswith("\\alg\\") or str_line.startswith("\\noindent") or (not str_line.startswith(f"\\")) or str_line.startswith(f"\\citeauthor") :
                if flag == False and not (str_line.isspace()):
                    count += 1
                    counter[count] = [line_number]
                    flag = True
                if flag == True and not (str_line.isspace()):
                    continue

                if flag and (str_line.isspace()):
                    counter[count].append(line_number)
                    flag = False

        flow[section]=(str(lines[section[0]-1]),counter)
    return flow

def objects(lines,ans,new_dict,type):
    objects=ans[type]
    if type=="\\end{figure}":
        for object in objects:
            found_caption=False
            for line_number in range(object[0], object[1] + 1):
                str_line = str(lines[line_number])
                if str_line.find("\\caption")!=-1:
                    index = str_line.find("{")
                    s = str_line[index:]
                    new_dict[object]=(type,True,s)
                    found_caption=True
                    break
            if not found_caption:
                new_dict[object] = (type, False, "")
    else:
        for object in objects:
            if (new_dict.get(object,0) != 0):
                new_dict[object] = (type, new_dict[object][1])
                continue
            new_dict[object] = (type)
    return new_dict


def parse(lines):
    file = lines

    parsing_tree,lines_dict=receive_lines_version_1(file)

    new_dict = count_paragraphs(file,parsing_tree, lines_dict)

    object_list=["\\end{table}",
            "\\end{figure}",
            "\\title","\\[","\\prob","\\end{definition}",
            "\\end{itemize}",
            "\\end{cases}","\\end{subfigure}",
            "\\end{enumerate}","\\item","\\end{equation}"]

    for obj in object_list:
        new_dict=objects(file,parsing_tree,new_dict,obj)
    return new_dict, parsing_tree, file

