import re
import sys
import time
import operator

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
UTF_ENCODING = 'utf-8'
ISO_ENCODING = 'iso-8859-1'
WRITE = 'w'

def tokenize(string):
    return ['<s>'] + re.findall(r'\w+', string.lower()) + ['</s>']

def count_ngrams(lines, n = 1):
    ngrams = {}
    
    for line in lines:
        ngram = []
        count = 0
        
        for word in tokenize(line):
            ngram.append(word)
            count += 1
            
            if count == n:
                ngram = tuple(ngram)
                
                if not ngram in ngrams:
                    ngrams[ngram] = 0
                ngrams[ngram] += 1
                
                count = 0
                ngram = []
                
    return ngrams


def print_ngrams(ngrams, file = sys.stdout):
    ngrams = dict(sorted(ngrams.items(), key = operator.itemgetter(1), reverse=True))
    
    for ngram in ngrams:
        print('{0} {1}'.format(' '.join(ngram), ngrams[ngram]), file = file)
    print('', file = file)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python ngrams.py filename n-size [output_file]')
        sys.exit(1)
        
    if(len(sys.argv) > 3):
        output_file = open(sys.argv[3], WRITE, encoding = ISO_ENCODING)
    else:
        output_file = sys.stdout

    print(time.strftime(TIME_FORMAT, time.gmtime()))
    
    n_size = int(sys.argv[2])
    
    with open(sys.argv[1], encoding = UTF_ENCODING) as file:
        ngrams = count_ngrams(file, n = n_size)
    print_ngrams(ngrams, file = output_file)
    
    output_file.close()
    file.close()    
    
    print(time.strftime(TIME_FORMAT, time.gmtime()))
    