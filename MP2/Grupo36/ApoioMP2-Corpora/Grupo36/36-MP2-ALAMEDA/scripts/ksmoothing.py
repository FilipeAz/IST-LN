import collections
import re
import sys
import time
import ngrams

# #########################
#    Text preprocessing   #
# #########################

def preprocess_text(unigrams_file, bigrams_file, lemmas_file):
	unigrams_map = {}
	bigrams_map = {}		
	
	if lemmas_file:
		for line in lemmas_file:
			lemmas = line.split() #(base, lemma1, lemma2)
	
	if unigrams_file:
		for line in unigrams_file:
			unigram = line.split() #(word, count)
			if(unigram):
				unigrams_map[unigram[0]] = float(unigram[1])

	if bigrams_file:
		for line in bigrams_file:
			bigram = line.split() #(word1, word2, count)
			if(bigram):
				bigrams_map[(bigram[0], bigram[1])] = float(bigram[2])	
			
	return unigrams_map, bigrams_map, lemmas

# #############################
#     Arguments processing    #
# #############################

def process_args():
	if(len(sys.argv) < 5 or len(sys.argv) > 7):
		print('Usage: python ksmoothing.py k unigrams-file bigrams-file lemmas-file [unigram_out-file] [bigram_out_file]')
		sys.exit(1)
	
	unigrams_file = open(sys.argv[2], ngrams.READ, encoding = ngrams.ISO_ENCODING) #file with unigram counts
	bigrams_file = open(sys.argv[3], ngrams.READ, encoding = ngrams.ISO_ENCODING) #file with bigram counts
	lemmas_file = open(sys.argv[4], ngrams.READ, encoding = ngrams.ISO_ENCODING) #file with base word and its lemmas
	
	if(len(sys.argv) > 5):
		unigram_out_file = open(sys.argv[5], ngrams.WRITE, encoding = ngrams.ISO_ENCODING) #nigrams output file
	else:
		unigram_out_file = sys.stdout
		
	if(len(sys.argv) > 6):
		bigram_out_file = open(sys.argv[6], ngrams.WRITE, encoding = ngrams.ISO_ENCODING) #bigrams output file
	else:
		bigram_out_file = sys.stdout	
		
	return unigrams_file, bigrams_file, lemmas_file, unigram_out_file, bigram_out_file

# #############################
#      Auxiliary Functions    #
# #############################

def get_count(ngram_map, ngram):
	if ngram in ngram_map:
		return ngram_map[ngram]
	return 0

#utility function to avoid generating the entire bigrams file
def get_bigram_smoothed_probability(unigrams_map, bigram, k):
	if bigram[0] in unigrams_map and bigram[1] in unigrams_map:
		vocabulary_size = len(unigrams_map) #V - number of different word types
		
		return k / (get_count(unigrams_map, bigram[0]) + (k * vocabulary_size))
	return 0
			
# #############################
#             Main            #
# #############################

if __name__ == '__main__':
	print(time.strftime(ngrams.TIME_FORMAT, time.gmtime()))
	
	unigrams_file, bigrams_file, lemmas_file, unigram_out_file, bigram_out_file = process_args()
	unigrams_map, bigrams_map, lemmas = preprocess_text(unigrams_file, bigrams_file, lemmas_file)
	
	vocabulary_size = len(unigrams_map) #V - number of different word types
	size = sum([unigrams_map[word] for word in unigrams_map.keys()]) #N - total number of words
	k = float(sys.argv[1])
	
	smooth_bigrams_map = {}
	smooth_unigrams_map = {}
	
	for word in unigrams_map.keys():
		#P*(w) = C(w) + k / N + kV
		smooth_unigrams_map[(word,)] = (get_count(unigrams_map, word) + k) / (size + (k * vocabulary_size))
		
		#C*(w) = (C(w) + k) * N / N + kV
		#smooth_unigrams_map[(word,)] = (get_count(unigrams_map, word) + k) * (size / (size + (k * vocabulary_size)))
	
	#add all combinations of the desired lemmas since they are needed in the next step 
	for word1 in unigrams_map.keys():
		for word2 in unigrams_map.keys():
			if word1 == lemmas[1] or word1 == lemmas[2] or word2 == lemmas[1] or word2 == lemmas[2]:
				bigram = (word1, word2)
				
				if bigram not in bigrams_map:
					smooth_bigrams_map[bigram] = k / (get_count(unigrams_map, bigram[0]) + (k * vocabulary_size))	
	
	for bigram in bigrams_map.keys():
		#P(w1w2) = P(w2 | w1) = C(w1, w2) + k / C(w1) + kV
		smooth_bigrams_map[bigram] = (get_count(bigrams_map, bigram) + k) / (get_count(unigrams_map, bigram[0]) + (k * vocabulary_size))
		
		#C*(w1w2) = (C(w1, w2) + k) * C(w1) / C(w1) + kV
		#smooth_bigrams_map[bigram] = ((get_count(bigrams_map, bigram) + k) * get_count(unigrams_map, bigram[0])) / (get_count(unigrams_map, bigram[0]) + (k * vocabulary_size))

	ngrams.print_ngrams(smooth_unigrams_map, file = unigram_out_file)
	ngrams.print_ngrams(smooth_bigrams_map, file = bigram_out_file)

	print(time.strftime(ngrams.TIME_FORMAT, time.gmtime()))
	
	ngrams.exit(unigrams_file, bigrams_file, lemmas_file, unigram_out_file, bigram_out_file)
