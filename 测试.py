# a="#7e7e7e"
# if a[0]=="#":
#     print(1)
import win32api

import numpy as np

a=[231,231,231]

b=[221,207,221]
kk=abs((np.array(b)-np.array(a)))/np.array(a)
could=1
for i in kk:
    if i>1-0.9:
        could=0
        break
print(could)