bases=("fomos" "cobre")

scripts=scripts
ngrams=$scripts/ngrams.py
ksmooth=$scripts/ksmoothing.py
program=$scripts/program.py

k=1 

params=parametrization

out="Anotado.out"
final="Anotado.final"
non_smooth=".temp.txt"
unigram="Unigramas"
bigram="Bigramas"
lemmas="Lemas.txt"
sents="Frases.txt"
result="Resultado.txt"

for base in "${bases[@]}" 
	do
		sed -n "/^.*$base.*$base.*$/I!p" generated/$base$out > generated/$base$final
		sed -n -i "/^n-é-verbo/!p" generated/$base$final
		sed -n -i "/^\(ser\|ir\|cobrir\|cobrar\|\?\)#/!p" generated/$base$final
		sed -n -i "/^\(ser\|ir\|cobrir\|cobrar\)\??\t/!p" generated/$base$final
		sed -n -i "s/\(ser\|ir\|cobrir\|cobrar\)\(.*\)$base\(.*\)/\2\1\3/gp" generated/$base$final

		python3 $ngrams generated/$base$final 1 generated/$base$unigram$non_smooth
		python3 $ngrams generated/$base$final 2 generated/$base$bigram$non_smooth

		python3 $ksmooth $k generated/$base$unigram$non_smooth generated/$base$bigram$non_smooth $params/$base$lemmas generated/$base$unigram.txt generated/$base$bigram.txt

		find . -name \*$non_smooth -type f -delete

		python3 $program generated/$base$unigram.txt generated/$base$bigram.txt $params/$base$lemmas corpora/test/$base$sents generated/results/$base$result
done
