Let's talk about binary numbers. We have an -digit binary number, , and we denote the digit at index  (zero-indexed from right to left) to be . We can find the decimal value of  using the following formula:
For example, if binary number , we compute its decimal value like so:
Meanwhile, in our well-known decimal number system where each digit ranges from  to , the value of some decimal number, , can be expanded in the same way:
Now that we've discussed both systems, let's combine decimal and binary numbers in a new system we call decibinary! In this number system, each digit ranges from  to  (like the decimal number system), but the place value of each digit corresponds to the one in the binary number system. For example, the decibinary number  represents the decimal number because:
Pretty cool system, right? Unfortunately, there's a problem: two different decibinary numbers can evaluate to the same decimal value! For example, the decibinary number  also evaluates to the decimal value :
This is a major problem because our new number system has no real applications beyond this challenge!
Consider an infinite list of non-negative decibinary numbers that is sorted according to the following rules:
The decibinary numbers are sorted in increasing order of the decimal value that they evaluate to.
Any two decibinary numbers that evaluate to the same decimal value are ordered by increasing decimal value, meaning the equivalent decibinary values are strictly interpreted and compared as decimal values and the smaller decimal value is ordered first. For example,  and  both evaluate to . We would order  before  because .
Here is a list of first few decibinary numbers properly ordered:
image
You will be given  queries in the form of an integer, . For each , find and print the the  decibinary number in the list on a new line.
Function Description
Complete the decibinaryNumbers function in the editor below. For each query, it should return the decibinary number at that one-based index.
decibinaryNumbers has the following parameter(s):
x: the index of the decibinary number to return
Input Format
The first line contains an integer, , the number of queries.
Each of the next  lines contains an integer, , describing a query.
Constraints
Subtasks
 for  of the maximum score
 for  of the maximum score
 for  of the maximum score
