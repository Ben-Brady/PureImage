import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


def Plot3Point(DATA:dict):
    Labels = list(DATA.keys())
    Data = [x[:3] for x in (DATA.values())]

    NewData = [[],[],[]]

    for Point in Data:
        for x in range(len(Point)):
            NewData[x].append(Point[x])

    fig = plt.figure()
    ax = plt.axes(projection ='3d')

    for i in range(len(Data)): #plot each point + it's index as text above
        ax.scatter(NewData[0][i],NewData[1][i],NewData[2][i],color='b') 
        ax.text(NewData[0][i],NewData[1][i],NewData[2][i], Labels[i], size=8, zorder=1,
        color='k') 
    plt.show()