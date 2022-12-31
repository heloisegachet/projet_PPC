import numpy as np

def diff(x,y,i,j):
	if x!=y:
		return i!=j

def diag(x,y,i,j):
	return ((x-y)!=np.abs(i-j)) and ((x-y)!=-np.abs(i-j))
