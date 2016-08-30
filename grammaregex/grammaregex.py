import re


class PatternSyntaxException(Exception):
    def __init__(self, pattern):
        self.pattern = pattern

    def __str__(self):
        return repr("Error in syntax of provided pattern (%s)" % self.pattern)


def __match_token__(t, p, isEdge):
    p = p.strip()
    if p[0] == "!":
        return not __match_token__(t, p[1:], isEdge)
    elif p[0] == "[":
        return any(__match_token__(t, _p, isEdge) for _p in p[1:-1].split(","))
    elif p == "*" or p == "**":
        return True
    elif isEdge:
        return p == t.dep_
    else:
        return p == t.tag_ or p == t.pos_ or p == t.ent_type_ or p == t.lemma_



def verify_pattern(pattern):
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
    def __print_sent__(token, attr):
        print "{",
        [__print_sent__(t, attr) for t in token.lefts]
        print "%s->%s(%s)" % (token,token.dep_,token.tag_ if not attr else getattr(token, attr)),
        [__print_sent__(t, attr) for t in token.rights]
        print "}",
    return __print_sent__(sent.root, token_attr)


def match_tree(sentence, pattern):
    if not verify_pattern(pattern):
        raise PatternSyntaxException(pattern)

    def __match_node__(t, p):
        pat_node = p.pop(0) if p else ""
        return not pat_node or (__match_token__(t, pat_node, False) and __match_edge__(t.children,p))

    def __match_edge__(edges,p):
        pat_edge = p.pop(0) if p else ""
        if not pat_edge:
            return True
        elif not edges:
            return False
        else:
            for (t) in edges:
                if (__match_token__(t, pat_edge, True)) and __match_node__(t, list(p)):
                    return True
                elif pat_edge == "**" and __match_edge__(t.children, ["**"] + p):
                    return True
        return False
    return __match_node__(sentence.root, pattern.split("/"))


def find_tokens(sentence, pattern):
    if not verify_pattern(pattern):
        raise PatternSyntaxException(pattern)

    def __match_node__(t, p, tokens):
        pat_node = p.pop(0) if p else ""
        res = not pat_node or (__match_token__(t, pat_node, False) and (not p or __match_edge__(t.children, p, tokens)))
        if res and not p:
            tokens.append(t)
        return res

    def __match_edge__(edges,p, tokens):
        pat_edge = p.pop(0) if p else ""
        if pat_edge:
            for (t) in edges:
                if __match_token__(t, pat_edge, True):
                    if not __match_node__(t, list(p), tokens) and pat_edge == "**":
                        __match_edge__(t.children, ["**"] + p, tokens)
    result_tokens = []
    __match_node__(sentence.root, pattern.split("/"), result_tokens)
    return result_tokens
