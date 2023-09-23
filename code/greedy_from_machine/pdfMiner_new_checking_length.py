from pathlib import Path
from typing import Iterable, Any

from pdfminer.high_level import extract_pages

a = {}
def show_ltitem_hierarchy(o: Any,page,page_num, depth=0):
    """Show location and text of LTItem and all its descendants"""

    x = get_indented_name(o, depth).strip()
    # print(type(x))
    # print(x)
    # print(x == "LTTextBoxHorizontal")
    if(x == "LTTextLineHorizontal"):
        #if(len(get_optional_text(o)) > 60):
        if(not get_optional_text(o).startswith("Copyright © 2022,")):
            a[page_num].append((get_optional_text(o),get_optional_bbox(o,page)))
        # print(
        #     f'{get_indented_name(o, depth):<30.30s} '
        #     f'{get_optional_bbox(o,page)} '

        #     f'{get_optional_text(o)}'
        # )

    if isinstance(o, Iterable):
        for i in o:
            show_ltitem_hierarchy(i,page,page_num, depth=depth + 1)


def get_indented_name(o: Any, depth: int) -> str:
    """Indented name of LTItem"""
    return '  ' * depth + o.__class__.__name__


def get_optional_bbox(o: Any,page) -> str:
    """Bounding box of LTItem if available, otherwise empty string"""
    if hasattr(o, 'bbox'):
        return (o.bbox[0],page.height-o.bbox[3],o.bbox[2],page.height-o.bbox[1])
        # return f'{o.bbox[0]:<4.0f} {page.height-o.bbox[3]:<4.0f} {o.bbox[2]:<4.0f} {page.height-o.bbox[1]:<4.0f}'
    return ''


def get_optional_text(o: Any) -> str:
    """Text of LTItem if available, otherwise empty string"""
    if hasattr(o, 'get_text'):
        return o.get_text().strip()
    return ''


def run(p):
    path = Path(p).expanduser()

    pages = extract_pages(path)
    pages_number=3
    try:
        for i in range(pages_number):
            a[i]=[]
            page = pages.__next__()
            show_ltitem_hierarchy(page,page, i)
    except:
        return a

    # pages.__next__()
    # pages.__next__()
    # pages.__next__()
    # pages.__next__()
    # page=pages.__next__()
    # show_ltitem_hierarchy(page,page,ans)
    return a










