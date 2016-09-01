import unittest
from grammaregex import match_tree, find_tokens, verify_pattern, PatternSyntaxException
import spacy

# _sentence will be used throughout the all tests as it is time-consuming to create it.
# The fact of time-consumption is also reason for keeping all tests in single module file
_sentence = None


def setUpModule():
    nlp = spacy.load("en")
    doc = nlp(u"Mrs. Robinson graduated from the Wharton School of the University of Pennsylvania in 1980.")
    global _sentence
    _sentence = next(doc.sents)


class TestVerifyPatternMethod(unittest.TestCase):
    def test_right_patterns(self):
        self.assertTrue(verify_pattern("VBD/prep/IN/pobj/NNP"))
        self.assertTrue(verify_pattern("VBD/*/IN/pobj/NNP"))
        self.assertTrue(verify_pattern("VBD/prep/IN/**/NNP"))
        self.assertTrue(verify_pattern("VBD/[prep,*]/IN/pobj/NNP"))
        self.assertTrue(verify_pattern("VBD/prep/IN/[pobj,prep]/*"))
        self.assertTrue(verify_pattern("*/**/IN/[pobj]/NNP"))

    def test_wrong_patterns(self):
        self.assertFalse(verify_pattern("*/***/IN/pobj/NNP"))
        self.assertFalse(verify_pattern("VBD/ prep/IN/pobj/NNP"))
        self.assertFalse(verify_pattern("VBD/prep/[IN,*,]/pobj/NNP"))
        self.assertFalse(verify_pattern("VBD/prep/IN/pobj/"))
        self.assertFalse(verify_pattern("/prep/IN/pobj/NNP"))
        self.assertFalse(verify_pattern("VBD/[prep/IN/pobj/NNP"))
        self.assertFalse(verify_pattern("[]"))


class TestMatchTreeMethod(unittest.TestCase):
    def test_match_wrong_pattern(self):
        with self.assertRaises(PatternSyntaxException):
            match_tree(_sentence, "")

    def test_match_simple_patterns(self):
        self.assertTrue(match_tree(_sentence, "VBD/prep/IN/pobj/NNP"))

    def test_not_match_simple_patterns(self):
        self.assertFalse(match_tree(_sentence, "VBD/prep/IN/pobj/VBD"))

    def test_match_pattern_with_stars(self):
        self.assertTrue(match_tree(_sentence, "VBD/prep/IN/pobj/*"))
        self.assertTrue(match_tree(_sentence, "VBD/prep/*/pobj/NNP"))
        self.assertTrue(match_tree(_sentence, "VBD/**/DT"))
        self.assertTrue(match_tree(_sentence, "VBD/**/*"))

    def test_not_match_pattern_with_stars(self):
        self.assertFalse(match_tree(_sentence, "VBD/*/DT/pobj/*"))
        self.assertFalse(match_tree(_sentence, "VBD/**/DT/pobj/*"))

    def test_match_with_lists(self):
        self.assertTrue(match_tree(_sentence, "VBD/prep/IN/*/[NNP,DT]"))
        self.assertTrue(match_tree(_sentence, "VBD/prep/IN/[pobj,prep,*]/NNP"))

    def test_not_match_with_lists(self):
        self.assertFalse(match_tree(_sentence, "VBD/prep/IN/pobj/[IN,DT]"))
        self.assertFalse(match_tree(_sentence, "VBD/**/IN/[pobj,prep]/DT"))


class TestFindTokensMethod(unittest.TestCase):

    def test_find_wrong_pattern(self):
        with self.assertRaises(PatternSyntaxException):
            match_tree(_sentence, "*//[]")

    def test_find_simple_patterns(self):
        self.assertListEqual(["School"],
                             [x.orth_ for x in find_tokens(_sentence, "VBD/prep/IN/pobj/NNP")])

    def test_not_find_simple_patterns(self):
        self.assertListEqual([],
                             [x.orth_ for x in find_tokens(_sentence, "VBD/prep/IN/pobj/VBD")])

    def test_find_pattern_with_stars(self):
        self.assertListEqual(["School", "1980"],
                             [x.orth_ for x in find_tokens(_sentence, "VBD/prep/IN/pobj/*")])
        self.assertListEqual(["School"],
                             [x.orth_ for x in find_tokens(_sentence, "VBD/prep/*/pobj/NNP")])
        self.assertListEqual(["the", "the"],
                             [x.orth_ for x in find_tokens(_sentence, "VBD/**/DT")])
        self.assertListEqual(["Robinson", "Mrs.", "from", "School", "the", "Wharton", "of", "University", "the", "of", "Pennsylvania", "in", "1980", "."],
                             [x.orth_ for x in find_tokens(_sentence, "VBD/**/*")])

    def test_not_match_pattern_with_stars(self):
        self.assertListEqual([],
                             [x.orth_ for x in find_tokens(_sentence, "VBD/*/DT/pobj/*")])
        self.assertListEqual([],
                             [x.orth_ for x in find_tokens(_sentence, "VBD/**/DT/pobj/*")])

    def test_match_with_lists(self):
        self.assertListEqual(["School"],
                             [x.orth_ for x in find_tokens(_sentence, "VBD/prep/IN/*/[NNP,DT]")])
        self.assertListEqual(["School"],
                             [x.orth_ for x in find_tokens(_sentence, "VBD/prep/IN/[pobj,prep,*]/NNP")])

    def test_not_match_with_lists(self):
        self.assertListEqual([],
                             [x.orth_ for x in find_tokens(_sentence, "VBD/prep/IN/pobj/[IN,DT]")])
        self.assertListEqual([],
                             [x.orth_ for x in find_tokens(_sentence, "VBD/**/IN/[pobj,prep]/DT")])

if __name__ == '__main__':
    unittest.main()

