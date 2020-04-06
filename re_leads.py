#!/usr/bin/env python
# coding: utf-8

# In[19]:


import pandas as pd

a = pd.read_csv("counter.csv")

b = a["campaign"]


list = ["google","facebook", "youtube", "quora","linkedin","kaleyra","dm", "news"]
new  = []
for i in b:
    for j in list:
        if j in i.lower():
           new.append(j) 
           break
    else :
       new.append("others")
    
print(new) 
x= pd.DataFrame(new, columns = ['group'])
x['count'] = a['count']

get = x.groupby('group').sum()


print(get)

