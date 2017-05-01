import sys, os, time, requests, queue, re
import pickle

try:
    f2 = open('cache/variable/dict.pckl', 'rb')
    f3 = open('cache/variable/pk.pckl', 'rb')
except FileNotFoundError:
    print("variable file not found", file=sys.stderr)
d = pickle.load(f2)
f2.close()
pk = pickle.load(f3)
f3.close()
# print(d)
# print(pk)
#
# for key, value in d.items():
#     if value["pk"] >= 0:
#         print(key)
#         print(value)

d2 = {}
for key, value in d.items():
    if value["pk"] < 1700:
        d2[key] = value

pk = 1700
# print(d2)


f = open('cache/variable/pk.pckl', 'wb')
pickle.dump(pk, f)
f.close()
f = open('cache/variable/dict.pckl', 'wb')
pickle.dump(d2, f)
f.close()
