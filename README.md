# grammaregex

Regex like pattern tree matching but on sentence's tree instead of Strings.

Currently it works on sentences(and assumes this format) produced by [spaCy](https://spacy.io/) library.
Direction for future would be to make it independent on NLP parser libraries providers.

1. Installation
2. License
3. Description
4. API docs
5. Examples


## 1. Installation

grammaregex is published on PyPi, so to install it run:
pip install grammaregex

It requires spaCy library only.


## 2. License

grammaregex is available for everyone else to use on MIT license bases(liberal free usage).


## 3. Description

Idea of grammaregex is to provide operations on tree sentence syntax produced by spaCy using 
friendly-regex-like format similar to path patterns on OS systems.
Patterns are build in format: node/edge/node/edge/.../node...
So the analogy to path-patterns like dir/dir/.../dir/file is that we also travel by tree like 
directory tree in OS and you can treat node as file and edge as directory with the differences:
-Instead of directory name we have name of dependency(edge) with parent token
-Instead of file we have token(node)
-path consists of alternate in sequence node/edge/node/edge (opposite to path-pattern where we have
only directories with a file on the end).
Grammar pattern always starts with node because root token doesn't have any dependency and ends on final token.
Node is one of token part, it can be: pos(e.g. ADV, NOUN), tag(e.g. VBD, NNP), lemma(base of word) or entity_names type(e.g. PERSON)

So for instance to express pattern like: Verb connected by prep(prepositional) dependency with IN(subordinating conjunction) which is 
connected by pobj(object of preposition) with NNP(singular noun) we will have such pattern:
VBD/prep/IN/pobj/NNP

You can use '\*' char to express any edge or token like: 

VBD/\*/IN - verb connected by any dependency with IN

or 

\*/prep/IN - any root node connected by prep with IN

You can also use '\*\*' chars to express any edge on any level like:

VBD/\*\*/DT - verb connected with eny edge n-times with DT at the end

There is also possibility to use list to express "one of ..." like:

VBD/prep/IN/pobj/[IN,DT]


## 4. API docs
Library for now contains 4 methods:

* print_tree(sent, token_attr):
    Prints sentences tree as string using token_attr from token(like pos_, tag_ etc.)

    Param sent: sentence to print
    Param token_attr: choosen attr to present for tokens(e.g. dep_, pos_, tag_, ...)


* verify_pattern(pattern):
    Verifies if pattern for matching and finding fulfill expected structure.
	
	Param: pattern: string pattern to verify

    Return: True if pattern has proper syntax, False otherwise


* match_tree(sentence, pattern):
    Matches given sentence with provided pattern.

    Param sentence: sentence from Spacy(see: http://spacy.io/docs/#doc-spans-sents) representing complete statement
    Param pattern: pattern to which sentence will be compared

    Return: True if sentence match to pattern, False otherwise

    Raises: PatternSyntaxException: if pattern has wrong syntax


* find_tokens(sentence, pattern):
    Find all tokens from parts of sentence fitted to pattern, being on the end of matched sub-tree(of sentence)

    Param sentence: sentence from Spacy(see: http://spacy.io/docs/#doc-spans-sents) representing complete statement
    Param pattern: pattern to which sentence will be compared

    Return: Spacy tokens(see: http://spacy.io/docs/#token) found at the end of pattern if whole pattern match

    Raises: PatternSyntaxException: if pattern has wrong syntax


## 5. Examples
Below you will find a few examples of usage. Examples will base on such sentence:
"Mrs. Robinson graduated from the Wharton School of the University of Pennsylvania in 1980."

To prepare such sentence in spacy you need to do:
nlp = spacy.load("en")
doc = nlp(u"Mrs. Robinson graduated from the Wharton School of the University of Pennsylvania in 1980.")
sent = next(doc.sents)

Now basing on this 'sent' variable we can do for instance:

* print_tree(sent, "tag_")

  Prints:
  { { { Mrs.->compound(NNP) } Robinson->nsubj(NNP) } graduated->ROOT(VBD) { from->prep(IN) { { the->det(DT) } { Wharton->compound(NNP) } School->pobj(NNP) { of->prep(IN) { { the->det(DT) } University->pobj(NNP) { of->prep(IN) { Pennsylvania->pobj(NNP) } } } } } } { in->prep(IN) { 1980->pobj(CD) } } { .->punct(.) } }

* match_tree(sent, "VBD/prep/IN/pobj/NNP")
  
  Result: True

* match_tree(sent, "VBD/prep/IN/pobj/VBD")

  Result: False

* match_tree(sent, "VBD/**/DT")
  
  Result: True

* find_tokens(sent, "VBD/prep/IN/pobj/*")

  Result: ["School", "1980"]

* find_tokens(sent, "VBD/prep/IN/*/[NNP,DT]")

  Result: ["School"]

* find_tokens(sent, "VBD/**/DT")

  Result: ["the", "the"]
