#!/usr/bin/dev python
#coding=utf-8
"""
Author:         Xiao-Yan Xu <wanderxu@gmail.com>
Description:
use chi square to do fitting.

"""
import math
import numpy as np
import scipy.optimize as opt

## define read file func
def file2list(filename):
		fr = open(filename)
		array = fr.readlines()
		num = len(array)
		returnMat=np.zeros((num,4))  # you can change the dimension 
		index = 0
		for line in array:
				line = line.strip()
				linelist = line.split()
				returnMat[index,:]=linelist[0:4] # you can change the dimension
				index +=1
		return returnMat

## define curvefunc for curve_fit
def curvefunc (xv, *p0 ):
        results = p0[0]
        for i in range(len(xv)):
            results = results + p0[i+1]*xv[i]
        return results

def chi_square ( xdata, ydata, ydata_sigma, p0 ):
        popt,pcov = opt.curve_fit(curvefunc, xdata, ydata, p0, sigma=ydata_sigma, absolute_sigma=False )
        perr = np.sqrt(np.diag(pcov))
        rchi_sq = np.sum( ( (ydata-curvefunc(xdata, *popt ) ) / ydata_sigma )**2 ) / len(ydata)
        return popt, perr, rchi_sq


## prepare data
#indat=file2list("train.dat")
indat=np.loadtxt( 'train.dat')
inmat = np.transpose(indat)
ncol=len(inmat)
xdata = inmat[1:ncol]
ydata = inmat[0]
ydata_sigma =len(ydata)*[1.0]
p0=ncol*[1.0]
popt,perr,rchi_sq = chi_square( xdata, ydata, ydata_sigma, p0 )
for i in range(ncol-1) :
    print " {} +/- {} for p{}".format(popt[i+1],perr[i+1],i+1)
i=0
print " {} +/- {} for p{}".format(popt[i],perr[i],i)
print " x^2 = ", rchi_sq
