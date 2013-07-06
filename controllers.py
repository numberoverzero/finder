import ujson
from finder import parsers


def process_card(card, scale=10, split=''):
    '''
    Pass 'left' or 'right' when processing a split card.
    Processes and updates all additional fields (cmc, loyalty, tilde rules) on a card
    that is already populated with basic data like mana cost, name, oracle rules, etc.
    '''
    card.processed_ascii_name = parsers.ascii_card_name(card.name)
    card.processed_cmc = parsers.cmc(card.cost, scale=scale, split=split)
    card.processed_colors = parsers.colors(card.color, card.cost)
    card.processed_power = parsers.power_toughness(card.power, scale=scale)
    card.processed_toughness = parsers.power_toughness(card.toughness, scale=scale)
    card.processed_loyalty = parsers.loyalty(card.type, card.toughness, scale=scale)

    type, subtype = parsers.types(card.type, split=split)
    card.processed_types = type
    card.processed_subtypes = subtype
    card.processed_tilde_rules = parsers.tilde_rules(card.name, card.oracle_rules)
