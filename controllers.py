from finder import (
    models,
    parsers,
    util
)


def process_card(card, scale=10, split=''):
    '''
    Pass 'left' or 'right' when processing a split card.
    Processes and updates all additional fields (cmc, loyalty, tilde rules) on a card
    that is already populated with basic data like mana cost, name, oracle rules, etc.
    '''
    card.processed_ascii_name = parsers.ascii_card_name(card.name)
    card.processed_cmc = parsers.cmc(card.cost, scale=scale, split=split)
    card.processed_colors = parsers.colors(card.color, card.cost)
    card.processed_power = parsers.power_toughness(card.type, card.power, scale=scale)
    card.processed_toughness = parsers.power_toughness(card.type, card.toughness, scale=scale)
    card.processed_loyalty = parsers.loyalty(card.type, card.toughness, scale=scale)

    type, subtype = parsers.types(card.type, split=split)
    card.processed_types = type
    card.processed_subtypes = subtype
    card.processed_tilde_rules = parsers.tilde_rules(card.name, card.oracle_rules)

    card.processed_scale = scale

    # Catch Ghostfire's colorless oddity
    if card.name == u'Ghostfire':
        card.processed_colors = u''


def with_fields(card, fields, precision=1):
    '''
    returns a dictionary of card attributes filtered using the {key: bool} dictionary fields.
    keys are entries in finder.models.returnable_card_fields, such as:
        fields= {
            'colors': True,
            'cmc': True,
        }
    Any omitted fields are assumed False.  Some fields are formatted for clarity.
    '''

    filtered_results = {}
    for key, field in models.returnable_card_fields.iteritems():
        if fields.get(key, False):
            value = getattr(card, field, None)
            filtered_results[key] = value

    #=================
    # post-processing
    #=================

    if 'rulings' in filtered_results:
        text = filtered_results['rulings']
        text = util.sanitize(text)
        filtered_results['rulings'] = text.split(u'\n')

    def scale_value(field):
        if field in filtered_results:
            value = filtered_results[field]
            formatted_value = util.format_scaled_value(value, card.processed_scale, precision=precision)
            filtered_results[field] = formatted_value

    scale_value('cmc')
    scale_value('power')
    scale_value('toughness')

    return filtered_results
