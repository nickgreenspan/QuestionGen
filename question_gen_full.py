import spacy

#from benepar.spacy_plugin import BeneparComponent



sent1 = "The building has 30 floors."
sent2 = "The property is located on 30 beacon street, and is very tall."
sent3 = "The Sponsors are Besyata Investment Group and The Scharf Group."
sent4 = "The owners gave out free cookies on opening day."
sent5 = "The Scharf Group is a well known Brooklyn family office with a stellar ownership and development background."
sent6 = "The building is so tall."
sent7 = "The Sponsors purchased the Land and 26,000 sf of air rights in 2017, and have worked on all the approvals for a total current market value of $22 Million."
sent8 = "The Sponsors are currently seeking a $47,000,000 construction loan, which represents 80 of the total Capitalization."
sent9 = "Bob should defintely go to work today."
sentlong = "In connection with the Proposed Transaction, it is understood that the Disclosing Party and its Representatives (as hereinafter defined) are prepared to furnish the Recipient and its Representatives with certain oral and written information concerning the Property that is or may be non-public, confidential and/or proprietary in nature, which may include, without limitation, contracts, documents, appraisals, site plans, plans and specifications, renderings, drawings, reports, studies, analysis (financial or otherwise), budgets, financial statements, organizational, principal and/or sponsor information, and computer data and/or files (“confidential Information”)."
sent10 = "Edward J. Minskoff, the principal of the Sponsor, has claimed the penthouse unit for his personal residence, arguably the greatest commitment a Sponsor can make to a development’s delivery, quality, and success."
sent11 = "Apple shifts the market."
sentlist = [sent1, sent2, sent3, sent4, sent5, sent6, sent7, sent8, sent9, sent10, sent11]
nlp = spacy.load("en_core_web_sm") #small is a lot faster than medium, and seems to have identical performance
#nlp.add_pipe(BeneparComponent('benepar_en')) #adds contiuency parsing functionality
p1 = "111 Washington Street is currently planned as a 51-story, 405,444 gross square foot building with a cellar mechanical area, commercial space at the base, and apartments and amenities on the upper floors. The building will consist of 283,075 net rentable square feet of residential area and an additional 23,179 net rentable square feet of commercial. In total, the building will contain 429 residential apartment units. Location The subject site is located at the southeast corner of Washington and Carlisle Street in Lower Manhattan. The site is bounded by Carlisle Street to the north, Washington Street to the west, Rector Street to the south, and Greenwich Street to the east. In addition to this large footprint, the site also contains air rights from adjacent parcels which will allow for improved light and air corridors to the south and east."



def gen_questions(sent):
	gen_questions.quest1 = ""
	gen_questions.quest2 = ""

	gen_questions.ans1 = ""
	gen_questions.ans2 = ""
	qa = []
	#if ("."  != sent[-1] and "." != sent[-2]) or 'We' in sent or 'we' in sent or len(sent.split()) < 4: #might want to get rid of 'we' sentences
	#	return []
	doc = nlp(sent)
	
	for token in doc:
		if token.dep_ == "ROOT":#need to take into account that root sometimes is a noun and not a verb, this might not actually be an issue if we are soley dealing with full sentances
								# also need to take into account auxilary verbs before the root verb are not counted
								#
								#Might want to add functionality so that multiple parts of sentances can be used, look into contiuency parsing
								#Constituency parsing could be big, also in splitting up questions with an 'and' in them into multiple questions if that is deemed necessary
								# 
			root = token
			break

	for left in root.lefts:
		if left.dep_ == "nsubj" or left.dep_ == "nsubjpass": #could add adverbs like 'defintely'
			add_word1(left)

		elif left.dep_ == "aux" or left.dep_ == "auxpass":
			add_word1(left)
			add_word2(left)
			aux = True

	gen_questions.quest1 += (" " + root.text)
	gen_questions.quest2 += (" " + root.text)

	
	k = 0
	for right in root.rights:
		if k == 0 and right.pos_ == "ADP":
			gen_questions.quest2 += (" " + right.text)
			gen_questions.quest1 += (" " + right.text)
			for right2 in right.rights:
				if right2.pos_ != "CCONJ" and right2.pos_ != "PUNCT":
					add_word2(right2)
			k += 1
		elif right.pos_ != "CCONJ" and right.pos_ != "PUNCT": #could add adpositions here too, question of style, also might want to take more precautions so answers don't go on too long
			add_word2(right) 
			k += 1
		else:
			break

	if root.text == "is": #switches the order for is and or questions for improved readiblity
		gen_questions.quest2 = "What is" + gen_questions.quest2[:-2] + "?"
	elif root.text == "are":
		gen_questions.quest2 = "What are" + gen_questions.quest2[:-3] + "?"
	else:
		gen_questions.quest2 = gen_questions.quest2[1:] + " what?"

	gen_questions.quest1 = "What" + gen_questions.quest1 + "?"


	qa.append(str("question 1: " + gen_questions.quest1 + " ans: " + gen_questions.ans1))
	qa.append(str("question 2: " + gen_questions.quest2 + " ans: " + gen_questions.ans2))
	return qa




def add_word1(token):
	if token.n_lefts != 0:
		for left in token.lefts:
			add_word1(left)
	
	gen_questions.quest2 += (" " + token.text)
	if token.dep_ != "aux" and token.dep_ != "auxpass":
		gen_questions.ans1 += (" " + token.text)
	
	if token.n_rights != 0:
		for right in token.rights:
			add_word1(right)

def add_word2(token):
	if token.n_lefts != 0:
		for left in token.lefts: #could add condition here to get rid of commas
			add_word2(left)
	
	gen_questions.quest1 += (" " + token.text)
	if token.dep_ != "aux" and token.dep_ != "auxpass":
		gen_questions.ans2 += (" " + token.text)

	
	if token.n_rights != 0:
		for right in token.rights:
			add_word2(right)
for sent in sentlist:
	print(sent, gen_questions(sent))
	print(" ")

