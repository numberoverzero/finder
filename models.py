from finder import db


class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    multiverse_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Text)
    color = db.Column(db.Text)
    type = db.Column(db.Text)
    set = db.Column(db.Text)
    rarity = db.Column(db.Text)
    power = db.Column(db.Text)
    toughness = db.Column(db.Text)
    oracle_rules = db.Column(db.Text)
    flavor_text = db.Column(db.Text)
    watermark = db.Column(db.Text)
    number = db.Column(db.Integer)
    artist = db.Column(db.Text)
    rulings = db.Column(db.Text)

    processed_ascii_name = db.COlumn(db.Text)
    processed_cmc = db.Column(db.Integer)
    processed_colors = db.Column(db.Text)
    processed_power = db.Column(db.Integer)
    processed_toughness = db.Column(db.Integer)
    processed_loyalty = db.Column(db.Integer)
    processed_types = db.Column(db.Text)
    processed_subtypes = db.Column(db.Text)
    processed_tilde_rules = db.Column(db.Text)


card_fields = [
    'multiverse_id',
    'name',
    'cost',
    'color',
    'type',
    'set',
    'rarity',
    'power',
    'toughness',
    'oracle_rules',
    'flavor_text',
    'watermark',
    'number',
    'artist',
    'rulings',
    'processed_ascii_name',
    'processed_cmc',
    'processed_colors',
    'processed_power',
    'processed_toughness',
    'processed_loyalty',
    'processed_types',
    'processed_subtypes',
    'processed_tilde_rules',
]

returnable_card_fields = {
    'id': 'multiverse_id',
    'name': 'name',
    'cost': 'cost',
    'type': 'type',
    'set': 'set',
    'rarity': 'rarity',
    'power': 'power',
    'toughness': 'toughness',
    'rules': 'oracle_rules',
    'flavor': 'flavor_text',
    'watermark': 'watermark',
    'number': 'number',
    'artist': 'artist',
    'rulings': 'rulings',
    'ascii_name': 'processed_ascii_name',
    'cmc': 'processed_cmc',
    'colors': 'processed_colors',
    'loyalty': 'processed_loyalty',
}


db.create_all()
