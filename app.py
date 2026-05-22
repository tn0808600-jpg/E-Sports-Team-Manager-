import os
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


DB_PATH = "/home/rapeepat/esport/E-Sports Team Manager.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    players = conn.execute('''
        SELECT p.Player_ID, p.In_Game_Name, p.Role, t.Team_Name 
        FROM Players p 
        LEFT JOIN Teams t ON p.Team_ID = t.Team_ID
        ORDER BY p.In_Game_Name ASC
    ''').fetchall()
    
    gears = conn.execute('''
        SELECT p.In_Game_Name, g.Category, g.Brand, g.Model 
        FROM Gears g 
        JOIN Players p ON g.Player_ID = p.Player_ID
        ORDER BY p.In_Game_Name ASC
    ''').fetchall()

    results = conn.execute('''
        SELECT tr.Tournament_Name, t.Team_Name, mr.Placement, mr.Prize_Won 
        FROM Match_Results mr 
        JOIN Teams t ON mr.Team_ID = t.Team_ID 
        JOIN Tournaments tr ON mr.Tournament_ID = tr.Tournament_ID
        ORDER BY tr.Tournament_Name ASC
    ''').fetchall()
    conn.close()
    return render_template('index.html', players=players, gears=gears, results=results)

@app.route('/append', methods=['GET', 'POST'])
def append():
    if request.method == 'POST':
        ingame_name = request.form.get('ingame_name')
        role = request.form.get('role')
        team_id = request.form.get('team_id') or None

        conn = get_db_connection()
        try:

            conn.execute(
                'INSERT INTO Players (In_Game_Name, Role, Team_ID) VALUES (?,?,?)',
                (ingame_name, role, team_id)
            )
            conn.commit()
        finally:
            conn.close()
        return redirect(url_for('index'))

    conn = get_db_connection()
    teams = conn.execute('SELECT Team_ID, Team_Name FROM Teams').fetchall()
    conn.close()
    return render_template('append.html', teams=teams)

@app.route('/edit/<int:player_id>', methods=['GET', 'POST'])
def edit(player_id):
    conn = get_db_connection()
    if request.method == 'POST':
        ingame_name = request.form.get('ingame_name')
        role = request.form.get('role')
        team_id = request.form.get('team_id') or None

        try:

            conn.execute('''
                UPDATE Players 
                SET In_Game_Name = ?, Role = ?, Team_ID = ?
                WHERE Player_ID = ?
            ''', (ingame_name, role, team_id, player_id))
            conn.commit()
        finally:
            conn.close()
        return redirect(url_for('index'))

    player = conn.execute('SELECT * FROM Players WHERE Player_ID = ?', (player_id,)).fetchone()
    teams = conn.execute('SELECT Team_ID, Team_Name FROM Teams').fetchall()
    conn.close()
    
    if player is None:
        return "Player Not Found", 404

    return render_template('edit.html', player=player, teams=teams)

@app.route('/delete/<int:player_id>')
def delete(player_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Players WHERE Player_ID = ?', (player_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
