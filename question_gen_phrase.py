#notes:
# wh-words: what, where, why, who, whom, which, when, how,
#probably most will be what, where, who, or when
#things to figure out about the input phrase: plurality, whether it is a person, place, or time
#use dependency parsing to figure out what is the main subject of the phrase
#
import spacy
#import nltk
test1 = "property location"
test2 = "the building height"
test3 = "the building was built in"
test4 = "the property is located at"
test5 = "property located"
test6 = "the building location"
test7 = "stories"
test8 = "building entrance"
test9 = "bedrooms"
test10 = "the lot size"

nlp = spacy.load("en_core_web_sm") #try larger version
#test_doc = nlp(test10)

#for token in test_doc:
#	print(token.text, token.tag_, token.dep_)

#print(len(list(test_doc.noun_chunks)))
#for chunk in test_doc.noun_chunks:
	#print(chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text, chunk.root.head.tag_)
#	pos = chunk.root.head.tag_
#	break


#print(pos)

def question_gen(phrase):
	question_list = ["what", "where", "when", "who", "how", "why", "which", "whom"]
	wh_type = "what"
	phrase_type = ""
	main_text = ""
	tokens = nlp(phrase)
	if tokens[0].text in question_list:
		return phrase
	if tokens[0].text == "building":
		phrase = "the " + phrase
		#print(phrase)
		tokens = nlp(phrase)
	#if tokens[-1].text == "in":
	#	return str()
	for token in tokens:
		if token.dep_ == "ROOT":
			phrase_type = token.tag_
			main_text = token.text
			print(phrase_type, main_text)
			break
	wh_type = wh_type_checker(main_text)
	print(wh_type, phrase_type)
	if wh_type == "how many":
		return str("how many " + main_text)
	elif phrase_type == "NNS" or phrase_type == "NNPS":
		if tokens[0].text == "the":
			return str(wh_type + "are " + phrase)
		else:
			return str(wh_type + " are the " + phrase)
	elif phrase_type == "NN" or phrase_type == "NNP":
		if tokens[0].text == "the":
			return str(wh_type + " is " + phrase)
		else:
			return str(wh_type + " is the " + phrase)



def wh_type_checker(main_text):
 	when_list = ["opening", "groundbreaking"]
 	where_list = ["entrance", "exit", "location", "entrances", "exits"]
 	who_list = ["broker", "manager", "architect", "dealer", "engineer", "brokers", "managers", "architects", "dealers", "engineers"]
 	how_many_list = ["floors", "stories", "feet", "inches", "bedrooms"]
 	if main_text in when_list:
 		return "when"
 	elif main_text in where_list:
 		return "where"
 	elif main_text in who_list:
 		return "who"
 	elif main_text in how_many_list:
 		return "how many"
 	else:
 		return "what"

print(question_gen(test7))

