import heapq

def add(s):
    return s + chr(ord('A') + len(s))

def swap(s):
    return s[1] + s[0] + s[2:]

def rotate(s):
    return s[1:] + s[0]

def find_min_operations(letter_display): # returns (mininimum number of operations to create the letter display, number of ways to achieve this minimum)
    arr = [(0, '')]
    heapq.heapify(arr)
    seen = {}
    count = {(0, ''): 1}

    def add_to_arr(num_operations, s, c):
        if s not in seen:
            seen[s] = num_operations
            count[(num_operations, s)] = c
            heapq.heappush(arr, (num_operations, s))
        else:
            if num_operations == seen[s]:
                count[(num_operations, s)] += c
            
    num_operations, string = 0, ''
    while True:
        (num_operations, string) = heapq.heappop(arr)
        if string == letter_display: break
        if len(string) < len(letter_display):
            add_to_arr(num_operations + 1, add(string), count[(num_operations, string)])
        if len(string) >= 2:
            add_to_arr(num_operations + 1, swap(string), count[(num_operations, string)])
        if len(string) >= 2:
            add_to_arr(num_operations + 1, rotate(string), count[(num_operations, string)])
    return num_operations, count[(num_operations, string)]

# question 3a
print(find_min_operations('ACBD')[0])

# question 3b
from itertools import permutations
for p in map(''.join, permutations('ABCDE')):
    if find_min_operations(p)[0] == 6: print(p)

# questions 3c
print(find_min_operations('HGFEDCBA'))

# more
print(find_min_operations('HAGBDFEC'))