
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
		self.jobfolder = 'finalplot_nocircRNAjobs'
		self.maxchr = '18'

	def generate (self):

                alltissues=['PG','lncRNA','TUCP','miRNA']
                allsamples=['BC1','BC3','BC4','BC5','BC6','BC7','BC8','BC9','CC1','CC2','CC3','CC4']

                os.system('mkdir -p '+self.path+'/'+self.jobfolder+'/')

                myoutput=open(self.path+'/'+self.jobfolder+'/runthis_pipeline.sh','w')
	        myoutput1=open(self.path+'/'+self.jobfolder+'/runthis_dump.sh','w')
	        myoutput2=open(self.path+'/'+self.jobfolder+'/alljobs_dump.sh','w')

                for mytissue in alltissues:
                        for mysample in allsamples:
                                print>>myoutput2,'''export PATH=/Lustre01/tangqianzi/software/anaconda2new/bin/:$PATH
python '''+self.path+'/06.prepare_forfinalplot.py'+' '+mytissue+' '+mysample


	        print>>myoutput1,'/usr/bin/perl /Lustre01/tangqianzi/software/scripts/qsub-sgenew.pl --maxjob 100 --lines 6 --jobprefix mydump --convert no --resource nodes=1:ppn=1,mem=30g '+self.path+'/'+self.jobfolder+'/alljobs_dump.sh'

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
