from flask import Flask, render_template, request, session, jsonify, redirect, url_for

app = Flask(__name__)
app.secret_key = 'Your_Secret_Key'

# Game data
locations = {
    'entrance': {
        'name': 'The Temple Entrance',
        'description': 'A grand archway leads into a dark and mysterious temple',
        'directions': {'north': 'hallway'},
    },
    'hallway': {
        'name': 'A Dimly Lit Hallway',
        'description': 'Torches flicker on the walls, casting long shadows. There are doors to the east and west.',
        'directions': {'east': 'chamber', 'west': 'treasury', 'south': 'entrance'},
    },
    'chamber': {
        'name': 'The Treasury',
        'description': 'This is where the legendary treasure is said to be hidden!',
        'directions': {'west': 'hallway'},
    },
}

@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialise the game session
    if 'location' not in session:
        session['location'] = 'entrance'  # Set initial location
        session['inventory'] = []  # Initialise empty inventory
        session['message'] = ''  # Initialise empty message
        show_intro()  # Display the intro text

    if request.method == 'POST':
        # Handle actions submitted through forms
        action = request.form.get('action')
        if action == 'go':
            direction = request.form.get('direction')
            if direction:
                return process_action(f'go {direction}')  # Process 'go' action
        return process_action(action)  # Process other actions
    else:
        # Handle initial page load
        show_current_location()  # Display starting location info

    # Render the template with game data
    message = session.pop('message', '')  # Get and clear the message
    return render_template('index.html', location=locations[session['location']], inventory=session['inventory'], message=message)

# --- Game Functions ---
def show_intro():
    '''Displays the game's introduction'''
    message = '\nWelcome to the Adventure of the Hidden Treasure!\n' \
              'You are an intrepid explorer seeking a legendary treasure hidden deep within an ancient temple.\n' \
              'Your journey will be fraught with peril, but the rewards are immeasurable.\n' \
              'Good luck!\n'
    return jsonify({'message': message})

def show_current_location():
    '''Displays the description of the current location'''
    location_data = locations[session['location']].copy()
    location_data['current location'] = session['location']
    return jsonify(location_data)

def process_action(action):
    '''Process the player's action and returns a jsonify response'''
    if action == 'quit':
        return jsonify({'message': 'You have quit the game.'})
    elif action.startswith('go'):
        pass  # Placeholder for 'go' action handling
    elif action == 'take':
        pass  # Placeholder for 'take' action handling
    elif action == 'inventory':
        pass  # Placeholder for 'inventory' action handling
    else:
        return jsonify({'message': 'Invalid action.'})

def move_player(direction):
    '''Moves the player to a new location if possible'''
    location = session['location']
    new_location = locations[location]['directions'].get(direction)
    if new_location:
        return new_location
    else:
        print('You cannot go that way.')
        return location 

def take_item(item):
    '''Adds an item to the player's inventory if possible'''
    location = session['location']
    if 'items' in locations[location] and item in locations[location]['items']:
        session['inventory'].append(item)
        locations[location]['items'].remove(item)
        print(f'You take the {item}.')

def show_inventory():
    '''Displays the player's inventory'''
    inventory = session.get('inventory', [])
    if inventory:
        print('\nYour inventory:')
        for item in inventory:
            print(f'{item}')
    else:
        print('\nYour inventory is empty.')

if __name__ == '__main__':
    app.run(debug=True)

