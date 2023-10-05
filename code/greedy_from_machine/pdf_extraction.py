import pdfplumber


def content(path):
    # return pdfMiner.run(path)
    return []
def pictures(path):
    dict={}
    mypdf=pdfplumber.open(path)
    for page_number in range(len(mypdf.pages)):

        plumber_page = mypdf.pages[page_number]
        images = []

        images_in_plumber_page = plumber_page.images  # pdfplumber

        for k in range(len(images_in_plumber_page)):
            img = images_in_plumber_page[k]
            images.append({"pageNumber": 0 + 1, "width": img['width'], "height": img['height'], "x0": img['x0'],
                                   "y0": plumber_page.height-img['y1'], "x1": img['x1'], "y1": plumber_page.height-img['y0']})
        dict[page_number]= images

    return dict


def tables(path):
    dict={}
    mypdf=pdfplumber.open(path)
    for page_number in range(len(mypdf.pages)):

        p0 = mypdf.pages[page_number]
        tables1=p0.find_tables(table_settings={}) #print details
        # tables2=p0.extract_tables(table_settings={}) #cells values (content of table)
        arr= {0:[]}
        for t in tables1:
            arr[0].append(t.bbox)
        dict[page_number]= arr
    return dict

def run(path):

    content_array=content(path)

    pictures_array= pictures(path)

    tables_array = tables(path)

    return {"id":path,"content":content_array,"pictures":pictures_array,"tables":tables_array}


if __name__=="__main__":

    path = '../pdf-tests/new_test.pdf'

    ans=run(path)

    for key in ans:
        if key=="content":
            for c in ans["content"]["paragraphs"]:
                print(c)
        print(str(key)+":   "+str(ans[key]))