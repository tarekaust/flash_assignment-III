from collections import defaultdict
from sqlalchemy import extract, func
from app import db
from app.models.goal_scorers import GoalScorer
from app.models.matches import Match

def get_pie_chart_data():
    goals_by_player = db.session.query(
        GoalScorer.scorer,
        func.count().label('goals')
    ).group_by(GoalScorer.scorer).order_by(func.count().desc()).limit(10).all()

    return [r[0] for r in goals_by_player], [r[1] for r in goals_by_player]

def get_bar_chart_data():
    year_counts = defaultdict(int)
    for match in Match.query.all():
        year = match.date[:4] if match.date else 'Unknown'
        year_counts[year] += 1
    return list(year_counts.keys()), list(year_counts.values())

def get_heatmap_data():
    ranges = ['0–15', '16–30', '31–45', '46–60', '61–75', '76–90', '91+']
    buckets = [0]*7
    for scorer in GoalScorer.query.all():
        try:
            m = int(scorer.minute)
            if m <= 15:
                buckets[0] += 1
            elif m <= 30:
                buckets[1] += 1
            elif m <= 45:
                buckets[2] += 1
            elif m <= 60:
                buckets[3] += 1
            elif m <= 75:
                buckets[4] += 1
            elif m <= 90:
                buckets[5] += 1
            else:
                buckets[6] += 1
        except:
            continue
    return ranges, buckets

def get_country_goal_trend(country):
    result = db.session.query(
        extract('year', GoalScorer.date).label('year'),
        func.count().label('goals')
    ).filter(GoalScorer.team_scored == country)\
     .group_by('year').order_by('year').all()

    return [str(row.year) for row in result], [row.goals for row in result]

def get_country_list():
    countries = db.session.query(Match.home_team).distinct().all()
    return sorted(set(c[0] for c in countries))
