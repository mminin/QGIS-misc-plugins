amp=[]
with open('../source/amp.txt','r') as amplitude:
    for ampline in amplitude:
        amp+=[q for q in ampline[1:-1].split(' ') if q !='']
amp[-1]=amp[-1][:-1]
amp=[float(q) for q in amp]

wavel=[]
with open('../source/wavelen.txt','r') as wavelength:
    wavel=wavelength.readline()[1:-1].split(', ')
wavel=[float(q) for q in wavel]

data=list(zip(wavel,amp))
for x in [-1,1,0]: del data[x]

####

import numpy as np
import math
import matplotlib.pyplot as plt
sample=data
###
#
#
#
#
####
start  = sample[:1]
end    = sample[-1:]
getDist = lambda p1,p2,p3: ( (p1[1]-p2[1])*p3[0] - (p1[0]-p2[0])*p3[1] + p2[0]*p1[1] - p2[1]*p1[0]) / \
                             math.sqrt( (p2[1]-p1[1])**2 + (p2[0]-p1[0])**2 )
def getFurthestPnt(sample):
    start  = sample[:1][0]
    end    = sample[-1:][0]
    subsample=sample[1:-1]
    d,n,nn=0,0,-1
    for p in sample:
        nn+=1
        dn=getDist(start, end, p)
        n=nn*(d<dn)+n*(d>dn)
        d=[d,dn][d<dn]
    return n

#getFurthestPnt(sample)

def recur(sample,q):
    if len(sample)>2:
        fp=getFurthestPnt(sample)
        p1=sample[:1][0]
        p2=sample[-1:][0]
        p3=sample[fp]
        #plt.plot([p1[0],p2[0]],[p1[1],p2[1]])
        #plt.plot([p1[0],p3[0]],[p1[1],p3[1]])
        #plt.plot([p2[0],p3[0]],[p2[1],p3[1]])
        if fp != 0:
            q.append(sample[fp])
            subsampA=sample[:fp+1]
            subsampB=sample[fp:]
            recur(subsampA,q)
            recur(subsampB,q)

samplex=[a[0] for a in sample]
sampley=[a[1] for a in sample]
plt.scatter(samplex,sampley,color='blue')

q=[]
recur(sample,q)
qx=[a[0] for a in q]
qy=[a[1] for a in q]
plt.scatter(qx,qy,color='red')
qsort=sorted(q, key=lambda w:w[0])
qsort=[(samplex[0],sampley[0])]+qsort+[(samplex[-1],sampley[-1])]
for i in range(len(qsort)-1):
    plt.plot([qsort[i][0],qsort[i+1][0]],[qsort[i][1],qsort[i+1][1]], color='black')


qsortx=[q[0] for q in qsort]
qsorty=[q[1] for q in qsort]

contiY=np.interp(samplex,qsortx,qsorty)
plt.scatter(samplex,contiY, color="purple")

contRemY=sampley/contiY
plt.plot(samplex,contRemY, color="black")

plt.show()




