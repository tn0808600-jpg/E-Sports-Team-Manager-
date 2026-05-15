from flask import Flask, render_template
import sqlite3
app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('E-Sports Team Manager.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')

def index():
    conn = get_db_connection()
    players = conn.execute('''
        SELECT p.In_Game_Name, p.Role, t.Team_Name 
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
    
    return render_template('Index.html', players=players, gears=gears, results=results)

if __name__ == '__main__':
    app.run(debug=True)
    