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


db.create_all()
