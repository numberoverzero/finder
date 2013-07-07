'''
Usage:
  python scraper_converter.py scraped.db formatted.db

Processes the cards scraped using the gatherer downloader and adds sane attributes fields for querying
(int pow/toughness, cmc) and saves the output to a new sqlite database.

Card attributes are saved according to finder.models.Card
'''

import sqlsoup
from finder import (
    controllers,
    models,
    util
)

sides = [u'left', u'right']

# raw field name => models.Card attribute name
# note that these are only the fields we care about (printedname, printedrules etc are omitted)
field_conversion = {
    'id': 'multiverse_id',
    'name': 'name',
    'cost': 'cost',
    'color': 'color',
    'type': 'type',
    'set': 'set',
    'rarity': 'rarity',
    'power': 'power',
    'toughness': 'toughness',
    'rules': 'oracle_rules',
    'flavor': 'flavor_text',
    'watermark': 'watermark',
    'cardnum': 'number',
    'artist': 'artist',
    'rulings': 'rulings'
}


def convert(indb, outdb, scale=10):
    '''Convert each entry in indb using various parsers and save to outdb'''
    src = sqlsoup.SQLSoup('sqlite:///{}'.format(indb))

    dst = None
    raise NotImplementedError('dst is None!')

    rows = src.MTGCardInfo.all()
    for row in rows:
        convert_row(row, dst, scale=scale)


def convert_row(row, dst, scale=10):
    '''Convert a src row into one or more dst cards'''
    name = util.sanitize(row.name)
    attrs = {dkey: getattr(row, skey) for skey, dkey in field_conversion.iteritems()}
    # Split card, process both halves
    if u'//' in name:
        for side in sides:
            dst.add(to_card(attrs, scale=scale, split=side))
    else:
        dst.add(to_card(attrs, scale=scale))


def to_card(attrs, scale=10, split=''):
    '''attrs is a dictionary whose keys are finder.model.Card attributes.'''
    card = models.Card(**attrs)
    controllers.process_card(card, scale=scale, split=split)
    return card

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='sqlite .db database to load from (should use gatherer downloader save format')
    parser.add_argument('output', help='filename to save well-formed card sqlite .db database to')

    args = parser.parse_args()
    convert(args.input, args.output, scale=10)
