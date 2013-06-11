import unittest

from finder import util
from finder import parsers


class UnicodeCardNameTests(unittest.TestCase):
    def setUp(self):
        self.old_root = util.get_root()
        util.set_root(__file__)

    def tearDown(self):
        util.set_root(self.old_root)

    def testAsciiCardNames(self):
        unicode_data = util.load_file('unicode_cards.txt')
        tests = []
        for line in unicode_data.split(u'\n'):
            if not line:
                continue
            original, expected = line.split(u',')
            tests.append((original.strip(), expected.strip()))

        for original, expected in tests:
            actual = parsers.ascii_card_name(original)
            try:
                assert actual == expected
            except AssertionError:
                print "Expected", expected
                print "Actual", actual


class PowerToughnessTests(unittest.TestCase):
    def _validate(self, string, expected_power, expected_toughness, scale=10):
        actual_power, actual_toughness = parsers.power_toughness(unicode(string), scale=scale)
        assert actual_power == int(expected_power * scale)
        assert actual_toughness == int(expected_toughness * scale)

    def testBasic(self):
        self._validate(u'1/2', 1, 2)

    def testSpace(self):
        self._validate(u'1/ 2', 1, 2)
        self._validate(u'1 /2', 1, 2)
        self._validate(u'1 / 2', 1, 2)

    def testHalfPower(self):
        string = u'1' + unichr(0xbd) + u'/' + u'2'
        self._validate(string, 1.5, 2)

    def testWildCards(self):
        self._validate('*+1/*', 1, 0)

    def testNegatives(self):
        string = u'4-*' + u'/' + u'-1'
        self._validate(string, 4, -1)

    def testAltWildCards(self):
        string = u'x+2 / x-2'
        self._validate(string, 2, -2)

    def testExponenetsIgnored(self):
        string = u'*' + unichr(0xb2) + u'/' + u'*' + unichr(0xb2)
        self._validate(string, 0, 0)

    def testFilterIllegalCharacters(self):
        string = '2badvalue/4nambla'
        self._validate(string, 2, 4)


class CMCTests(unittest.TestCase):
    def _validate(self, string, expected, scale=10, split='', raises=None):
        if raises:
            with self.assertRaises(raises):
                self._validate(string, expected, scale=scale, split=split, raises=None)
        else:
            actual = parsers.cmc(unicode(string), scale=scale, split=split)
            assert actual == int(expected * scale)

    def testBasic(self):
        self._validate('2', 2)

    def testHalf(self):
        self._validate('HalfW', 0.5)

    def testBrokenHalf(self):
        self._validate('Half(2/r)', 2, raises=AssertionError)

    def testSplitCosts(self):
        self._validate('(2/r)g(w/b)', 4)

    def testSplitCards(self):
        string = u"HalfW(2/g) // 123wubrg"
        left = 2.5
        right = 128
        self._validate(string, left, split='left')
        self._validate(string, right, split='right')

    def testSplitCardWithEmpty(self):
        string = u"// x"
        left = 0
        right = 0
        self._validate(string, left, split='left')
        self._validate(string, right, split='right')

    def testColoredMana(self):
        self._validate('wwuubbrrgg', 10)

    def testMultiDigit(self):
        self._validate('12345', 12345)

    def testNegativeCostsFail(self):
        self._validate('-10g', -9, raises=AssertionError)

    def testAllPatterns(self):
        string = '10000wwuub(2/g)(2/g)(r/b)HalfG'
        expected = 10000+5+2+2+1+0.5
        self._validate(string, expected)


class ColorsTests(unittest.TestCase):
    def _validate(self, colors, cost, expected, not_expected=None):
        if not_expected is None:
            not_expected = u''.join(c for c in u'wubrg' if c not in expected)
        actual = parsers.colors(unicode(colors), unicode(cost))
        for color in unicode(expected):
            assert color in actual
        for color in unicode(not_expected):
            assert color not in actual

    def testColor(self):
        self._validate('Blue', '', 'u')

    def testColorDoesNotUseCost(self):
        self._validate('Blue', 'gggg', 'u')

    def testMultipleColors(self):
        self._validate('Red/White/Blue', '', 'urw')

    def testOnlyCost(self):
        self._validate('', 'g', 'g')

    def testColorlessCosts(self):
        self._validate('', '2g', 'g')

    def testColorless(self):
        self._validate('', '', '')
        self._validate('', '10000', '')

    def testMultiColorCost(self):
        self._validate('', '2rg', 'gr')

    def testSplitColors(self):
        self._validate('', '(b/g', 'bg')


class TypesTests(unittest.TestCase):
    def _validate(self, string, expected_types, expected_subtypes, split=''):
        nonzero = lambda s: filter(bool, s)

        actual_types, actual_subtypes = parsers.types(unicode(string), split=split)

        actual_types = nonzero(actual_types.split(u' '))
        actual_subtypes = nonzero(actual_subtypes.split(u' '))

        assert len(actual_types) == len(expected_types)
        assert len(actual_subtypes) == len(expected_subtypes)

        for expected_type in expected_types:
            assert unicode(expected_type) in actual_types
        for subtype in expected_subtypes:
            assert unicode(subtype) in actual_subtypes

    def testNoSubtype(self):
        self._validate('Land', ['Land'], [])

    def testMultipleTypes(self):
        self._validate('Basic Land', ['Land', 'Basic'], [])

    def testSubtype(self):
        self._validate('Type-Sub', ['Type'], ['Sub'])

    def testSpaces(self):
        self._validate('Type -Sub', ['Type'], ['Sub'])
        self._validate('Type- Sub', ['Type'], ['Sub'])
        self._validate('Type - Sub', ['Type'], ['Sub'])

    def testMutipleSubtypes(self):
        self._validate('Basic - Sub1 Sub2', ['Basic'], ['Sub1', 'Sub2'])

    def testNoType(self):
        self._validate('- Subtype', [], ['Subtype'])

    def testHyphenSubtype(self):
        self._validate('- Sub-type', [], ['Sub-type'])

    def testSplitTypes(self):
        string = "Tribal Instant - Goblin // - Multiple Subtypes"
        left_types = ['Tribal', 'Instant']
        left_subtypes = ['Goblin']
        right_types = []
        right_subtypes = ['Multiple', 'Subtypes']
        self._validate(string, left_types, left_subtypes, split='left')
        self._validate(string, right_types, right_subtypes, split='right')
