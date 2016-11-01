# coding: utf-8
'''
@Author: zengguangsheng
@Date: 2016-05-24~26 05-31
@Topic: T1-B1-1 data analysis (first draft)
'''
## import packages
from pyspark import SparkConf,SparkContext
import re
import numpy as np
from pyspark.mllib.clustering import KMeans, KMeansModel
from math import sqrt
import matplotlib.pyplot as plt
from pyspark.mllib.linalg import Vectors
import time
import json
get_ipython().magic(u'matplotlib inline')

## self-defined function: to compute fisher distance for each feature
'''
parameter:
FmatVector---one feature vector
return:
    return fisher distance of each feature vector
	
	2....
	
'''
def fisherDist(FmatVector):
    
    fmatV = np.array(FmatVector)
    num = np.size(fmatV)
    per10Data  = num / 10 + 1
    
    preMean = np.mean(fmatV[0:per10Data])
    preVariance = np.var(fmatV[0:per10Data])
    postMean = np.mean(fmatV[num-per10Data:num])
    postVariance = np.var(fmatV[num-per10Data:num])
    
    fDistance = (preMean-postMean)**2 / (preVariance + postVariance)
    
    return fDistance


## self-defined function: to selecte main feature from source feature matrix
'''
parameter:
Fmat---source feature matrix
FCodingSeq---feature coding sequences
FSelectedNum---the numbers of features we want to select
return: 
    the features matrix we selected   
	3....
'''
def FeatureSelection(FMat,FCodingSeq,FSelectedNum):
    SFunion = []
    for seq in FCodingSeq:
	## acording to FCodingSeq, select features from source features
        SelectedFeature = FMat[seq-1]
	## normalization into (-1,1) 
        SelectedFeature = SelectedFeature / max(abs(SelectedFeature)) 
        SFunion.append(SelectedFeature)
    selectedFmat = sc.parallelize(SFunion)
    ## TODO we should filter features which is unrelative with result
    ## acording to FSelectedNum, reduce features from selected features 
    selectedFmat = selectedFmat.take(FSelectedNum) 
    return selectedFmat


## Evaluate clustering by computing Within Set Sum of Squared Errors
## self-defined function: to evaluate clustering
'''
parameter:
point--- each feature samplling point
return: 
    Squared Errors of each point
	//
'''
def error(point):
    center = clusters.centers[clusters.predict(point)]
    return sqrt(sum([x**2 for x in (point - center)]))


## self-defined function: to find the health cluster's Center
'''
parameter:
clustersCenters---the centers of all clusters
memsVector--the membership vector of sampling points
dataIndex--- to record the index of each sampling point
return: 
    the health cluster's Center vector
	
	
	4...
'''
def FindHealthCenter(clustersCenters,memsVector,dataIndex):
    eachClusternum = np.zeros(clusterNums,dtype=np.int64)
    for mems in memsVector:
        for i in range(clusterNums):
            if mems == i :
                tmpvec[i][dataIndex]=1+dataIndex
                eachClusternum[i] += 1
                dataIndex += 1
    Tj = np.zeros(clusterNums,dtype=np.float)
    for i in range(clusterNums):
        Tj[i] = sum(tmpvec[i])/eachClusternum[i]
    return clustersCenters[np.argsort(Tj)[0]]



## self-defined function: to compute DV FV and SV distance
'''
parameter:
Vh---the centers of the health cluster
P--selected feature matrix, namely clusterData or likely selectedfmat
return: 
    DV FV and SV distance
	
	
	5..
'''
def DistanceAnalysis(Vh,P):
    DV = []
    DV = P.map(lambda point: sum([abs(x) for x in (point - Vh)])/seleFnum).collect()
    tempPoint = P.take(P.count())
    Point = np.array(tempPoint)
    
    FV = []
    FV.append(sum([abs(x) for x in (Point[0] - Point[1])])/seleFnum)
    for i in range(1,len(Point)-1):
        FV.append((sum([abs(x) for x in (Point[i] - Point[i+1])])/seleFnum \
				+ sum([abs(x) for x in (Point[i] - Point[i-1])])/seleFnum) / 2 )
    FV.append(sum([abs(x) for x in (Point[len(Point)-1] - Point[len(Point)-2])])/seleFnum)
    if len(DV) != len(FV):
        print "Error: len(DV) != len(FV)!"
        return
    
    SV = []
    for i in range(len(DV)):
        SV = map(lambda (x,y): sqrt(x*y),zip(DV,FV))
    return [DV,FV,SV]

