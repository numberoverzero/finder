from finder import db


class Card(db.Model):
    __tablename__ = 'finder-cards'
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

    calc_converted_mana_cost = db.Column(db.Integer)
    calc_colors = db.Column(db.Text)
    calc_power = db.Column(db.Integer)
    calc_toughness = db.Column(db.Integer)
    calc_type = db.Column(db.Text)
    calc_subtypes = db.Column(db.Text)
