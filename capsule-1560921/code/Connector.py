def get_data(data):
    return data[data.find("{") + 1:data.find("}")]
    return data


def create_order(sorted_latex):
    i = 0
    cur_min = 0
    cur_max = 0
    lst = []
    while i < len(sorted_latex):
        cur_min, cur_max = sorted_latex[i][0]
        parent = sorted_latex[i]
        children = []
        while i+1 < len(sorted_latex):
            min, max = sorted_latex[i+1][0]
            if min > cur_min and max < cur_max:
                children.append(sorted_latex[i+1])
                i+=1
            else:
                break
        lst.append({"parent": parent, "children":create_order(children)})
        i+=1

    return lst




def objectify(obj, lines,pdf_parsing):
    parent = obj["parent"]
    children = obj["children"]
    if isinstance(parent[1], tuple):
        if isinstance(parent[1][1], dict):  # par
            type = "par"
            paragraphs = parent[1][1]
        else:  # picture
            type = "pic"
            caption = parent[1][2]
    else:  # table/definition...
        type = "else"
    pass

def recurs(hirar, lines):
    parpar2 = []
    for i in range(len(hirar)):

        obj = hirar[i]
        parent = obj["parent"]
        children = obj["children"]
        paragraphs = {}

        if isinstance(parent[1], tuple):
            # print(parent[1][1])
            if isinstance(parent[1][1], dict):  # par
                # print(parent[1][0])
                type = "par"
                paragraphs = parent[1][1]
            else:  # picture
                type = "pic"
                caption = parent[1][2]
        else:  # table/definition...
            type = "else"
        if type == "par":
            for par in paragraphs:
                size = paragraphs[par]
                lns = lines[size[0]:size[1]]
                liine_koin = ''.join(lns)
                parpar2.append([liine_koin, size])
        for child in children:
            parpar2.extend(recurs([child],lines))
    return parpar2


def removeDoubles(res):
    lst = []
    for i in range(len(res)):
        same = False
        for j in range(i,len(res)):
            if i != j:
                if res[i][1] == res[j][1]:
                    same = True
        if same == False:
            lst.append(res[i])

    return lst


def read_first(lines, sorted_latex):
    first_line_object=min(sorted_latex[0][0][0],len(lines)-1)
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
                res.append([helper_str,[from_index,to_index+1]])
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


def connect(latex_parsing, lines):
    sorted_latex = sorted(latex_parsing.items(), key=lambda x: x[0][0])

    hirar = create_order(sorted_latex)
    # first_res = read_first(lines,sorted_latex)
    res = recurs(hirar, lines)

    res = removeDoubles(res)
    # first_res.extend(res)
    # res=first_res
    return res,sorted_latex[0][0][0]




