import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cbook as cbook

data= np.loadtxt("times.txt", delimiter=",", )
print data
x = data[:,0]
y = data[:,1] 

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.set_title("Document Frequency Parsing")
ax1.set_xlabel("# of Documents")
ax1.set_ylabel("time(s)")
ax1.plot(x, y, c='r', label = 'the data') 

plt.show()

