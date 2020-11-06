
import numpy as np

import numpy as np

data = np.array([[1,9,3,4,5], [1,3,3,6,7], [20,2,4,5,7], [3,1,5,6,7], [4,6,6,7,8]])

# 按照第一列排序

idex=np.lexsort([data[:,0]])

sorted_data = data[idex, :]

print(sorted_data)
print(float(-0.05)>float(-0.1))
# 按照第二列排序


