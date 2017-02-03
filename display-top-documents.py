#!/usr/bin/env python
"""
Simple tool to display document rankings generated by NMF stored in one or more PKL
files.

Sample usage:
python display-top-documents.py base-nmf/factors_1000_001.pkl 
"""
import logging as log
from optparse import OptionParser
import numpy as np
import unsupervised.rankings, unsupervised.util

# --------------------------------------------------------------

def main():
	parser = OptionParser(usage="usage: %prog [options] factor_file1 factor_file2 ...")
	parser.add_option("-t", "--top", action="store", type="int", dest="top", help="number of top document ids to show", default=10)
	(options, args) = parser.parse_args()
	if( len(args) < 1 ):
		parser.error( "Must specify at least one factor file" )
	log.basicConfig(level=20, format='%(message)s')

	# Load each cached ranking set
	for in_path in args:
		log.info( "Loading model from %s ..." % in_path )
		(W,H,doc_ids,terms) = unsupervised.util.load_nmf_factors( in_path )
		k = W.shape[1]
		log.info( "Model has %d rankings covering %d documents" % ( k, len(doc_ids) ) )
		for topic_index in range(k):
			top_indices = np.argsort( W[:,topic_index] )[::-1]
			top_indices = top_indices[0:min(len(top_indices),options.top)]
			top_doc_ids = [ doc_ids[index] for index in top_indices ]
			log.info("C%02d: %s" % (topic_index+1, ", ".join(top_doc_ids) ) )

# --------------------------------------------------------------

if __name__ == "__main__":
	main()