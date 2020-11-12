
import sys
import re
from optparse import OptionParser
import subprocess
import os
import time

#modify /Lustre02/data/hic/highres_human/allsamples/'''+mytissue+'''_forsort/allcisandtrans.hic for your specific case
#modify alltissues=['A1','A2','A3','A4'] for your specific case

class generate:

	def __init__ (self,path='/Lustre01/tangqianzi/forJinOrth/expresion_level_coreAtlas/'):

		self.path = path
		self.jobfolder = 'allcorjobs'

	def generate (self):

                alltissues=['circRNA','lncRNA','miRNA','PG','TUCP']

                os.system('mkdir -p '+self.path+'/'+self.jobfolder+'/')

                myoutput=open(self.path+'/'+self.jobfolder+'/runthis_pipeline.sh','w')
	        myoutput1=open(self.path+'/'+self.jobfolder+'/runthis_dump.sh','w')
	        myoutput2=open(self.path+'/'+self.jobfolder+'/alljobs_dump.sh','w')

                for mytissue in alltissues:
                        os.system('mkdir -p '+self.path+'/Rscripts/')
                        handle1=open(self.path+'/Rscripts/pearson1_'+mytissue+'.R','w')
                        handle2=open(self.path+'/Rscripts/spearman1_'+mytissue+'.R','w')


                        print>>handle1,'''setwd("'''+self.path+'''")
data<-read.table(file="forcor_'''+mytissue+'''.txt",sep="\\t",header=T,row.names=1)
mymatrix<-cor(t(as.matrix(data)),method = c("pearson"))
colnames(mymatrix)<-rownames(data)
rownames(mymatrix)<-rownames(data)
write.table(mymatrix,file="pearson1_'''+mytissue+'''.txt",sep="\\t",quote=F,row.names=T,col.names=T)
'''

                        print>>handle2,'''setwd("'''+self.path+'''")
data<-read.table(file="forcor_'''+mytissue+'''.txt",sep="\\t",header=T,row.names=1)
mymatrix<-cor(t(as.matrix(data)),method = c("spearman"))
colnames(mymatrix)<-rownames(data)
rownames(mymatrix)<-rownames(data)
write.table(mymatrix,file="spearman1_'''+mytissue+'''.txt",sep="\\t",quote=F,row.names=T,col.names=T)
'''


                        handle1.close()
                        handle2.close()

                        print>>myoutput2,'''export R_LIBS=/Lustre01/tangqianzi/software/Rlibstest/:$R_LIBS
Rscript '''+self.path+'/Rscripts/pearson1_'+mytissue+'.R'

                        print>>myoutput2,'''export R_LIBS=/Lustre01/tangqianzi/software/Rlibstest/:$R_LIBS
Rscript '''+self.path+'/Rscripts/spearman1_'+mytissue+'.R'

                for mytissue in alltissues:
                        handle3=open(self.path+'/Rscripts/pearson2_'+mytissue+'.R','w')
                        handle4=open(self.path+'/Rscripts/spearman2_'+mytissue+'.R','w')

                        print>>handle3,'''library(Hmisc)
setwd("'''+self.path+'''")
data<-read.table(file="forcor_'''+mytissue+'''.txt",sep="\\t",header=T,row.names=1)
matriz <-rcorr(t(as.matrix(data)), type=c("pearson"))

matriz_r<-matriz$r
matriz_P<-matriz$P

colnames(matriz_r)<-rownames(data)
rownames(matriz_r)<-rownames(data)

colnames(matriz_P)<-rownames(data)
rownames(matriz_P)<-rownames(data)

write.table(matriz_r,file="pearson2_'''+mytissue+'''.r.txt",sep="\\t",quote=F,row.names=T,col.names=T)
write.table(matriz_P,file="pearson2_'''+mytissue+'''.P.txt",sep="\t",quote=F,row.names=T,col.names=T)
'''


                        print>>handle4,'''library(Hmisc)
setwd("'''+self.path+'''")
data<-read.table(file="forcor_'''+mytissue+'''.txt",sep="\\t",header=T,row.names=1)
matriz <-rcorr(t(as.matrix(data)), type=c("spearman"))

matriz_r<-matriz$r
matriz_P<-matriz$P

colnames(matriz_r)<-rownames(data)
rownames(matriz_r)<-rownames(data)

colnames(matriz_P)<-rownames(data)
rownames(matriz_P)<-rownames(data)

write.table(matriz_r,file="spearman2_'''+mytissue+'''.r.txt",sep="\\t",quote=F,row.names=T,col.names=T)
write.table(matriz_P,file="spearman2_'''+mytissue+'''.P.txt",sep="\t",quote=F,row.names=T,col.names=T)
'''


                        handle3.close()
                        handle4.close()

                        print>>myoutput2,'''export R_LIBS=/Lustre01/tangqianzi/software/Rlibstest/:$R_LIBS
Rscript '''+self.path+'/Rscripts/pearson2_'+mytissue+'.R'

                        print>>myoutput2,'''export R_LIBS=/Lustre01/tangqianzi/software/Rlibstest/:$R_LIBS
Rscript '''+self.path+'/Rscripts/spearman2_'+mytissue+'.R'

	        print>>myoutput1,'/usr/bin/perl /Lustre01/tangqianzi/software/scripts/qsub-sgenew.pl --maxjob 100 --lines 2 --jobprefix mydump --convert no --resource nodes=1:ppn=1,mem=150g '+self.path+'/'+self.jobfolder+'/alljobs_dump.sh'

	        myoutput1.close()
	        myoutput2.close()

	        print>>myoutput,'sh '+self.path+'/'+self.jobfolder+'/runthis_dump.sh'

	        myoutput.close()


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
