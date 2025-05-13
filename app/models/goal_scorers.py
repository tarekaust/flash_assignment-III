from app import db
from datetime import date

class GoalScorer(db.Model):
    __tablename__ = 'goal_scorers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    home_team = db.Column(db.String, nullable=False)
    away_team = db.Column(db.String, nullable=False)
    team_scored = db.Column(db.String, nullable=False)
    scorer = db.Column(db.String, nullable=False)
    minute = db.Column(db.Integer, nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=False)
    date = db.Column(db.String, nullable=True)

    def __repr__(self):
        return (
            f"<GoalScorer id={self.id} home_team={self.home_team} away_team={self.away_team} "
            f"team_scored={self.team_scored} scorer={self.scorer} minute={self.minute} "
            f"match_id={self.match_id} date={self.date}>"
        )