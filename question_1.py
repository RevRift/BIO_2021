import time

def is_pat(s): # improve the time complexity of this at a later point
    if not s: return True
    if len(s) == 1: return True
    for i in range(1, len(s)): 
        # print(i, s[:i], s[i:])
        if (min(s[:i]) > max(s[i:]) and 
        is_pat(''.join(reversed(s[:i]))) and 
        is_pat(''.join(reversed(s[i:])))): return True
    return False


def question_1a(s1, s2):
    print('YES' if is_pat(s1) else 'NO')
    print('YES' if is_pat(s2) else 'NO')
    print('YES' if is_pat(s1 + s2) else 'NO')

tests = [('AB', False), ('BA', True), ('DE', False), ('ED', True), ('DEC', True), ('CEDAB', True)]
for test, exp in tests:
    print(f'is_pat({test}) = {is_pat(test)}, expected: {exp}')

more_tests = [('DE', 'C'), ('A', 'A'), ('A', 'B'), ('B', 'A'), ('AB', 'CD'), ('BEFCD', 'A'),
    ('GEA', 'DBCF'), ('EFCD', 'GAB'), ('ECBDFA', 'LKJIHG'), ('BDIGEF', 'HCA'), ('JKHGIL', 'ADFEBC')]
for a, b in more_tests:
    start_time = time.time()
    print(a, b)
    question_1a(a, b); 
    print(f'Test took {time.time() - start_time} milliseconds'); print();

from itertools import permutations
def question_1b(s):
    return sum(is_pat(''.join(p)) for p in permutations(s))

print(question_1b('ABCD'))
print(question_1b('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))