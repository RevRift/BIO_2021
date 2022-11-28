# question 1a
def is_pat(s):
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

print("Question 1a:"); question_1a('DE', 'C'); print()

# question 1b
from itertools import permutations
def question_1b(s):
    return sum(is_pat(''.join(p)) for p in permutations(s))

print(f"Question 1b: {question_1b('ABCD')}"); print()

# question 1c
""" 
If the first letter of the whole pat is B then all the letters of the left hand pat must be before B in the alphabet
So the Left hand pat can only contain A so the left hand pat is A
the right hand pat is now a permutation of letters B to Z, let's focux on this new pat

our new pat is a permutation of the letters B-Z, but B is at the end (because we reversed the order of the previous left hand pat)
since all letters of the left hand pat must come after letters in the right hand pat, the right hand pat must be a combination of consecutive letters starting from B
but if the right hand pat had a length greater than one (i.e. if it was CB or DCB or CDB or ECDB),
the right hand pat wouldn't be a pat because reversing it gives a string starting with B,
where B is the minimum letter in the string, so you can't slice the string anywhere to make it obey the min(left hand pat) > max(right hand pat) rule
so B must be on its own as the right hand pat

this leaves the letters C-Z to handle (i.e. 24 consecutive letters of the alphabet) and they lie between B and A.             B_______A
so the variety of pats we can create comes from the number of ways we can arrange the letters C-Z to make pats
the explanation for the recurrence relation for counting this can be found at https://reasoning.page/programming/bio-2021-q1/ (not my website)
"""
from functools import lru_cache

@lru_cache
def count_pats(num_of_letters):
    if num_of_letters == 1: return 1
    return sum(count_pats(i) * count_pats(num_of_letters - i) for i in range(1, num_of_letters))

print(f'Question 1c: {count_pats(24)}'); print()