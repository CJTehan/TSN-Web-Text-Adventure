import copy
from flask import Flask, render_template, request, session, jsonify, redirect, url_for

app = Flask(__name__)
app.secret_key = "webgame123"

# Game Data
locations = {
    'entrance':{
            'name': 'The Temple Entrance',
            'description': 'A grand archway leads into a dark and mysterious temple.',
            'directions':{'north': 'hallway'},
            "location_items": ["chest key"]
        },
        'hallway': {
            'name': 'a dimly lit Hallway',
            'description': 'Torches flicker on the walls, casting long shadows. There are doors to the east and west.',
            'directions': {'east': 'chamber', 'west': 'treasury', 'south': 'entrance'},
            "location_items": ["gold coin"]
        },
        'chamber': {
            'name': 'The Treasury',
            'description': 'This is approaching where the legendary teasure is said to be hidden but beware the potential dangers!',
            'directions': {'east': 'hallway'},
            "location_items": ["health potion"]
        },
        'temple throne':{
            'name': 'The legendary treasure',
            'description': 'You enter a large open room with a chest directly in the centre of the room with only the light from the moon lighting the ground in front of you, unaware of the dangers lurking in front of you.',
            'directions': {'west': 'hallway', 'north': 'mysterious statue', 'south': 'an open chest'},
            "location_items": ["sword of destiny"]
        },
    }

# Make a deep copy of the original locations to use for resetting
original_locations = copy.deepcopy(locations)

# --- Flask Routes ---
@app.route("/", methods = ["GET", "POST"])
def index():
    # Intialise the game session
    if request.method == 'GET':
        session.clear()
        session['location'] = 'entrance'
        session['inventory'] = []
        session['message'] = ''
        print("Initial location data being passed to template:", locations['entrance'])
        print("Type of location items:", type(locations['entrance']['location_items']))
        return render_template('index.html', location=locations['entrance'], inventory=session['inventory'], message='')
    elif request.method == 'POST':
        data = request.get_json()  # Use get_json() to read JSON data
        action = data.get('action') if data else None
        print(f"Action received in index: {action}")
        if not action:
            return jsonify({'message': 'No action provided.'}), 400
        response = process_action(action)
        if response:
            return response
        else:
            return jsonify({'message': 'Action could not be processed.'}), 500

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

# The current room with added changes trying to get the function to work through the page
def show_current_location(location, locations):
    """Displays the players current location in the game"""
    location_data = locations[location].copy()
    location_data["current location"] = location
    location_data["message"] = f"You have moved to {location_data["name"]}"
    location_data["location_items"] = locations[location]["location_items"]
    return jsonify(location_data)
    
def process_action(action):
    """Process the players action and return a JSON response"""
    if action == "restart":
        session.clear()
        session["location"] = "entrance"
# Reset the game locations to their original state
        global locations
        locations = copy.deepcopy(original_locations)
        return show_current_location("entrance")
    if action == "quit":
        session.clear()
        return jsonify({"message":"Thanks for playing!", "redirect": "/", "pause": 2})
        
    elif action.startswith("go"):
        direction = action.split("", 1)[1].lower()
        return move_player(direction)
        
    elif action == "get":
        # Button for get action
        item =request.json.get("item")
        if item:
            return take_item(item)
        return jsonify({"message": "Please specify an item to take."})
    elif action == "inventory":
        return show_inventory()
    else:
        return jsonify({"message": "Invalid action."})
    # Added necessary action processing for the functionality of the user actions - Conor

def move_player(direction):
    """Moves player to a new location if possible"""
    current_location = session.get("location")
    new_location = locations[current_location]["directions"].get(direction)
    if new_location:
        session['location'] = new_location  # Update the session with the new location
        return jsonify({"location": new_location, "message": f"You moved {direction} to {locations[new_location]["name"]}."})
    else:
        return jsonify({"message": "You cannot go that way."})

def take_item(item):
    """Adds item to players inventory"""
    current_location = session.get("location", "entrance")
    if "location_items" in locations[current_location] and item in locations[current_location]["location_items"]:
        inventory = session.get("inventory", [])
        inventory.append(item)
        session['inventory'] = inventory
        locations[current_location]['location_items'].remove(item)
        return jsonify({'message': f'You take the {item}.', 'inventory':inventory})
    else:
        return jsonify({'message': 'There is no such item here.'}) 

def show_inventory(inventory):
    """Displays the players inventory"""
    inventory = session.get("inventory", [])
    if inventory:
        inventory_str = "\n".join(f"- {item}" for item in inventory)
        return jsonify({"message": f"\nYour inventory:\n{inventory_str}"})
    else:
        return jsonify({"message": "\nYour inventory."})



if __name__ == "__main__":
    app.run(debug = True)