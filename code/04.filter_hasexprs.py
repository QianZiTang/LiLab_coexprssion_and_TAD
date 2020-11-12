
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
		self.input1 = open(path+'/TSS_'+mytype+'.txt','r')
		self.input2 = open(path+'/forcor_'+mytype+'.txt','r')
		self.output = open(path+'/TSS_'+mytype+'.forfilter.txt','w')
		self.maxchr = '18'

	def generate (self):

                keepgenes={}
                i=0
                for line in self.input2:
                        line=line.rstrip()
                        parts=line.split('\t')
                        if i!=0:
                                keepgenes[parts[0]]=0
                        i+=1


                for line in self.input1:
                        line=line.rstrip()
                        parts=line.split('\t')
                        if parts[2] in keepgenes:
                                print>>self.output,parts[2]+'\t'+'1'
                        else:
                                print>>self.output,parts[2]+'\t'+'0'



		self.input1.close()
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
