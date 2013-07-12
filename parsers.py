import unicodedata
import re

_non_decomp_replacements = {
    0xc6: u'Ae',
    0xe6: u'ae'
}
_numbers = u''.join(map(str, range(10)))  # Filter for numbers in cmc
_pow_tough_include = '-0123456789'  # Filter for power and toughness once weird stuff is removed
_pos_half = unichr(0xbd)  # Unicode '1/2' character, used in unhinged power/toughness
_neg_half = u'-' + _pos_half  # Negative of previous
_half_s = u'Half'  # Used in unhinged mana costs
_split_pattern = u'(\([2wubrg]/[wubrg]\))'  # Split (2/g), (u/w) etc mana costs
_tiny_colors = u'bgruw'
_full_colors = {
    u'white': u'w',
    u'blue': u'u',
    u'black': u'b',
    u'red': u'r',
    u'green': u'g'
}
_extra_minus_pattern = u'-(?!\d+)'  # Matches minus signs not followed by a number


def ascii_card_name(card_name):
    card_name = _remove_accents(card_name)
    card_name = _replace_non_decomposable_unicode(card_name)
    return card_name


def power_toughness(types, value, scale=10):
    '''
    Returns power or toughness as an int.  x, *, etc are treated as 0.
    NOTE: due to unhinged's 1/2 power, toughness thing, all values are scaled by 10 so values can be stored
    as integers.  When querying these values, multiply the input by 10 to properly compare them, and divide by 10
    when returning them.
    '''
    if u'creature' not in types.lower():
        return None
    return _creature_stat(value.strip(), scale=scale)


def loyalty(types, toughness, scale=10):
    '''
    Loyalty is only valid for creatures with the planeswalker type.
    Their loyalty is equal to their toughness.
    Even though loyalty is currently whole numbers, uses the same scaling as power, toughness, and mana cost.
    I wouldn't put it past WotC to add half loyalty in the next Un-set.
    '''
    if u'planeswalker' not in types.lower():
        return None
    return _creature_stat(toughness.strip(), scale=scale)


def tilde_rules(name, oracle_rules):
    '''
    If the card's rules refer to itself, such as "When Foo comes into play..." this will return a string of rules
    with those self-refereces replaced with tildes: "When ~ comes into play..."
    This is a common search pattern when looking for cards with a particular effect.
    '''
    if name not in oracle_rules:
        return None
    return re.sub(unicode(name), u"~", unicode(oracle_rules), re.UNICODE)


def cmc(cost, scale=10, split=''):
    '''
    Pass 'left' or 'right' for getting one half of the cmc of a split card.
    Returns the converted mana cost of a spell as an integer.
    NOTE: due to unhinged's 1/2 mana cost (Little Girl, #74257) all values are scaled by 10 so values can be stored
    as integers.  When querying these values, multiply the input by 10 properly compare them, and divide by 10
    when returning them.
    '''
    cost = _split(cost, split=split)

    #Dictionary since python2.x doesn't have nonlocal keyword
    total = 0

    # Split matching comes before halfs.  Otherwise, 'Half(b/w)' would
    # break when the '(' got chopped from procesing Half.
    # This still won't return an honest value for some half split cards (which don't exist yet):
    # Half(2/b) -> HalfWW -> W, total=5 -> '', total=15 (5 from HalfW, 10 from W)
    def split_match(match):
        group = match.group(0)
        if u'2' in group:
            return u'ww'
        else:
            return u'w'

    # Simple replace with 'W' or 'WW' which will count as 1 or 2, respectively
    cost = re.sub(_split_pattern, split_match, cost)

    while _half_s in cost:
        half_index = cost.index(_half_s)
        # Can't just use replace since we have the get the character after 'Half' as well
        cost = cost[0:half_index] + cost[half_index + len(_half_s) + 1:]
        total += scale / 2
    cost = cost.lower()

    # Drop Everything but [0-9wubrg] since other characters have cmc 0
    cost = u''.join(c for c in cost if c in _numbers+_tiny_colors)

    # Count up color characters
    for c in cost:
        if c in _tiny_colors:
            total += scale
    # Drop color characters
    cost = u''.join(c for c in cost if c in _numbers)

    # At this point we've dropped splits, variables, halves, and color characters.
    # We should only have integers left, so convert and add
    # If there's nothing left, it was all variable mana cost
    if cost:
        total += scale * int(cost)
    return total


def colors(colors, cost):
    '''
    Returns the colors of a card.
    Cards with explicit colors (eg. Pact of Negation) do not check mana cost for color.
    The input for pact of negation should be 'Blue', '0'

    NOTE: Ghost Fire (gatherer says it's colorless) is not properly parsed by this function,
        since its Color is '' and its Cost is 'R'
    '''
    calc_colors = set()
    # Handle cards with explicit colors
    if colors:
        for raw_color in colors.split(u'/'):
            color = raw_color.strip().lower()
            calc_colors.add(_full_colors[color])
    elif cost:
        for char in cost:
            if char.lower() in _tiny_colors:
                calc_colors.add(char.lower())
    return u''.join(sorted(calc_colors))


def types(string, split=''):
    '''
    Pass 'left' or 'right' for getting one half of the cmc of a split card.
    Returns the types and subtypes of a card, as split by the first u'-' found.
    Multiple subtypes are split on spaces.
    Ex: 'Land - Urza's Power-Plant' -> ["Land", ("Urza's", "Power-Plant")]
    '''
    string = _split(string, split=split)
    types = string.split('-', 1)
    if len(types) < 2:
        types.append(u'')
    type, subtypes = types
    return type.strip(), subtypes.strip()


def _remove_accents(input_str):
    nfkd_form = unicodedata.normalize("NFKD", unicode(input_str))
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


def _replace_non_decomposable_unicode(input_str):
    return input_str.translate(_non_decomp_replacements)


def _split(string, split=''):
    '''Pass 'left' or 'right' for getting one half of the cmc of a split card.'''
    if u'//' not in string:
        return string

    split = split.lower() or u''
    split = unicode(split)

    if split == u'left':
        string = string.split(u'//', 1)[0].strip()
    elif split == u'right':
        string = string.split(u'//', 1)[1].strip()
    else:
        raise ValueError(u"split must be u'left' or u'right' (got '{}'}".format(split))
    return string


def _creature_stat(string, scale=10):
    '''
    Returns power or toughness as an int.  x, *, etc are treated as 0.
    NOTE: due to unhinged's 1/2 power, toughness thing, all values are scaled by 10 so values can be stored
    as integers.  When querying these values, multiply the input by 10 to properly compare them, and divide by 10
    when returning them.
    '''
    total = 0
    if _neg_half in string:
        total -= scale / 2
        string.replace(_neg_half, u'')
    if _pos_half in string:
        total += scale / 2
        string.replace(_pos_half, u'')
    filtered_string = u''.join(c for c in string if c in _pow_tough_include)
    # Drop dangling minus signs, as in "4-*" -> "4-"
    filtered_string = re.sub(_extra_minus_pattern, u'', filtered_string)
    if filtered_string:
        #If we filter everything out, it was all wildcards/already accounted for
        total += scale * int(filtered_string)
    return total
