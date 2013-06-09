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

    calc_converted_mana_cost = db.Column(db.Integer)
    calc_colors = db.Column(db.Text)
    calc_power = db.Column(db.Integer)
    calc_toughness = db.Column(db.Integer)
    calc_type = db.Column(db.Text)
    calc_subtypes = db.Column(db.Text)

    def as_tabbed_value(self):
        '''Returns the column values separated by tabs for bulk-importing.'''
        return '\t'.join(
            self.id,
            self.multiverse_id,
            self.name,
            self.cost,
            self.color,
            self.type,
            self.set,
            self.rarity,
            self.power,
            self.toughness,
            self.oracle_rules,
            self.flavor_text,
            self.watermark,
            self.number,
            self.artist,
            self.calc_converted_mana_cost,
            self.calc_colors,
            self.calc_power,
            self.calc_toughness,
            self.calc_type,
            self.calc_subtypes,
        )


db.create_all()
