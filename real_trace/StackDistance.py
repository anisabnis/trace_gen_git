import random, sys, math
#from sympy import *
#from sympy.mpmath import *

class StackDistance:
	def __init__(self, currentCap):
		self.inf = sys.maxsize
		self.servedCount = 0
		self.servedBytes = 0
		self.popularity = {} # Hitcount of all objects
		self.currentCap = currentCap
		self.currentHitrate = 0.0

	def getHitrate(self, newCap):
		return -1
# Che's approximation model functions
class CheHitrate(StackDistance):
	def __init__(self, currentCap, m, multiple):
		StackDistance.__init__(self, currentCap)
		# Che's approximation model
		self.hitrateCT = {} # Periodically updated hitrate curve based on characteristic time (count,size)
		self.lastAccess = {}
		self.IATDist = {} # (count, bytes)
		self.popDist = {} # 100 popularity buckets? or may be by log so we capture magnitudes
		self.multiple = multiple

	def updateHist(self, oid, csize, multicopy, t):
		if random.uniform(0,1) < 1.2:
			IAT = self.inf if oid not in self.lastAccess else t - self.lastAccess[oid]
			if IAT < 0:
				return
			self.lastAccess[oid] = t if oid not in self.lastAccess else (t if t > self.lastAccess[oid] else self.lastAccess[oid])
			#multiple = 1000
			#self.multiple = 1 # multiple=1 for IAT-SD
			IAT_m = (IAT//self.multiple)*self.multiple
			self.IATDist[IAT_m] = (1, csize) if IAT_m not in self.IATDist else (self.IATDist[IAT_m][0]+1, self.IATDist[IAT_m][1]+csize)
			self.servedCount +=1
			self.servedBytes += csize
			# COMMENTED out for IAT-SD - 03/11/16
			#self.popularity[oid] = 1 if oid not in self.popularity else self.popularity[oid]+1
			#self.popDist[int(math.log(self.popularity[oid], 10))] = 1 if int(math.log(self.popularity[oid], 10)) not in self.popDist \
			#							  else self.popDist[int(math.log(self.popularity[oid], 10))]+1

			return IAT_m

	def computeCurve(self):
		count = 0
		bytes = 0
		x = sorted(self.IATDist.keys())
		for i in x:
			count += self.IATDist[i][0]
			bytes += self.IATDist[i][1]
			self.hitrateCT[i] = (count/self.servedCount, bytes/self.servedBytes)

	def getHitrate(self, newCap):
		# Use Che's approximation to get characteristic time from newCap
		total = sum(list(self.popDist.values()))
		# popDistListCdf:
	#	print(self.popDist)
		total = sum(self.popDist.values())
		popDistFrac = [self.popDist[i]/total for i in self.popDist]
		popDistList = {}

		# Define symbols for summation
		i = Symbol('i')
		n = Symbol('n')
		# solve doesnt work
		#charTimeList = solve(Eq(nsum(lambda i: 1-pow(exp(-1*popDistFrac[int(i)]),n), [0,len(popDistFrac)-1])), n)
		#print(Eq(nsum(lambda i: 1-pow(exp(-1*popDistFrac[int(i)]),n), [0,len(popDistList)-1])), n)

		# Solving numerically
		# number of variable = number of popularity levels - WRONG
		# charTimeList = nsolve([Eq(newCap-nsum(lambda i: 1-pow(exp(-1*popDistFrac[int(i)]),n), [0,len(popDistFrac)-1]))], [n], [1])
		# number of variable = number of unique objects
		charTimeList = nsolve([Eq(newCap-nsum(lambda i: 1-pow(exp(-1*popDistFrac[int(i)]),n), [0,len(popDistFrac)-1]))], [n], [1])
		#print(newCap-nsum(lambda i: 1-pow(exp(-1*popDistFrac[int(i)]),n), [0,len(popDistFrac)-1]))
		charTime = float(list(charTimeList)[0])
		#charTime = 0

		print(popDistFrac)
		print('charTime:', charTime)
		# Currently only request hitrate
		hitrate = self.hitrateCT[int(charTime/100)][0] if int(charTime/100) in self.hitrateCT else 0
		return hitrate
# Stack distance functions
class SDHitrate(StackDistance):
	def __init__(self, currentCap, m, multiple):
		StackDistance.__init__(self, currentCap)
		self.B = {} # Binary values
		self.B[0] = []
		self.P = {} # Last accesstime for oid
		self.SD = {} # SD count
		self.SDBytes = {} # SD bytes
		self.requests = 0
		self.bytes = 0
		self.m = m
		self.multiple = multiple
		self.hitrateSD = {}
		self.hitrateSDRev_b = {}
		self.hitrateSDRev_c = {}

	def add(self, oid, csize, numCopies, newCopy): # If newCopy == True update old location by numCopies-1 and new location by numCopies; numCopies = updated number
		B = self.B
		P = self.P
		SD = self.SD
		SDBytes = self.SDBytes
		m = self.m

		self.requests += 1
		self.bytes += csize if oid not in P else B[0][P[oid]-1]

		# For now:
		#csize = 1 #for request SD

		# Append B
		if oid in P:
			B[0].append(0)
		else:
			B[0].append(csize)
		if self.requests//(m**(len(B))) == 1 and len(B) not in B:
			B[len(B)] = []

		for i in range(1, len(B)):
			if (self.requests//(m**i))-1 >=0 and (self.requests//(m**i)) > len(B[i]):
				ni = (self.requests//(m**i))-1
				B[i].append(sum(B[i-1][ni*(m):ni*(m)+m]))

		newCopy = False
		numCopies = 1
		#print('before update', B)
		# Update B is required
		if oid in P:
			if newCopy and numCopies>1:
				self.update(P[oid]-1, B[0][P[oid]-1]*(numCopies-1), self.requests-1, B[0][P[oid]-1]*numCopies)
			else:
				self.update(P[oid]-1, B[0][P[oid]-1]*(numCopies), self.requests-1, B[0][P[oid]-1]*numCopies)

		# Compute SD
		# In multiples of 10000?
		#multiple = 100e9 # 100G
		#multiple = 1 # multiple = 1 for IAT-SD
		if oid in P:
			csize = B[0][self.requests-1] # old csize
			sd_id = ((self.search(P[oid]-1, self.requests-1)+csize*numCopies)//self.multiple)*self.multiple
			SD[sd_id] = 1 if sd_id not in SD else SD[sd_id]+1
			SDBytes[sd_id] = csize if sd_id not in SDBytes else SDBytes[sd_id]+csize
		else:
			sd_id = (sys.maxsize//self.multiple)*self.multiple
			SD[sd_id] = 1 if sd_id not in SD else SD[sd_id]+1
			SDBytes[sd_id] = csize if sd_id not in SDBytes else SDBytes[sd_id]+csize

		#print('after update', B)
		P[oid] = self.requests

		return sd_id

	def update(self, old_pos, old_value, new_pos, new_value):
		B = self.B
		m = self.m

		lvl = 0
		#print('update', old_pos, new_pos, old_pos//m, new_pos//m)
		rList = [j for j in range(len(B)) if old_pos//m**j == new_pos//m**j]
		r = min(rList) if len(rList) > 0 else len(B)

		#print('p,t,r', old_pos, new_pos, r)
		for i in range(r):
			if old_pos//m**i < len(B[i]):
				B[i][old_pos//m**i] -= old_value
			if new_pos//m**i < len(B[i]):
				B[i][new_pos//m**i] += new_value

	def search(self, p, t):
		B = self.B
		requests = self.requests
		m = self.m

		lvl = 0
		retval2 = 0
		iterator2 = 0

		while(p//m != t//m):
			iterator2+=1
			newList = [B[lvl][i] if (p//m+1)*m-1 >= p+1 and p+1 >=0 else 0 for i in range(p+1, (p//m+1)*m-1 + 1)]
			newList2 = [B[lvl][i] if t-1 >= (t//m)*m and (t//m)*m >= 0 else 0 for i in range((t//m)*m, t-1 + 1)]
			retval2 += sum(newList)
			retval2 += sum(newList2)
			p = p//m
			t = t//m
			lvl += 1
		iterator2+=1
		newList = [B[lvl][i] if t-1 >= p+1 and p+1 >= 0 else 0 for i in range(p+1, t-1 + 1)]
		retval2 += sum(newList)
		#if retval != retval2:
		#	print('not equal!', retval, retval2)
		return retval2

	def updateHist(self, oid, csize, numCopies, newCopy, t):
		sd = self.add(oid, csize, numCopies, newCopy)
		return sd

	def computeCurve(self):
		count = 0
		bytes = 0
		x = sorted(self.SD.keys())
		#print(self.SD, self.requests)
		for i in x:
			count += self.SD[i]
			bytes += self.SDBytes[i]
			self.hitrateSD[i] = (count/self.requests, bytes/self.bytes)
		self.hitrateSDRev_b = dict((value[1],key) for key,value in self.hitrateSD.items()) # byte hitrate
		self.hitrateSDRev_c = dict((value[0],key) for key,value in self.hitrateSD.items()) # byte hitrate

	def getByteHitrate(self, newCap, t):
		#print('o')
		#print([(i,self.hitrateSD[i]) for i in sorted(self.hitrateSD.keys())])
		print(t, [(i,self.hitrateSD[i][1]) for i in sorted(self.hitrateSD.keys())])
		print()
