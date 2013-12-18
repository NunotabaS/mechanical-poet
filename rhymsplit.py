from nltk.corpus import cmudict
import re

d = cmudict.dict()
s = ["and"] #stopwords

def nsyl(word):
	return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]]

def guessSyllable(word):
	sylcount = 0
	if re.match(r"^\d+$", word):
		sylcount = len(word)
	else:
		lastVowel = False
		for letter in word:	
			if letter in ['a','e','i','o','u','y'] and not lastVowel:
				sylcount += 1
				lastVowel = True
			else:
				lastVowel = False
	#print "Guessing " + word + " has syllables %d" % sylcount
	return sylcount

def getSyllable(word):
	try:
		return nsyl(word)[0];
	except KeyError:
		return guessSyllable(word);

def getSubsentence(text, splitinto):
	sc = 0
	listIdx = 0
	words = text.lower().split();
	tmp = []
	subparts = []
	for word in words:
		if word in s:
			continue;
		sc += getSyllable(word)
		tmp.append(word)
		if sc >= splitinto[listIdx % len(splitinto)]:
			subparts.append(" ".join(tmp))
			tmp = []
			sc = 0
			listIdx += 1
	if len(tmp) > 0:
		subparts.append(" ".join(tmp))
	return subparts

def normText(text):
	text = re.sub(r"[-,\(\)]"," ", text);
	return re.sub(r"[^a-zA-Z0-9\s]", "", text)
	
def split(delimiters, string, maxsplit=0):
    import re
    regexPattern = '|'.join(map(re.escape, delimiters))
    return re.split(regexPattern, string, maxsplit)

if __name__ == '__main__' : 
	import sys
	with open(sys.argv[2]) as g:
		stopwords = [re.sub(r"\n", "", line) for line in g.readlines()];
		print stopwords
		with open(sys.argv[1]) as f:
			for line in f:
				line = normText(line)
				sentences = split(stopwords, line)
				for sentence in sentences:
					print ""
					#print sentence
					print getSubsentence(normText(sentence), [11]);
