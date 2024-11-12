from flask import Flask, render_template, request, session, jsonify, redirect, url_for

app = Flask(__name__)
app.secret_key = "webgame123"

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

        },
        'hallway':{
            'name': 'The legendary treasure',
            'description': 'You enter a large open room with a chest directly in the centre of the room with only the light from the moon lighting the ground in front of you, unaware of the dangers lurking in front of you.',
            'directions': {'west': 'hallway', 'north': 'mysterious statue', 'south': 'an open chest'},
        },
        
    }

# --- Flask Routes ---
@app.route("/", method = ["GET", "POST"])
def index():
    # Intialise the game session
    if "location" not in session:
        session["location"] = "entrance" # Set initial location
        session["inventory"] = [] # Initialise empty inventory
        session ["message"] = "" # Initialis empty message
        show_intro() # Display the intro text
    
    if request.method == "POST":
        # Handle actions submitted through forms
        action = request.form.get("action")
        if action == "go":
            direction = request.form.get("direction")
            if direction:
                return process_action(f"go {direction}") # Process go action
        return process_action(action) # process other actions
    else: # Request.method == "GET"
        # Handle initial page load
        show_current_location("entrance") # Display starting location info

    # Render the template with game data
    message = session.pop("message", "") # Get and clear the message
    return render_template("index.html", location = locations[session["location"]], inventory = session["inventory"], message = message)

# --- Game Function ---
def show_intro():
    """Displays the games intro"""
    message = "\nWelcome to the Adventure of the Hidden Treasure!\n" \
        "You are an intrepid explorer seeing a legendary treasure hidden deep within an ancient temple.\n"
    "Your journey will be fraught with peril, but the rewards are immeasurable.\n" \
    "Good Luck!\n"
    return jsonify({"message": message}) # Return a JSON response

# The current room
def show_current_location(location, locations):
    """Displays the players current location in the game"""
    location_data = locations[location].copy()
    location_data["current location"] = location
    return jsonify(location_data)

def process_action(action):
    """Process the players action and return a JSON response"""
    if action == "quit":
        message = "Thanks for playing!"
        return jsonify("all")
        
    elif action.startswith("go"):
        direction = action.split()[-1]
        app.route("/")
        

    elif action == "take":
        

    elif action == "inventory":

    else:
        return jsonify({"message": "Invalid Action"})


def move_player(direction):
    """Moves player to a new location if possible"""


def take_item():
    """Adds item to players inventory"""

def show_inventory(inventory):
    """Displays the players inventory"""




if __name__ == "__main__":
    app.run(debug = True)