Output Format
For each query, print a single integer denoting the the  decibinary number in the list. Note that this must be the actual decibinary number and not its decimal value. Use 1-based indexing.
Sample Input 0
5
1
2
3
4
10
Sample Output 0
0
1
2
10
100
Explanation 0
For each , we print the  decibinary number on a new line. See the figure in the problem statement.
Sample Input 1
7
8
23
19
16
26
7
6
Sample Output 1
12
23
102
14
111
4
11
Sample Input 2
10
19
25
6
8
20
10
27
24
30
11
Sample Output 2
102
103
11
12
110
100
8
31
32
5
"""

# !/bin/python3

import math
import os
import random
import re
import sys
import bisect
import array
import timeit
from itertools import repeat


def decbinValue(x):
    ans = 0
    p2 = 1
    while x > 0:
        ans += (x % 10) * p2
        p2 *= 2
        x //= 10
    return ans


class Solution:
    def __init__(self):
        self.nrepr = {0: 1, 1: 1, 2: 2, 3: 2}
        self.ndrepr = {(0, 0): 1}
        # self.initSimple()
        self.init()
        # self.test()
        # self.speedTest()

    def numRepr(self, n):
        if n in self.nrepr:
            return self.nrepr[n]
        ans = 0
        for i in range(10):
            if n - i >= 0 and (n - i) % 2 == 0:
                ans += self.numRepr((n - i) // 2)
        self.nrepr[n] = ans
        return ans

    def numFixR(self, n, d):
        if (n, d) in self.ndrepr:
            return self.ndrepr[(n, d)]
        if d == 0 and n > 0:
            return 0
        if n > (2 ** d - 1) * 9:
            return 0
        ans = 0
        for i in range(10):
            if n - i >= 0 and (n - i) % 2 == 0:
                ans += self.numFixR((n - i) // 2, d - 1)
        self.ndrepr[(n, d)] = ans
        return ans

    def test(self):
        print(10 ** 16)
        print(self.numRepr(100000))
        print(self.numRepr(100))
        start = timeit.default_timer()
        self.decibinaryNumbers(10 ** 16)
        stop = timeit.default_timer()
        self.decibinaryNumbers(10 ** 16)
        stop2 = timeit.default_timer()
        print(self.decibinaryNumbers(10 ** 16))
        print('Time 1st: ', stop - start, '2nd:', stop2 - stop)
        for d in range(1, 35000):
            if str(self.decibinaryNumbersSimple(d)) != self.decibinaryNumbers(d):
                print("Yoop", d, self.decibinaryNumbersSimple(d), self.decibinaryNumbers(d))
                break
        a = array.array('q', [1, 10 ** 8, 10 ** 15, 10 ** 16])
        print(a, a.itemsize)

    def speedTest(self):
        print(10 ** 16)
        print(self.numRepr(100000))
        print(self.numRepr(100))
        start = timeit.default_timer()
        self.decibinaryNumbers(10 ** 16)
        stop = timeit.default_timer()
        self.decibinaryNumbers(10 ** 16)
        stop2 = timeit.default_timer()
        print(self.decibinaryNumbers(10 ** 16))
        print('Time 1st: ', stop - start, '2nd:', stop2 - stop)
        t1 = timeit.default_timer()
        for x in range(10 ** 15, 10 ** 15 + 10000):
            self.decibinaryNumbers(x)
        t2 = timeit.default_timer()
        print('Time many: ', t2 - t1)

    def initSimple(self):
        d = {}
        val = 0
        for n in range(1200111):
            if n % 10 == 0:
                val = decbinValue(n)
            else:
                val += 1
            if val not in d:
                d[val] = [n]
            else:
                d[val].append(n)
        self.dbl = []
        ls = []
        for v in range(100):
            self.dbl.extend(sorted(d[v]))
            ll = len(d[v])
            ls.append((ll, self.numRepr(v)))
        print(len(self.dbl))

    def decibinaryNumbersSimple(self, x):
        if x <= len(self.dbl):
            return self.dbl[x - 1]
        else:
            return 0

    def init(self):
        # tmst1 = timeit.default_timer()
        self.MAX_VAL = 285113
        # print(self.MAX_VAL, bin(self.MAX_VAL), len(bin(self.MAX_VAL)))
        self.MAX_L = 20
        # tmst2 = timeit.default_timer()
        self.ndra = [list(repeat(0, self.MAX_VAL)) for i in range(self.MAX_L)]
        # self.ndra = [array.array('q', repeat(0, self.MAX_VAL)) for i in range(self.MAX_L)]
        # self.ndra = [memoryview(self.mem[i*8*self.MAX_VAL: (i+1)*8*self.MAX_VAL]).cast('q') for i in range(self.MAX_L)]
        # [array.array('q', repeat(0, self.MAX_VAL)) for i in range(self.MAX_L)]
        for d in range(self.MAX_L):
            self.ndra[d][0] = 1
        # tmst3 = timeit.default_timer()
        max_values = [(2 ** d - 1) * 9 for d in range(self.MAX_L)]
        for v in range(1, self.MAX_VAL):
            # self.ndra[0][v] = 0 # default is zero
            rr = [(v - i) // 2 for i in range(10) if v - i >= 0 and (v - i) % 2 == 0]
            slc = slice(min(rr), max(rr) + 1)
            for d in range(1, self.MAX_L):
                if v <= max_values[d]:
                    self.ndra[d][v] = sum(self.ndra[d - 1][slc])
        # tmst4 = timeit.default_timer()
        self.ssum = list(repeat(0, self.MAX_VAL))
        self.ssum[0] = self.ndra[-1][0]
        for v in range(1, self.MAX_VAL):
            self.ssum[v] = self.ssum[v - 1] + self.ndra[-1][v]
        # print(self.ssum[-1])
        # tmst5 = timeit.default_timer()
        # print('Time whole: ', tmst4 - tmst1)
        # print('Time : ', tmst2 - tmst1)
        # print('Time : ', tmst3 - tmst2)
        # print('Time : ', tmst4 - tmst3)
        # print('Time : ', tmst5 - tmst4)
        # for v in range(1, self.MAX_VAL//1000):
        #     d = 3
        #     if self.ndra[d][v] != self.numFixR(v, d):
        #         print("NOOO", v, self.ndra[d][v], self.numFixR(v, d))
        #         break;

    def numFixArr(self, n, d):
        return self.ndra[d][n]

    def decibinaryNumbers(self, x):
        if x == 1:
            return "0"
        # find decibinary value
        v = bisect.bisect_left(self.ssum, x)
        x = x - self.ssum[v - 1]
        # v = 0
        # while self.numRepr(v) < x:
        #     x -= self.numRepr(v)
        #     v += 1
        # if v != newv or x != newx:
        #     print("WWW", x, newx, v, newv)
        #     return 0
        # find lenth of result
        l = 0
        while self.ndra[l][v] < x:
            l += 1
        res = [0] * l
        selected_value = 0
        rv = v
        for pos in range(l):
            dig_left = l - pos - 1
            p2 = 2 ** dig_left
            ndra_dig = self.ndra[dig_left]
            for dig in range(10):
                ndr = ndra_dig[rv]
                if ndr < x:
                    x -= ndr
                else:
                    res[pos] = dig
                    break
                rv -= p2
        return "".join(map(str, res))


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    q = int(input())
    sol = Solution()
    for q_itr in range(q):
        x = int(input())
        result = sol.decibinaryNumbers(x)
        fptr.write(str(result) + '\n')
    fptr.close()