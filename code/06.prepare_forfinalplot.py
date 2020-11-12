#spearman1_TUCP.txt

import sys
import re
from optparse import OptionParser
import subprocess
import os
import time

#modify /Lustre02/data/hic/highres_human/allsamples/'''+mytissue+'''_forsort/allcisandtrans.hic for your specific case
#modify alltissues=['A1','A2','A3','A4'] for your specific case

class generate:

	def __init__ (self,path='/Lustre01/tangqianzi/forJinOrth/expresion_level_coreAtlas/',mytype='lncRNA',mysample='BC1'):

		self.path = path
		self.input1 = open(path+'/TSS_'+mytype+'.annotate.txt','r')
		self.input2 = open('/Lustre01/tangqianzi/forJinOrth/expresion_level_coreAtlas/ULB_TADfiles/'+mysample+'/total.combined.domaincalls','r')
		self.input3 = open(path+'/TSS_'+mytype+'.txt','r')
		self.output = open(path+'/forplot_'+mytype+'_'+mysample+'.txt','w')

		## self.input2 = open(path+'/spearman1_'+mytype+'.txt','r')
		self.maxchr = '18'
		self.mytype = mytype
		self.cutoff = '0.5'

	def generate (self):

	        gene2TSS={}
	        mychroms=[]
	        allTADs={}
	        for i in range(1,int(self.maxchr)+1):
	               mychroms.append(str(i))
	               allTADs[str(i)]=[]
	               gene2TSS[str(i)]={}

	        for line in self.input3:
	               line=line.rstrip()
	               parts=line.split('\t')
	               if parts[0] in mychroms:
	                       gene2TSS[parts[0]][parts[2]]=int(parts[1])



	        for line in self.input2:
	               line=line.rstrip()
	               parts=line.split('\t')
	               if parts[0] in mychroms:
	                       allTADs[parts[0]].append([int(parts[1]),int(parts[2])])

                allpairs_res={}
                allpairs={}
                for i in range(0,6):
                        #all>0.5, all, all>0.5 withinTAD, all withinTAD
                        allpairs_res[str(i)]=[0,0,0,0]
                        ## allpairs[str(i)]={}

                for mychr in mychroms:
                        allpairs[mychr]={}

	        for line in self.input1:
	               line=line.rstrip()
	               parts=line.split('\t')

	               pairnames=[parts[0],parts[1]]
	               pairnames.sort()

	               allpairs[parts[3]][pairnames[0]+'-'+pairnames[1]]=parts[2]

	        for mychr in mychroms:
	               handle=open(self.path+'/spearman1_'+self.mytype+'_'+mychr+'.txt','r')

	               m=0
	               ## allkeep={}
	               for line in handle:
	                       line=line.rstrip()
	                       parts=line.split('\t')
	                       if m==0:
	                               allnames=parts

	                       else:
	                               for n in range(1,len(parts)):
	                                       name1=parts[0]
	                                       name2=allnames[n-1]

	                                       if name1==name2:
	                                               continue


	                                       pairnames=[name1,name2]
	                                       pairnames.sort()

	                                       name1=pairnames[0]
	                                       name2=pairnames[1]

	                                       if pairnames[0]+'-'+pairnames[1] not in allpairs[mychr]:
	                                               continue

	                                       mytype=allpairs[mychr][pairnames[0]+'-'+pairnames[1]]

	                                       if float(parts[n])>float(self.cutoff):
                                                    allpairs_res[mytype][0]+=1

                                               allpairs_res[mytype][1]+=1


                                               gene1pos=gene2TSS[mychr][name1]
                                               gene2pos=gene2TSS[mychr][name2]

                                               sigsameTAD=0
                                               for eachparts in allTADs[mychr]:
                                                    start=eachparts[0]
                                                    end=eachparts[1]
                                                    if gene1pos>start and gene1pos<end and gene2pos>start and gene2pos<end:
                                                            sigsameTAD=1
                                                            break

                                               if sigsameTAD==1:
	                                            if float(parts[n])>float(self.cutoff):
                                                            allpairs_res[mytype][2]+=1

                                                    allpairs_res[mytype][3]+=1


	                       m+=1

	               handle.close()


                for i in range(0,6):
                       ratio1=float(allpairs_res[str(i)][2])/allpairs_res[str(i)][0]
                       ratio2=float(allpairs_res[str(i)][3])/allpairs_res[str(i)][1]
                       print>>self.output,str(i)+'\t'+str(allpairs_res[str(i)][0])+'\t'+str(allpairs_res[str(i)][1])+'\t'+str(allpairs_res[str(i)][2])+'\t'+str(allpairs_res[str(i)][3])+'\t'+str(ratio1)+'\t'+str(ratio2)


		self.input1.close()
                self.input2.close()
                self.input3.close()
                self.output.close()


def main():

	usage = "usage: %prog [options] <pathandfiles>"
	description = "Generate jobs."

	optparser = OptionParser(version="%prog 0.1",description=description,usage=usage,add_help_option=False)
	optparser.add_option("-h","--help",action="help",help="Show this help message and exit.")

	(options,pathandfiles) = optparser.parse_args()

	generate(mytype=pathandfiles[0],mysample=pathandfiles[1]).generate()


if __name__ == '__main__':

	try:
		main()
	except KeyboardInterrupt:
		sys.stderr.write("User interrupt me! ;-) See you!\n")
		sys.exit(0)