## by Euclidean distance
def DistanceAnalysisEuclidean(Vh,P):
    DV = []
    '''DV = P.map(lambda point:                sqrt(sum([x**2 for x in (point - Vh)]))).collect()'''
    DV = P.map(lambda point: sqrt(sum([x**2 for x in (point - Vh)]))).collect()
    tempPoint = P.take(P.count())
    Point = np.array(tempPoint)
    
    FV = []
    FV.append(sqrt(sum([x**2 for x in (Point[0] - Point[1])])))
    for i in range(1,len(Point)-1):
        FV.append((sqrt(sum([x**2 for x in (Point[i] - Point[i+1])])) \
				+ sqrt(sum([x**2 for x in (Point[i] - Point[i-1])]))) / 2 )
    FV.append(sqrt(sum([x**2 for x in (Point[len(Point)-1] - Point[len(Point)-2])])))
    if len(DV) != len(FV):
        print "Error: len(DV) != len(FV)!"
        return
    
    SV = []
    for i in range(len(DV)):
        SV = map(lambda (x,y): sqrt(x*y),zip(DV,FV))
    return [DV,FV,SV]


if __name__ == "__main__":
    ## Configure Spark
    # sc has been up and running,nothing to do here 
    t0 = time.clock()
    ## golbal variance
    clusterNums = 4  ## the numbers of clusters we expect
    ## feature coding sequences - fcs
    #fcs = np.array([18,14,17,13,2,12,7])
    #fcs = Vectors.dense([18,14,17,13,2,12,7])
    #fcsRDD = sc.parallelize(fcs)

    seleFnum = 5 ## feature num we select after feature coding sequences filtering
    ## for t1-b1-1.txt, we select 5 from 8(feature coding sequences)

    ## read data from hdfs
    inputdata  = sc.textFile("/home/hadoop/spark161/bear1/t1-b1-1.txt")
    dataNums =  inputdata.count()  # save numbers of sampling points
    print 'the number of data in file : %s ' % dataNums

    ## split data by space-white characters
    srcfMat = inputdata.map(lambda line: Vectors.dense(re.split('\s',line.strip())))

    ## get all sampling points, then save as numpy array
    tempMat = srcfMat.take(srcfMat.count())
    npFmatT = np.array(tempMat).T
    ## npFmatT: rows---features, col---sampling points, size: 18*dataNums
    print 'feature sampleing points try show:'    
    print npFmatT[0][0:5]
    
    FMatList = sc.parallelize(npFmatT).zipWithIndex().collect()
    FMatRDD = sc.parallelize(FMatList)
    ## get sorted feature coding sequences
    fCodeSeqRDD = FMatRDD.map(lambda eachFeature: (fisherDist(eachFeature[0]),eachFeature[1]+1)).sortByKey(False)
    
    fcsVectors = fCodeSeqRDD.take(fCodeSeqRDD.count())
    print 'all feature coding sequences(sorted by descending order):'
    print fcsVectors
    toJson = {}
    toJson["data"] = fcsVectors
    print 'write into json file......'
    print toJson
    #json.dump(toJson,open('/home/hadoop/IBDoutput/Bearing/t1b11_FisherDist_bar_data.json','w'))
    
    slectedFCSnum = 7
    myFcsVectorsRDD = fCodeSeqRDD.map(lambda each: each[1])
    myFcsVectorsList = myFcsVectorsRDD.take(myFcsVectorsRDD.count())
    ## feature coding sequences - fcs
    fcs = np.array(myFcsVectorsList[0:slectedFCSnum])
    #fcs = Vectors.dense([18,14,17,13,2,12,7])
    #fcsRDD = sc.parallelize(fcs)
    #fcsRDD.take(fcsRDD.count())
    
    reducedFmat = FeatureSelection(npFmatT,fcs,seleFnum)
    #selectedFmat = fcsRDD.map(lambda each: srcFMatT[each-1]/max(abs(srcFMatT[each-1])))
    ## return features matrix we selected as a list

    ## transform list to numpy array
    clusterData = np.array(reducedFmat).T
    ## clusterData: dataNums*5
    ## clusterData: rows---sampling points,cols---selected features
    print 'the reduced feature matrix :'
    print clusterData

    ## Build the model (cluster the data)
    clusterDataRDD = sc.parallelize(clusterData)
    t1 = time.clock()
    clusters = KMeans.train(clusterDataRDD, clusterNums , maxIterations=100, runs=1, initializationMode='k-means||', seed=None,             		initializationSteps=5, epsilon=1e-4, initialModel=None)
    t2 = time.clock()
    ## Find the cluster to which point belongs in this model.
    predictRDD = clusterDataRDD.map(lambda point: clusters.predict(point))
    memberShipVector = predictRDD.take(predictRDD.count())
    print 'the membership(the cluster to which point belongs) vector:'
    print memberShipVector[0:100]
	
    ## Evaluate clustering
    SSE = clusterDataRDD.map(lambda point: error(point))
    WSSSE = SSE.reduce(lambda x, y: x + y)
    print "the K-means cost(it's mine): " + str(WSSSE)

    ## Return the K-means cost (sum of squared distances of points to their 
    ## nearest center) for this model on the given data.
    ## this is a KMeansModel method (built-in)
    #print "the K-means cost(built-in): " + str(clusters.computeCost(clusterData))

    # membership matrix with time weights
    tmpvec = np.zeros([clusterNums,dataNums],dtype=np.int64)
    dataIndex = 0
    clusterCenters = clusters.centers
    # membership matrix with time weights
    Vh = FindHealthCenter(clusterCenters,memberShipVector,dataIndex)
    print 'Health Center:'
    print Vh
    
    ## Get the cluster centers, represented as a list of NumPy arrays.
    #clusters.centers

    ## plot sampling points scatter figure and Centers (choose two dimensions: E and E2)
    ## clusterData: dataNums*5,rows---sampling points,cols---selected features
    print 'plot sampling points scatter figure and Centers ......'
    t3 = time.clock()
    scatterPoints(memberShipVector,clusterCenters,clusterData) 
    t4 = time.clock()
    print 'plotPoints() takes %f s ' % (t4 - t3)
    ## to compute DV FV and SV distance
    t3 = time.clock()
    #threeDistance = DistanceAnalysis(Vh,clusterDataRDD)
    threeDistance = DistanceAnalysisEuclidean(Vh,clusterDataRDD)
    t4 = time.clock()
    print 'DistanceAnalysisEuclidean() takes %f s ' % (t4 - t3)
    ## threeDistance = [DV,FV,SV]
    np3Distance = np.array(threeDistance)
    SV = np3Distance[2]
    print 'Synthesize Value:'
    print SV
    #print sqrt(np3Distance[0][255]*np3Distance[1][255])==np3Distance[2][255]
    
    ## plot the SV
    print 'plot the SV ......' 
    t3 = time.clock()
    plotSV(SV)
    t4 = time.clock()
    print 'plotSV(SV) takes %f s ' % (t4 - t3)
    print 'Kmeans.train() takes %f s ' % (t2 - t1)
    print 'running time : %f s ' % (t4 - t0)
    ## Save and load model,so we can use this model later
    #clusters.save(sc, "/home/hadoop/spark161/bear1")
    #sameModel = KMeansModel.load(sc, "/home/hadoop/spark161/bear1")




