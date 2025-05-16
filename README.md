# Flask Football Statistics Dashboard

This project is a Flask-based web application designed to display football statistics, including tournaments, matches, and goal scorers. It also provides interactive charts for visualizing data such as top goal scorers, matches per year, and goals by minute range.

---

## Features

- **Tournaments Table**: Displays a list of football tournaments.
- **Matches Table**: Shows detailed match information, including teams, scores, date, and location.
- **Goal Scorers Table**: Lists players who scored goals, along with details like the team, minute, and match.
- **Interactive Charts**:
  - Pie chart for top goal scorers.
  - Bar chart for matches per year.
  - Heatmap-style chart for goals by minute range.
- **Country Performance Chart**: Displays goals scored by a selected country per year.

---

## Project Structure
flash_assignment/ 
    ├── app/ 
    │ ├── init.py # Flask app factory and database initialization 
    │ ├── controllers/ 
    │ │ └── routes.py # Application routes 
    │ ├── models/ 
    │ │ ├── tournament.py # Tournament model 
    │ │ ├── matches.py # Matches model 
    │ │ └── goal_scorers.py # Goal scorers model 
    │ ├── templates/ 
    │ │ └── home.html # Main HTML template 
    │ ├── static/ 
    │ │ ├── style.css # Custom CSS for styling 
    │ │ └── charts.js # JavaScript for Chart.js 
    │ └── football.db # SQLite database 
    ├── venv/ # Virtual environment 
    ├── requirements.txt # Python dependencies 
    └── README.md # Project documentation

---

## Installation

### Prerequisites
- Python 3.8 or higher
- Flask
- SQLite

### Steps
1. Clone the repository:
   git clone https://github.com/tarekaust/flash_assignment-III.git
   cd flash_assignment
   

2. Create a virtual environment:
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
    pip install -r requirements.txt

4. Initialize the database:
    flask shell
    >>> from app import db
    >>> db.create_all()
    >>> exit()

5. Run the application:
    flask run

6. Open your browser and navigate to:
    http://127.0.0.1:5000/

### Usage
Viewing Data
    Tournaments: Displays a list of tournaments with their IDs and names.
    Matches: Shows match details in a scrollable table. The total number of matches is displayed below the table.
    Goal Scorers: Lists players who scored goals, along with match details.
Charts
    Top Goal Scorers: A pie chart showing the distribution of goals among top players.
    Matches Per Year: A bar chart visualizing the number of matches played each year.
    Goals by Minute Range: A heatmap-style chart showing the distribution of goals scored in different minute ranges.
Country Performance
    Select a country to view its performance (goals scored per year) in a dynamically generated chart.

### Models
Tournament Model
    class Tournament(db.Model):
        __tablename__ = 'tournaments'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)

Match Model
    class Match(db.Model):
        __tablename__ = 'matches'
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        home_team = db.Column(db.String, nullable=False)
        away_team = db.Column(db.String, nullable=False)
        home_score = db.Column(db.Integer, nullable=True)
        away_score = db.Column(db.Integer, nullable=True)
        date = db.Column(db.Date, nullable=True)
        match_city = db.Column(db.String, nullable=True)
        match_country = db.Column(db.String, nullable=True)
        tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), nullable=True)

Goal Scorer Model
    class GoalScorer(db.Model):
        __tablename__ = 'goal_scorers'
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        home_team = db.Column(db.String, nullable=False)
        away_team = db.Column(db.String, nullable=False)
        team_scored = db.Column(db.String, nullable=False)
        scorer = db.Column(db.String, nullable=False)
        minute = db.Column(db.Integer, nullable=False)
        match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=False)
        date = db.Column(db.Date, nullable=True)

### API Endpoints
/
    Method: GET
    Description: Displays the main dashboard with tables and charts.
    Technologies Used
    Backend: Flask
    Frontend: HTML, CSS, JavaScript (Chart.js)
    Database: SQLite
    Charting Library: Chart.js

### Future Enhancements
    Add user authentication for personalized dashboards.
    Implement search and filter functionality for tables.
    Add more advanced visualizations (e.g., line charts, scatter plots).
    Integrate with a live football API for real-time data updates.

### License
    This project is licensed under the MIT License. See the LICENSE file for details.
