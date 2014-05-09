import matplotlib.pyplot as plt

plt.figure(1)
yticks=['a','b','c','d']
x=[1,2,3,4]
y=[1,2,3,4]
plt.plot(x,y)
plt.yticks(y,yticks)
plt.show()