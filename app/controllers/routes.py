from flask import Blueprint, render_template, request
from app import db
from app.models.matches import Match
from app.models.goal_scorers import GoalScorer
from app.models.tournament import Tournament
import matplotlib.pyplot as plt
import io
import base64
from collections import defaultdict

main = Blueprint('main', __name__)

# Helper: Pie chart for top goal scorers
def get_pie_chart_data():
    goals_by_player = db.session.query(GoalScorer.scorer, db.func.count().label('goals'))\
        .group_by(GoalScorer.scorer).order_by(db.func.count().desc()).limit(10).all()
    return [r[0] for r in goals_by_player], [r[1] for r in goals_by_player]

# Helper: Bar chart for matches per year
def get_bar_chart_data():
    year_counts = defaultdict(int)
    for match in Match.query.all():
        year = match.date[:4] if match.date else 'Unknown'
        year_counts[year] += 1
    return list(year_counts.keys()), list(year_counts.values())

# Helper: Heatmap-like bar chart for goals by minute range
def get_heatmap_data():
    minute_ranges = ['0–15', '16–30', '31–45', '46–60', '61–75', '76–90', '91+']
    minute_buckets = [0]*7
    for scorer in GoalScorer.query.all():
        try:
            m = int(scorer.minute)
            if m <= 15: minute_buckets[0] += 1
            elif m <= 30: minute_buckets[1] += 1
            elif m <= 45: minute_buckets[2] += 1
            elif m <= 60: minute_buckets[3] += 1
            elif m <= 75: minute_buckets[4] += 1
            elif m <= 90: minute_buckets[5] += 1
            else: minute_buckets[6] += 1
        except:
            continue
    return minute_ranges, minute_buckets

# Helper: Line chart for goals per year by selected country
def get_country_goals_chart(selected_country):
    country_goal_data = db.session.query(
        db.func.extract('year', Match.date).label('year'), db.func.count().label('goals')
    ).filter(Match.match_country == selected_country).group_by('year').all()

    years = [str(r[0]) for r in country_goal_data]
    goals = [r[1] for r in country_goal_data]

    fig, ax = plt.subplots()
    ax.plot(years, goals, marker='o')
    ax.set_title(f'Goals Scored by {selected_country} per Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Goals')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf-8')

# Main route for home page
@main.route('/', methods=['GET', 'POST'])
def home():
    tournaments = Tournament.query.all()
    matches = Match.query.all()
    goal_scorers = GoalScorer.query.all()

    # Charts
    pie_labels, pie_data = get_pie_chart_data()
    bar_labels, bar_data = get_bar_chart_data()
    heatmap_labels, heatmap_data = get_heatmap_data()

    # Dropdown country
    selected_country = request.args.get('selected_country', None)
    country_chart_image = None
    country_matches = []
    country_scorers = []
    country_tournaments = []

    if selected_country:
        country_chart_image = get_country_goals_chart(selected_country)
        country_matches = Match.query.filter(Match.match_country == selected_country).all()
        match_ids = [m.id for m in country_matches]
        country_scorers = GoalScorer.query.filter(GoalScorer.match_id.in_(match_ids)).all()

        # Fetch tournaments related to those matches
        tournament_ids = list(set([m.tournament_id for m in country_matches if m.tournament_id]))
        country_tournaments = Tournament.query.filter(Tournament.id.in_(tournament_ids)).all()

    country_list = list(set([match.match_country for match in matches if match.match_country]))

    return render_template('home.html',
                           tournaments=tournaments,
                           matches=matches,
                           goal_scorers=goal_scorers,
                           pie_labels=pie_labels,
                           pie_data=pie_data,
                           bar_labels=bar_labels,
                           bar_data=bar_data,
                           heatmap_labels=heatmap_labels,
                           heatmap_data=heatmap_data,
                           country_list=country_list,
                           selected_country=selected_country,
                           country_chart_image=country_chart_image,
                           country_matches=country_matches,
                           country_scorers=country_scorers,
                           country_tournaments=country_tournaments)