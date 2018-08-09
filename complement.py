import os
import openpyxl
import scholarly_copy as scholarly
import multiprocessing
from SpiderKit.ip_pool_foreign import IPProvider
import time
import json

path_reference = os.path.join(os.getcwd(), 'reference.xlsx')
# path_worksheet = os.path.join(os.getcwd(), 'result.xlsx')
path_result_file = os.path.join(os.getcwd(), 'result')

reference = openpyxl.load_workbook(path_reference)
sheet = reference.active

column = {
    "expert": "A",
    "affiliation": "B",
    "interests": "C",
    "email": "D",
    "phone": "E",
    "address": "F",
    "country": "G",
    "language": "H",
    "position": "I",
    "name": "J",
    "citedby": "K",
    "hindex": "L",
    "hindex5y": "M",
    "i10index": "N",
    "i10index5y": "O",
    "url_picture": "P",
}


def complement(lock, lower, upper, batch=3):
    print(lower, "~", upper)
    ipprovider = IPProvider()
    while lower < upper:
        list_result = []
        start = time.time()
        proxy = ipprovider.get_ip()
        _isIPNeedChange = False
        for i in range(lower, min(lower + batch, upper + 1)):
            if i > 5663:
                break
            if time.time() - start >= 60 or _isIPNeedChange:
                start = time.time()
                proxy = ipprovider.get_ip()
                _isIPNeedChange = False
            name = sheet[column["expert"] + str(i)].value
            name = name if name is not None else ''

            name_true = sheet[column["name"] + str(i)].value
            if name_true is not None and len(name_true) > 0:
                continue

            author = None
            max_tries = 3
            while author is None and max_tries > 0:
                try:
                    author = next(scholarly.search_author(name, proxy)).fill(proxy)
                except StopIteration:
                    print('No professor named', name, i)
                    list_result.append((str(i), '', -1, -1, -1, -1, -1, '', ''))
                    break
                except Exception as e:
                    _isIPNeedChange = True
                    print(e, name, i)
                    max_tries -= 1

            if author is None:
                list_result.append((str(i), '', -1, -1, -1, -1, -1, '', ''))
                continue

            name = author.name
            affiliation = author.affiliation
            citedby = author.citedby
            hindex = author.hindex
            hindex5y = author.hindex5y
            i10index = author.i10index
            i10index5y = author.i10index5y
            url_picture = author.url_picture

            result = (str(i), name, citedby, hindex, hindex5y, i10index, i10index5y, url_picture, affiliation)
            list_result.append(result)
            print(result)

        lock.acquire()
        try:
            with open(path_result_file, 'a', encoding='utf-8') as file:
                for r in list_result:
                    file.write(json.dumps(r) + '\n')

            # wb = openpyxl.load_workbook(path_worksheet)
            # st = wb.active
            # for item in list_result:
            #     st[column["name"] + item[0]] = item[1]
            #     st[column["citedby"] + item[0]] = item[2]
            #     st[column["hindex"] + item[0]] = item[3]
            #     st[column["hindex5y"] + item[0]] = item[4]
            #     st[column["i10index"] + item[0]] = item[5]
            #     st[column["i10index5y"] + item[0]] = item[6]
            #     st[column["url_picture"] + item[0]] = item[7]
            #     st[column["affiliation"] + item[0]] = item[8]
            #
            # wb.save(path_worksheet)

        finally:
            lock.release()

        lower = min(upper, lower + batch)


if __name__ == '__main__':
    with open(path_result_file, 'w', encoding='utf-8') as f:
        pass

    counts = 5563
    begin_no = 170  # 562~3562

    have_done = 0
    num_of_processing = 4
    quarter = counts // num_of_processing
    lock = multiprocessing.Lock()

    arg_list = [
        (lock, have_done + begin_no, begin_no + quarter),
        (lock, have_done + begin_no + quarter + 1, begin_no + quarter * 2),
        (lock, have_done + begin_no + quarter * 2 + 1, begin_no + quarter * 3),
        (lock, have_done + begin_no + quarter * 3 + 1, begin_no + quarter * 4),
        (lock, have_done + begin_no + quarter * 4 + 1, begin_no + quarter * 5),
        (lock, have_done + begin_no + quarter * 5 + 1, begin_no + quarter * 6),
    ]

    for j in range(1, num_of_processing + 1):
        process = multiprocessing.Process(target=complement, args=arg_list[j - 1])
        process.start()
        time.sleep(30)

    # lock = multiprocessing.Lock()

    # arg_list = [
    #     # (lock, 5246, 5662),
    #     (lock, 3711, 3793),
    #     (lock, 3864, 3939),
    #     (lock, 5246, 5662),
    #
    # ]
    #
    # for i in arg_list:
    #     process = multiprocessing.Process(target=complement, args=i)
    #     process.start()
