# This is a python snippet for quick hull algorithm implementation
# intended for use on hyperspectral data.

import numpy as np
import math
import matplotlib.pyplot as plt
sample = np.asarray([list(x) for x in zip(range(32),[x[0] for x in np.random.random((32,1)).tolist()])])
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
        plt.plot([p1[0],p2[0]],[p1[1],p2[1]])
        plt.plot([p1[0],p3[0]],[p1[1],p3[1]])
        plt.plot([p2[0],p3[0]],[p2[1],p3[1]])
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
#plt.show()

plt.show()
