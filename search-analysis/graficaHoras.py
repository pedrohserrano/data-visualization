#!/usr/local/Cellar/python3/3.5.1/bin/python3
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if __name__ == "__main__":
    
    todos=[[] for i in range(7)]
    dias=0

    while True:

        linea = sys.stdin.readline()
        if not linea:
            break
        
        # print(linea)
        separado=linea.split(',')

        # 1 es numeroDia, 2 es nombreDia
        x = int(separado[1])
        y = [int(i) for i in separado[3:27]]

        #print(separado)
        #print(y)
        
        todos[x].append(y)
        dias+=1
    
    fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(9, 4))

    axes[0][0].set_title('Lunes')
    axes[0][1].set_title('Martes')
    axes[0][2].set_title('Miercoles')
    axes[0][3].set_title('Jueves')
    axes[1][0].set_title('Viernes')
    axes[1][1].set_title('Sabado')
    axes[1][2].set_title('Domingo')
    
    numdia = 0
    for j in range(2):
        for i in range(4):
            if not (j == 1 and i > 2):
                dia = np.array(todos[numdia])
                numdia+=1

                bar_l = [i+1 for i in range(24)]
                performance=dia.mean(0)
                error=dia.std(0)
                
                # axes[j][i].barh(bar_l, performance, xerr=error, align='center',alpha = 0.5, color='green', ecolor='gray')
                axes[j][i].errorbar(bar_l, performance, yerr=error, fmt='o')

    # adding horizontal grid lines
    #for ax in axes:
    #    ax.yaxis.grid(True)
    #    ax.set_xticks([y+1 for y in range(len(all_data))])
    #    ax.set_xlabel('xlabel')
    #    ax.set_ylabel('ylabel')

    print("dias: {}".format(dias))
    # add x-tick labels
    #plt.setp(axes, xticks=[y+1 for y in range(len(all_data))],
    #         xticklabels=['x1', 'x2', 'x3', 'x4'])
    plt.show()

    #    20170202,3,Thursday,0,0,0,0,0,0,0,0,0,1,0,1,6,5,8,11,10,3,0,2,0,0,0,0
    