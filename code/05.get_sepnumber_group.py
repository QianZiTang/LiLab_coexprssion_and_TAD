
import sys
import re
from optparse import OptionParser
import subprocess
import os
import time

#modify /Lustre02/data/hic/highres_human/allsamples/'''+mytissue+'''_forsort/allcisandtrans.hic for your specific case
#modify alltissues=['A1','A2','A3','A4'] for your specific case

class generate:

	def __init__ (self,path='/Lustre01/tangqianzi/forJinOrth/expresion_level_coreAtlas/',mytype='miRNA'):

		self.path = path
		self.input = open(path+'/TSS_'+mytype+'.txt','r')
		self.input2 = open(path+'/TSS_'+mytype+'.forfilter.txt','r')
		self.output = open(path+'/TSS_'+mytype+'.annotate.txt','w')
		self.maxchr = '18'

	def generate (self):

	        gene2index={}
	        for line in self.input2:
	               line=line.rstrip()
	               parts=line.split('\t')
	               gene2index[parts[0]]=parts[1]


	        mychroms=[]
	        for i in range(1,int(self.maxchr)+1):
	               mychroms.append(str(i))

	        alldata=[]
	        allresults={}
	        for line in self.input:
	               line=line.rstrip()
	               parts=line.split('\t')
	               alldata.append(parts)
	               if parts[0] in mychroms:
	                       allresults[parts[0]]=[]

	        for parts in alldata:
	               if parts[0] in mychroms:
	                       allresults[parts[0]].append([int(parts[1]),parts[2]])


                for mychr in mychroms:
                       allresults[mychr].sort()
                       for k in range(0,len(allresults[mychr])):
                            myleft=max(0,k-6)
                            myright=min(k+6,len(allresults[mychr])-1)

                            for m in range(myleft,myright+1):
                                    mystep=abs(m-k)-1
                                    if mystep>=0:
                                            if gene2index[allresults[mychr][m][1]]=='1' and gene2index[allresults[mychr][k][1]]=='1':
                                                    print>>self.output,allresults[mychr][m][1]+'\t'+allresults[mychr][k][1]+'\t'+str(mystep)+'\t'+mychr


		self.input.close()
		self.input2.close()
		self.output.close()


def main():

	usage = "usage: %prog [options] <pathandfiles>"
	description = "Generate jobs."

	optparser = OptionParser(version="%prog 0.1",description=description,usage=usage,add_help_option=False)
	optparser.add_option("-h","--help",action="help",help="Show this help message and exit.")

	(options,pathandfiles) = optparser.parse_args()

	generate().generate()

if __name__ == '__main__':

	try:
		main()
	except KeyboardInterrupt:
		sys.stderr.write("User interrupt me! ;-) See you!\n")
		sys.exit(0)
