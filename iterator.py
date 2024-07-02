from itertools import repeat, accumulate, count, islice, permutations, combinations, combinations_with_replacement

class crepeat:
    def __init__(self,item) -> None:
        self.item = item

    def __iter__(self):
        return self
    
    def __next__(self):
        return self.item

def grepeat(item):
    while True:
        yield item

#for heslo in crepeat("Python do každé rodiny"):
#    print(heslo)

for fact in islice(accumulate(count(1), lambda x,y: x*y), 10):
    print(fact)
    

seznam=[]
seznam[10:20_000] # pamětově náročné
seznam.islice(10,20_000) # použitelné bez kopie

seznam.islice(1_000_000, 1_000_010)

print([(a,b) for a in range(5) for b in "abcd"])

print(["".join(output) for output in permutations("abcd", 3)])

print(["".join(output) for output in combinations("abcd", 3)])

print(["".join(output) for output in combinations_with_replacement("abcd", 3)])
