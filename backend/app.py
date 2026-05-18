from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import datetime
import os

app = Flask(__name__)
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS species (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            emoji TEXT NOT NULL,
            zone TEXT NOT NULL,
            zone_label TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')
    # Seed data if empty
    if conn.execute('SELECT COUNT(*) FROM species').fetchone()[0] == 0:
        seed_data = [
            ("Blue Whale", "🐋", "shallow", "Sunlight Zone", "The largest animal on Earth, reaching up to 30 meters. Feeds almost exclusively on tiny krill despite its massive size."),
            ("Clownfish", "🐠", "shallow", "Sunlight Zone", "Famous for living among sea anemone tentacles. Immune to the anemone's sting due to a protective mucus coating."),
            ("Sea Turtle", "🐢", "shallow", "Sunlight Zone", "Ancient mariners of the ocean, sea turtles have existed for over 100 million years and can live up to 80 years."),
            ("Hammerhead Shark", "🦈", "shallow", "Sunlight Zone", "Their wide-set eyes give them a 360-degree view. The hammer-shaped head also helps detect electrical fields from prey."),
            ("Giant Squid", "🦑", "mid", "Twilight Zone", "Can grow up to 13 meters long. Has the largest eyes in the animal kingdom — up to 30cm in diameter — to see in dim light."),
            ("Lanternfish", "🐟", "mid", "Twilight Zone", "One of the most abundant vertebrates on Earth. Uses bioluminescent photophores along its body to communicate and camouflage."),
            ("Vampire Squid", "🦑", "mid", "Twilight Zone", "Despite its name, it's neither a squid nor an octopus. It can invert its cloak of webbed arms to expose spine-like projections."),
            ("Oarfish", "🐡", "mid", "Twilight Zone", "The world's longest bony fish, reaching up to 11 meters. Rarely seen alive — likely the origin of sea serpent legends."),
            ("Anglerfish", "🎣", "deep", "Midnight Zone", "Uses a bioluminescent lure dangling from its head to attract prey in total darkness. Females are much larger than males."),
            ("Dumbo Octopus", "🐙", "deep", "The Abyss", "Named after Disney's Dumbo for its ear-like fins. Lives deeper than any other octopus — up to 7,000 meters down."),
            ("Barreleye Fish", "🐟", "deep", "Midnight Zone", "Has a transparent head filled with fluid. Its tubular eyes can rotate to look upward through its clear dome to spot prey."),
            ("Goblin Shark", "🦈", "deep", "Midnight Zone", "A living fossil unchanged for 125 million years. Has a protrusible jaw that shoots forward to snatch prey."),
        ]
        conn.executemany(
            'INSERT INTO species (name, emoji, zone, zone_label, description) VALUES (?,?,?,?,?)',
            seed_data
        )
    conn.commit()
    conn.close()

@app.route('/api/species')
def get_species():
    conn = get_db()
    rows = conn.execute('SELECT * FROM species').fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/species/<zone>')
def get_species_by_zone(zone):
    conn = get_db()
    rows = conn.execute('SELECT * FROM species WHERE zone = ?', (zone,)).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'timestamp': datetime.datetime.utcnow().isoformat()})

@app.route('/metrics')
def metrics():
    conn = get_db()
    total = conn.execute('SELECT COUNT(*) FROM species').fetchone()[0]
    conn.close()
    # Prometheus plain text format
    output = (
        "# HELP ocean_species_total Total number of species in the database\n"
        "# TYPE ocean_species_total gauge\n"
        f"ocean_species_total {total}\n"
        "# HELP ocean_api_up API health status\n"
        "# TYPE ocean_api_up gauge\n"
        "ocean_api_up 1\n"
    )
    return output, 200, {'Content-Type': 'text/plain; charset=utf-8'}
init_db()
if __name__ == '__main__':
   
    app.run(host='0.0.0.0', port=5000)
