import collections
import re
import sys
import time

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
ENCODING = 'ISO-8859-1'
READ = 'r'
WRITE = 'w'

# #########################
#   Text preprocessing    #
# #########################

def preprocess_text(unigrams_file, bigrams_file, lemmas_file):
	unigrams_map = {}
	bigrams_map = {}		
	
	for line in lemmas_file:
		lemmas = line.split() #(base, lemma1, lemma2)
	
	for line in unigrams_file:
		unigram = line.split() #(word, count)
		if(unigram):
			unigrams_map[unigram[0]] = int(unigram[1])

	for line in bigrams_file:
		bigram = line.split() #(word1, word2, count)
		if(bigram):
			bigrams_map[(bigram[0], bigram[1])] = int(bigram[2])	
			
	return unigrams_map, bigrams_map, lemmas

# #############################
#   Arguments preprocessing   #
# #############################

def process_args():
	if(len(sys.argv) != 4 and len(sys.argv) != 5):
		print('Usage: python laplace-smoothing.py unigrams-file bigrams-file lemmas-file [output-file]')
		sys.exit(1)
	
	unigrams_file = open(sys.argv[1], READ, encoding = ENCODING) #file with unigram counts
	bigrams_file = open(sys.argv[2], READ, encoding = ENCODING) #file with bigram counts
	lemmas_file = open(sys.argv[3], READ, encoding = ENCODING) #file with base word and its lemmas
	
	if(len(sys.argv) > 4):
		output_file = open(sys.argv[4], WRITE, encoding = ENCODING) #output file
	else:
		output_file = sys.stdout
		
	return unigrams_file, bigrams_file, lemmas_file, output_file

# #############################
#      Auxiliary Functions    #
# #############################

def get_count(ngram_map, ngram):
	if ngram in ngram_map:
		return ngram_map[ngram]
	return 0

def exit(*arg):
	if(arg):
		for file in arg:
			file.close()
			
# #############################
#             Main            #
# #############################

if __name__ == '__main__':
	print(time.strftime(TIME_FORMAT, time.gmtime()))
	
	unigrams_file, bigrams_file, lemmas_file, output_file = process_args()
	unigrams_map, bigrams_map, lemmas = preprocess_text(unigrams_file, bigrams_file, lemmas_file)
	
	vocabulary_size = len(unigrams_map) #V - number of different word types
	length = sum([unigrams_map[word] for word in unigrams_map.keys()]) #N - total number of words
	
	for word1 in unigrams_map.keys():
		for word2 in unigrams_map.keys():
			if word1 == lemmas[1] or word1 == lemmas[2] or word2 == lemmas[1] or word2 == lemmas[2]:
				bigram = (word1, word2)
			
				#P(bigram) = P(w2 | w1) = C(w1, w2) + 1 / C(w1) + V
				prob = (get_count(bigrams_map, bigram) + 1) / (get_count(unigrams_map, bigram[0]) + vocabulary_size)
				
				print(bigram[0] + ' ' + bigram[1] + ' ' + str(prob), file = output_file)

	print(time.strftime(TIME_FORMAT, time.gmtime()))
	
	exit(unigrams_file, bigrams_file, output_file)
