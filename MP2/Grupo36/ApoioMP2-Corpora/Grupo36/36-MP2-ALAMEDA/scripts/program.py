import collections
import re
import sys
import time
import ksmoothing

if __name__ == '__main__':

	parametrization = open(sys.argv[3], 'r', encoding="ISO-8859-1")
	unigramsFile = open(sys.argv[1], 'r', encoding="ISO-8859-1")
	bigramsFile = open(sys.argv[2], 'r', encoding="ISO-8859-1")
	
	unigrams_map, bigrams_map, lemmas = ksmoothing.preprocess_text(unigramsFile, bigramsFile, parametrization)
	
	parametrization.close()
	unigramsFile.close()
	bigramsFile.close()
	
	ambiguousWord = lemmas[0]

	firstLemma = lemmas[1]
	
	secondLemma = lemmas[2]
	
	
	
	firstLemma_UnigramProbability = 0
	
	secondLemma_UnigramProbability = 0
	
	for unigram in unigrams_map:
		if not unigram:
			continue
		if firstLemma == unigram:
			firstLemma_UnigramProbability = unigrams_map[unigram]
			
		if secondLemma == unigram:
			secondLemma_UnigramProbability = unigrams_map[unigram]
			

	if len(sys.argv) == 6:
		output = open(sys.argv[5], 'w', encoding="ISO-8859-1")
	else:
		output = sys.stdout
	
	sentences = open(sys.argv[4], 'r', encoding="utf-8")
	
	sentencesCounter = 1
	for line in sentences:
		wordsInLine = line.split()
		for i in range(len(wordsInLine)):
			if wordsInLine[i] == ambiguousWord:
				firstBigram_firstLemma = ""
				firstBigram_secondLemma = ""
				secondBigram_firstLemma = ""
				secondBigram_secondLemma = ""
				
				firstBigram_firstLemmaProbability = 0
				
				firstBigram_secondLemmaProbability = 0
				
				secondBigram_firstLemmaProbability = 0
				
				secondBigram_secondLemmaProbability = 0
				
				if i == 0:
					firstBigram_firstLemma = "<s> " + firstLemma 
					firstBigram_secondLemma = "<s> " + secondLemma
				else:
					firstBigram_firstLemma = wordsInLine[i-1] + " " + firstLemma
					firstBigram_secondLemma = wordsInLine[i-1] + " " + secondLemma
					
				if i == len(wordsInLine) - 1:
					secondBigram_firstLemma = firstLemma + " </s>"
					secondBigram_secondLemma = secondLemma + " </s>"
				else:
					secondBigram_firstLemma = firstLemma + " " + wordsInLine[i+1]
					secondBigram_secondLemma = secondLemma + " " + wordsInLine[i+1]
				
				
				
				for bigram in bigrams_map:
					if not bigram:
						continue
					bigramFound = bigram[0] + " " + bigram[1]
					
					if firstBigram_firstLemma == bigramFound:
						firstBigram_firstLemmaProbability = bigrams_map[bigram]
						
					if firstBigram_secondLemma == bigramFound:
						firstBigram_secondLemmaProbability = bigrams_map[bigram]
					
					if secondBigram_firstLemma == bigramFound:
						secondBigram_firstLemmaProbability = bigrams_map[bigram]
				
					if secondBigram_secondLemma == bigramFound:
						secondBigram_secondLemmaProbability = bigrams_map[bigram]
						
				
				if firstBigram_firstLemmaProbability == 0:
					firstBigram_firstLemmaProbability = firstLemma_UnigramProbability
					
				if secondBigram_firstLemmaProbability == 0:
					secondBigram_firstLemmaProbability = firstLemma_UnigramProbability
					
				if firstBigram_secondLemmaProbability == 0:
					firstBigram_secondLemmaProbability = secondLemma_UnigramProbability
					
				if secondBigram_secondLemmaProbability == 0:
					secondBigram_secondLemmaProbability = secondLemma_UnigramProbability
				
				
				output.write("Frase nr" + str(sentencesCounter) + ": " + line)
				
				firstLemmaProbability = firstBigram_firstLemmaProbability * secondBigram_firstLemmaProbability
				
				secondLemmaProbability = firstBigram_secondLemmaProbability * secondBigram_secondLemmaProbability
					
				output.write("Probabilidade de " + firstLemma + " = " + str(firstLemmaProbability) + "\n")
				
				output.write("Probabilidade de " + secondLemma + " = " + str(secondLemmaProbability) + "\n")
					
				if firstLemmaProbability > secondLemmaProbability:
					output.write("O lema '" + firstLemma + "' tem maior probabilidade\n")
				else:
					output.write("O lema '" + secondLemma + "' tem maior probabilidade\n")
				
		sentencesCounter += 1
		
	output.close()
	sentences.close()				
					
					
					
					
					
					
					