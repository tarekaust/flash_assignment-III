from app import db
from datetime import date

class Match(db.Model):
    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    home_team = db.Column(db.String, nullable=False)
    away_team = db.Column(db.String, nullable=False)
    home_score = db.Column(db.Integer, nullable=True)
    away_score = db.Column(db.Integer, nullable=True)
    tournament = db.Column(db.Integer, nullable=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), nullable=True)
    date = db.Column(db.String, nullable=True)
    match_city = db.Column(db.String, nullable=True)
    match_country = db.Column(db.String, nullable=True)

    def __repr__(self):
        return (
            f"<Match id={self.id} home_team={self.home_team} away_team={self.away_team} "
            f"home_score={self.home_score} away_score={self.away_score} "
            f"tournament_id={self.tournament_id} date={self.date} "
            f"match_city={self.match_city} match_country={self.match_country}>"
        )