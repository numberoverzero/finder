from finder import db


class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    multiverse_id = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer)
    power = db.Column(db.Text)
    toughness = db.Column(db.Text)

    artist = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Text, nullable=False)
    flavor_text = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    oracle_rules = db.Column(db.Text, nullable=False)
    rarity = db.Column(db.Text, nullable=False)
    set = db.Column(db.Text, nullable=False)
    type = db.Column(db.Text, nullable=False)
    watermark = db.Column(db.Text, nullable=False)
