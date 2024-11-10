from flask import Flask, render_template, jsonify, session

app = Flask(__name__)

# Game Data
location = {
    'entrance':{
            'name': 'The Temple Entrance',
            'description': 'A grand archway leads into a dark and mysterious temple.',
            'directions':{'north': 'hallway'},
        },
        'hallway': {
            'name': 'a dimly lit Hallway',
            'description': 'Torches flicker on the walls, casting long shadows. There are doors to the east and west.',
            'directions': {'east': 'chamber', 'west': 'treasury', 'south': 'entrance'},
        },
        'chamber': {
            'name': 'The Treasury',
            'description': 'This is where the legendary teasure is said to be hidden!',
            'directions': {'east': 'hallway'},
            # Add treasure and challenges here later

        'hallway':{
            'name': 'The legendary treasure'
            'description': 'You enter a large open room with a chest directly in the centre of the room with only the light from the moon ligthin the ground in front of you, unaware of the dangers lurking in front of you'
            'directions': {'west': 'hallway', 'north': 'mysterious statue', 'south': 'an open chest'},
        }
        },
    }

# --- Flask Routes ---
@app.route("/", method = ["GET", "POST"])
def index():
    return render_template("index.html")



if __name__ == "__main__":
    start_game()