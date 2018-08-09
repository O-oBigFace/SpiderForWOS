with open('result', 'r', encoding='utf-8') as f:
    r = f.read().replace('][', ']\n[')
    with open('result1', 'w', encoding='utf-8') as f1:
        f1.write(r)