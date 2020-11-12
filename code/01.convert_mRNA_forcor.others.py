
import sys
import re
from optparse import OptionParser
import subprocess
import os
import time
import math

#ESC_H1ESC-2.SRX378272

class generate:

	def __init__ (self,path='/Lustre01/tangqianzi/forJinOrth/expresion_level_coreAtlas/'):

		self.path = path
		self.input = open(path+'/48232_circRNA.exp.gene.tpm.rmPAD.0.05.txt','r')
		self.output = open(path+'/forcor_circRNA.txt','w')
		self.offset = '0.05'

	def generate (self):

	        i=0
	        for line in self.input:
	               line=line.rstrip()
	               parts=line.split('\t')
	               if i==0:
	                    print>>self.output,'\t'.join(parts[1:])

	               else:
	                    each=[]
                            for j in range(1,len(parts)):
                                    each.append(str(math.log(float(parts[j])+float(self.offset))/math.log(2)))
                            print>>self.output,parts[0]+'\t'+'\t'.join(each)

	               i+=1

		self.input.close()
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
