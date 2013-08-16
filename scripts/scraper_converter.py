'''
Usage:
  python scraper_converter.py scraped.db

Processes the cards scraped using the gatherer downloader and adds sane attributes fields for querying
(int pow/toughness, cmc) and saves the output to the app's database location.

Card attributes are saved according to finder.models.Card
'''

import os
import sqlsoup

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

def convert(indb, scale=10):
    '''Convert each entry in indb using various parsers and save to outdb'''
    from finder import db as dst
    src = sqlsoup.SQLSoup('sqlite:///{}'.format(indb))

    rows = src.MTGCardInfo.all()
    n = len(rows)
    notify_count = 10
    notify_interval = 100 / notify_count
    last = -notify_interval
    for i, row in enumerate(rows):
        convert_row(row, dst, scale=scale)
        if (100 * i / n) / notify_interval > last:
            last = (100 * i / n) / notify_interval
            print("{}% ({} / {})".format(last * notify_interval, i, n))
    print("100% ({} / {})".format(n, n))
    print("\nSaving changes...")
    dst.session.commit()
    print("Saved!\n")


def convert_row(row, dst, scale=10):
    '''Convert a src row into one or more dst cards'''
    from finder import util
    name = util.sanitize(row.name)
    attrs = {dkey: getattr(row, skey) for skey, dkey in field_conversion.iteritems()}
    # Split card, process both halves
    if u'//' in name:
        for side in sides:
            dst.session.add(to_card(attrs, scale=scale, split=side))
    else:
        dst.session.add(to_card(attrs, scale=scale))


def to_card(attrs, scale=10, split=''):
    '''attrs is a dictionary whose keys are finder.model.Card attributes.'''
    from finder import controllers, models
    card = models.Card(**attrs)
    controllers.process_card(card, scale=scale, split=split)
    return card

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='sqlite db to load from (gatherer downloader format)')

    args = parser.parse_args()
    convert(args.input, scale=10)
