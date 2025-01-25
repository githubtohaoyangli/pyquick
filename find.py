import os
def finde(path,name) :
    b=[]
    for root, dirs, files in os.walk(path):
        if name in files:
            a= os.path.join(root, name)
            b.append(a)
    return list(b)
#print(find("/Users","python_tool"))