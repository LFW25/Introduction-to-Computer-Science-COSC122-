import matplotlib.pyplot as plt 

x  = [1, 10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000, -1]
y = [702, 631, 632, 606, 556, 563, 569, 432, 322, 268, 226,  227, 208]


# plotting the points  
plt.plot(x, y) 

# naming the x axis 
plt.xlabel('Slice size of War and Peace ([:n])') 
# naming the y axis 
plt.ylabel('Number of guesses') 

# giving a title to my graph 
plt.title('Relationship between corpus size and guesses to complete a phrase') 

# function to show the plot 
plt.show() 