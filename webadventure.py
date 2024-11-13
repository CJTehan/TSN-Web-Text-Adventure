from flask import Flask, render_template, request, session, jsonify
import copy

app = Flask(__name__)
app.secret_key = 'Your_Secret_Key'  

locations = {
    'entrance': {
        'name': 'The Temple Entrance',
        'description': 'A grand stone archway leads into the ancient temple.',
        'location_items': ['torch', 'map']
    },
    
}

original_locations = copy.deepcopy(locations)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        
        session.clear()
        session['location'] = 'entrance'
        session['inventory'] = []
        session['message'] = ''
        
        
        print("Initial location data being passed to template:", locations['entrance'])
        return render_template('index.html', location=locations['entrance'], inventory=session['inventory'], message='')
    
    elif request.method == 'POST':
        data = request.get_json()   
        action = data.get('action') if data else None
        
        print(f"Action received in index: {action}")
        
        if not action:
            return jsonify({'message': 'No action provided.'}), 400
        
        response = process_action(action)
        if response:
            return response
        else:
            return jsonify({'message': 'Action could not be processed.'}), 500


def show_intro():
    '''Displays the game's introduction'''
    message = (
        'Welcome to the Adventure of the Hidden Treasure!\n'
        'You are an intrepid explorer seeking a legendary treasure hidden deep within an ancient temple.\n'
        'Your journey will be fraught with peril, but the rewards are immeasurable.\n'
        'Good luck!'
    )
    return jsonify({'message': message})  

def show_current_location(location):
    '''Displays the description of the current location'''
    location_data = locations[location].copy()
    location_data['current_location'] = location
    location_data['message'] = f'You have moved to {location_data["name"]}'
    location_data['location_items'] = locations[location].get('location_items', [])
    return jsonify(location_data)

def process_action(action):
    '''Process the player's action and returns a jsonify response'''
    if action == 'restart':
        session.clear()
        session['location'] = 'entrance'
        
        global locations
        locations = copy.deepcopy(original_locations)
        
        return show_current_location('entrance')
    
    elif action == 'quit':
        return jsonify({'message': 'Game Over. Thanks for playing!'})
    
    elif action.startswith('go'):
        direction = action.split(' ')[1]
        return move_player(direction)
    
    elif action == 'take':
        item = request.get_json().get('item')
        return take_item(item)
    
    elif action == 'inventory':
        return show_inventory()
    
    else:
        return jsonify({'message': 'Invalid action.'})

def move_player(direction):
    '''Moves the player to a new location if possible'''
    current_location = session.get('location')
    
    if direction == 'north' and current_location == 'entrance':
        new_location = 'hallway' 
        session['location'] = new_location
        return show_current_location(new_location)
    else:
        return jsonify({'message': f"You can't go {direction} from here."})

def take_item(item):
    '''Adds an item to the player's inventory if possible'''
    current_location = session.get('location')
    location_items = locations[current_location].get('location_items', [])
    
    if item in location_items:
        session['inventory'].append(item)
        location_items.remove(item)
        return jsonify({'message': f'You took the {item}.'})
    else:
        return jsonify({'message': f'{item} is not available to take here.'})

def show_inventory():
    '''Displays the player's inventory'''
    inventory = session.get('inventory', [])
    return jsonify({'message': f"Inventory: {', '.join(inventory) if inventory else 'Empty'}"})

if __name__ == '__main__':
    app.run(debug=True)