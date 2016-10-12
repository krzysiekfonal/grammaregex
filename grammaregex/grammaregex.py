"""
.. module:: grammaregex
   :platform: Unix, Windows, Linux
   :synopsis: A useful module for processing sentences(in tree form) by grammar patterns.

.. moduleauthor:: Krzysztof Fonal <krzysiekfonal@gmail.com>


"""


import re


class PatternSyntaxException(Exception):
    """Exception class for raising wrong structure of patterns"""

    def __init__(self, pattern):
        self.pattern = pattern

    def __str__(self):
        return repr("Error in syntax of provided pattern (%s)" % self.pattern)


def _match_token(t, p, isEdge):
    p = p.strip()
    if p[0] == "!":
        return not _match_token(t, p[1:], isEdge)
    elif p[0] == "[":
        return any(_match_token(t, _p, isEdge) for _p in p[1:-1].split(","))
    elif p == "*" or p == "**":
        return True
    elif isEdge:
        return p == t.dep_
    else:
        return p == t.tag_ or p == t.pos_ or p == t.ent_type_ or p == t.lemma_


def verify_pattern(pattern):
    """Verifies if pattern for matching and finding fulfill expected structure.

        :param pattern: string pattern to verify

        :return: True if pattern has proper syntax, False otherwise

    """

    regex = re.compile("^!?[a-zA-Z]+$|[*]{1,2}$")

    def __verify_pattern__(__pattern__):
        if not __pattern__:
            return False
        elif __pattern__[0] == "!":
            return __verify_pattern__(__pattern__[1:])
        elif __pattern__[0] == "[" and __pattern__[-1] == "]":
            return all(__verify_pattern__(p) for p in __pattern__[1:-1].split(","))
        else:
            return regex.match(__pattern__)
    return all(__verify_pattern__(p) for p in pattern.split("/"))


def print_tree(sent, token_attr):
    """Prints sentences tree as string using token_attr from token(like pos_, tag_ etc.)

        :param sent: sentence to print
        :param token_attr: choosen attr to present for tokens(e.g. dep_, pos_, tag_, ...)

    """
    def __print_sent__(token, attr):
        print("{", end=" ")
        [__print_sent__(t, attr) for t in token.lefts]
        print(u"%s->%s(%s)" % (token,token.dep_,token.tag_ if not attr else getattr(token, attr)), end="")
        [__print_sent__(t, attr) for t in token.rights]
        print("}", end=" ")
    return __print_sent__(sent.root, token_attr)


def match_tree(sentence, pattern):
    """Matches given sentence with provided pattern.

        :param sentence: sentence from Spacy(see: http://spacy.io/docs/#doc-spans-sents) representing complete statement
        :param pattern: pattern to which sentence will be compared

        :return: True if sentence match to pattern, False otherwise

        :raises: PatternSyntaxException: if pattern has wrong syntax

    """

    if not verify_pattern(pattern):
        raise PatternSyntaxException(pattern)

    def _match_node(t, p):
        pat_node = p.pop(0) if p else ""
        return not pat_node or (_match_token(t, pat_node, False) and _match_edge(t.children,p))

    def _match_edge(edges,p):
        pat_edge = p.pop(0) if p else ""
        if not pat_edge:
            return True
        elif not edges:
            return False
        else:
            for (t) in edges:
                if (_match_token(t, pat_edge, True)) and _match_node(t, list(p)):
                    return True
                elif pat_edge == "**" and _match_edge(t.children, ["**"] + p):
                    return True
        return False
    return _match_node(sentence.root, pattern.split("/"))


def find_tokens(sentence, pattern):
    """Find all tokens from parts of sentence fitted to pattern, being on the end of matched sub-tree(of sentence)

        :param sentence: sentence from Spacy(see: http://spacy.io/docs/#doc-spans-sents) representing complete statement
        :param pattern: pattern to which sentence will be compared

        :return: Spacy tokens(see: http://spacy.io/docs/#token) found at the end of pattern if whole pattern match

        :raises: PatternSyntaxException: if pattern has wrong syntax

    """

    if not verify_pattern(pattern):
        raise PatternSyntaxException(pattern)

    def _match_node(t, p, tokens):
        pat_node = p.pop(0) if p else ""
        res = not pat_node or (_match_token(t, pat_node, False) and (not p or _match_edge(t.children, p, tokens)))
        if res and not p:
            tokens.append(t)
        return res

    def _match_edge(edges,p, tokens):
        pat_edge = p.pop(0) if p else ""
        if pat_edge:
            for (t) in edges:
                if _match_token(t, pat_edge, True):
                    _match_node(t, list(p), tokens)
                    if pat_edge == "**":
                        _match_edge(t.children, ["**"] + p, tokens)
    result_tokens = []
    _match_node(sentence.root, pattern.split("/"), result_tokens)
    return result_tokens
