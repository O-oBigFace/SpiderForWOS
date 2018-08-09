import os
import openpyxl
import Google_complement
import multiprocessing
import time

path_reference = os.path.join(os.getcwd(), 'reference.xlsx')
path_worksheet = os.path.join(os.getcwd(), 'result.xlsx')
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
    while lower < upper:
        list_result = []
        for i in range(lower, lower + batch + 1):
            if i > 5663:
                break
            name = sheet[column["expert"] + str(i)].value
            name = name if name is not None else ''
            affiliation = sheet[column["affiliation"] + str(i)].value
            affiliation = affiliation if affiliation is not None else ''
            search = (name + ' ' + affiliation)
            print('-------------------------------------------------------')
            print(i, search)

            email = ''
            phone = ''
            address = ''
            country = ''
            language = ''
            position = ''

            # # 搜索-补全email, phone
            email, phone = Google_complement.get_email_and_phone(search)

            if len(affiliation) > 0:
                address = Google_complement.get_address(affiliation)
                country = Google_complement.get_country(affiliation)
            else:
                pass

            position = Google_complement.get_position(search)

            list_result.append((str(i), email, phone, address, country, language, position))
            print((str(i), email, phone, address, country, language, position))

        lock.acquire()
        try:
            wb = openpyxl.load_workbook(path_worksheet)
            st = wb.active
            for item in list_result:
                st[column["email"] + item[0]] = item[1]
                st[column["phone"] + item[0]] = item[2]
                st[column["address"] + item[0]] = item[3]
                st[column["country"] + item[0]] = item[4]
                st[column["language"] + item[0]] = item[5]
                st[column["position"] + item[0]] = item[6]
            wb.save(path_worksheet)
        finally:
            lock.release()

        lower = min(upper, lower + batch + 1)


if __name__ == '__main__':
    counts = 690 - 582
    begin_no = 582  # 562~3562

    have_done = 0
    num_of_processing = 1
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

    for i in range(1, num_of_processing + 1):
        process = multiprocessing.Process(target=complement, args=arg_list[i - 1])
        process.start()

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
