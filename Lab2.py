#!/usr/bin/env python
# coding: utf-8

# In[13]:


import sympy
import concurrent.futures


def tCalculaPrimo(data):
    primos = 0
    for i in range(len(data)):
        if sympy.isprime(data[i]):
            primos += 1
    return primos

def resolve_trhread(data, ThreadsQtdd):
    tamanholista = len(data)
    index = range(0, tamanholista+(tamanholista//ThreadsQtdd), tamanholista//ThreadsQtdd)
    primos = 0
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for i in range(ThreadsQtdd):
            futures.append(executor.submit(tCalculaPrimo, data=data[index[i]:index[i+1]]))
        for future in concurrent.futures.as_completed(futures):
            #futures.append(future.result())
            primos += future.result()
    return primos


# In[14]:


import sympy

def resolve_simples(data):
    tamanholista = len(data)
    primos = 0
    for i in range(tamanholista):
        if sympy.isprime(data[i]):
            primos += 1
    return primos


# In[15]:


# importing pandas library  
import pandas as pd 

def tabela(df,threads, tempo_exc, primo_mt,speedup):
    #print(df)
    A=[threads, tempo_exc, primo_mt,speedup]
    #print(A)
    
    #s = pd.Series(A, index=df.columns)
    #df = df.append(s, ignore_index=True)
    
    df.loc[len(df)] = A

    #display(df)
    return(df)


# In[23]:


from time import perf_counter_ns
import pandas as pd 
import matplotlib.pyplot as plt
lista = [1,2,3]
i=0
df = pd.DataFrame(columns=['Threads','Execucao','Numeros_Primos', 'SpeedUp'])
with open("data.csv") as file:
    data = [line.strip() for line in file]
    
while i<=1:
    for x in lista:
        
        threads = x
        data = list(map(int, data))
    
        start1 = perf_counter_ns()
        primo_sp = resolve_simples(data)
        finish1 = perf_counter_ns()

        start2 = perf_counter_ns()
        primo_mt = resolve_trhread(data, threads)
        finish2 = perf_counter_ns()

        tempo_exc = (finish2-start2)/1000000
        speedup = (finish1-start1)/(finish2-start2)

        df_2 = tabela(df,threads, tempo_exc, primo_mt,speedup)
    i=i+1
    print(i)
    
print('\n\nAnalise de %d valores\n\n'%(len(data)))
display(df_2)

df_2.plot(x ='SpeedUp', y='Threads', kind = 'scatter')


# In[ ]:




