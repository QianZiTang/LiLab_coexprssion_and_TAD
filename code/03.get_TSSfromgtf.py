
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
		self.input = open(path+'/sus_scrofa.analysis.gtf','r')
		self.input2 = open(path+'/forcor_PG.txt','r')
		self.output1 = open(path+'/TSS_PG.txt','w')
		self.output2 = open(path+'/TSS_TUCP.txt','w')
		self.output3 = open(path+'/TSS_lncRNA.txt','w')

	def generate (self):

	        keepPG={}
	        i=0
	        for line in self.input2:
	               line=line.rstrip()
	               parts=line.split('\t')
	               if i!=0:
	                       keepPG[parts[0]]=0

	               i+=1



                alldata=[]
                gene2trans={}
                trans2exon={}
                ## gene2type={}
	        for line in self.input:
	               line=line.rstrip()
	               parts=line.split('\t')
	               if not(line.startswith('#')):
	                       if parts[2]=='exon':
	                               eachparts=parts[8].split(';')

	                               start=parts[3]
	                               end=parts[4]
	                               ## newchr=ensemble2ucsc[parts[0]]

	                               for c in eachparts:
	                                       if re.search('gene_biotype "',c):
	                                               genetype=c.split('gene_biotype "')[1].split('"')[0]

	                                       if re.search('transcript_id "',c):
	                                               transid=c.split('transcript_id "')[1].split('"')[0]

	                                       if re.search('gene_id "',c):
	                                               geneid=c.split('gene_id "')[1].split('"')[0]




                                       if genetype=='TUCP' or genetype=='lncRNA' or genetype=='lincRNA':
                                               gene2trans[geneid]=[]
                                               trans2exon[transid]=[]
                                               ## gene2type[geneid]=genetype.rstrip().lstrip()

	                       elif parts[2]=='gene':
	                               eachparts=parts[8].split(';')

	                               start=parts[3]
	                               end=parts[4]
	                               ## newchr=ensemble2ucsc[parts[0]]

	                               for c in eachparts:
	                                       if re.search('gene_biotype "',c):
	                                               genetype=c.split('gene_biotype "')[1].split('"')[0]

	                                       if re.search('transcript_id "',c):
	                                               transid=c.split('transcript_id "')[1].split('"')[0]

	                                       if re.search('gene_id "',c):
	                                               geneid=c.split('gene_id "')[1].split('"')[0]

                                       ## if genetype=='protein_coding':
                                       if geneid in keepPG:
                                               if parts[6]=='+':
                                                       myTSS=parts[3]
                                               else:
                                                       myTSS=parts[4]

                                               print>>self.output1,parts[0]+'\t'+myTSS+'\t'+geneid


                               alldata.append(line)


  	        for line in alldata:
	               ## line=line.rstrip()
	               parts=line.split('\t')
	               ## if not(line.startswith('#')):
	               if 1:
	                       if parts[2]=='exon':
	                               eachparts=parts[8].split(';')

	                               start=int(parts[3])
	                               end=int(parts[4])
	                               ## newchr=ensemble2ucsc[parts[0]]

	                               for c in eachparts:
	                                       if re.search('gene_biotype "',c):
	                                               genetype=c.split('gene_biotype "')[1].split('"')[0]

	                                       if re.search('transcript_id "',c):
	                                               transid=c.split('transcript_id "')[1].split('"')[0]

	                                       if re.search('gene_id "',c):
	                                               geneid=c.split('gene_id "')[1].split('"')[0]

                                       #alldata.append(line)
                                       if genetype=='TUCP' or genetype=='lncRNA' or genetype=='lincRNA':
                                               gene2trans[geneid].append(transid)
                                               trans2exon[transid].append([start,end,parts[0]])


                trans2genefinal={}
                trans2keep={}
                for mygene in gene2trans:
                        each=[]
                        for mytrans in gene2trans[mygene]:
                                trans2keep[mytrans]=0
                                tot=0
                                for c in trans2exon[mytrans]:
                                        tot+=int(int(c[1])-int(c[0])+1)

                                each.append([tot,mytrans])

                        each.sort()
                        each.reverse()

                        mytransfinal=each[0][1]
                        trans2genefinal[mytransfinal]=mygene
                        trans2keep[mytransfinal]=1



  	        for line in alldata:
	               ## line=line.rstrip()
	               parts=line.split('\t')
	               ## if not(line.startswith('#')):
	               if 1:
	                       if parts[2]=='transcript':
	                               eachparts=parts[8].split(';')

	                               start=int(parts[3])
	                               end=int(parts[4])
	                               ## newchr=ensemble2ucsc[parts[0]]

	                               for c in eachparts:
	                                       if re.search('gene_biotype "',c):
	                                               genetype=c.split('gene_biotype "')[1].split('"')[0]

	                                       if re.search('transcript_id "',c):
	                                               transid=c.split('transcript_id "')[1].split('"')[0]

	                                       if re.search('gene_id "',c):
	                                               geneid=c.split('gene_id "')[1].split('"')[0]

                                       #alldata.append(line)
                                       if genetype=='TUCP' or genetype=='lncRNA' or genetype=='lincRNA':
                                               if trans2keep[transid]==1:
                                                       if parts[6]=='+':
                                                            myTSS=parts[3]
                                                       else:
                                                            myTSS=parts[4]

                                                       if genetype=='TUCP':
                                                            print>>self.output2,parts[0]+'\t'+myTSS+'\t'+geneid
                                                       else:
                                                            print>>self.output3,parts[0]+'\t'+myTSS+'\t'+geneid



		self.input.close()
		self.output1.close()
		self.output2.close()
                self.output3.close()


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
