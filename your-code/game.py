# define rooms and items game room

couch = {
    "name": "couch",
    "type": "furniture",
}

door_a = {
    "name": "door a",
    "type": "door",
}

key_a = {
    "name": "key for door a",
    "type": "key",
    "target": door_a,
}

piano = {
    "name": "piano",
    "type": "furniture",
}

game_room = {
    "name": "game room",
    "type": "room",
}

outside = {
  "name": "outside"
}

# define rooms and items bedroom1

queen_bed = {
    "name": "queen bed",
    "type": "furniture",
}

door_b = {
    "name": "door b",
    "type": "door",
}

door_c = {
    "name": "door c",
    "type": "door",
}

key_b = {
    "name": "key for door b",
    "type": "key",
    "target": door_b,
}

bedroom_1 = {
    "name": "bedroom 1",
    "type": "room",
}

outside_bedroom_1 = {
  "name": "outside bedroom 1"
}

# define rooms and items bedroom2

dresser = {
    "name": "dresser",
    "type": "furniture",
}

double_bed = {
    "name": "double bed",
    "type": "furniture",
}

key_c = {
    "name": "key for door c",
    "type": "key",
    "target": door_c,
}

door_d = {
    "name": "door d",
    "type": "door",
}

key_d = {
    "name": "key for door d",
    "type": "key",
    "target": door_d,
}

bedroom_2 = {
    "name": "bedroom 2",
    "type": "room",
}

outside_bedroom_2 = {
  "name": "outside bedroom 2"
}

# define rooms and items living room

dining_table = {
    "name": "dining table",
    "type": "furniture",
}



living_room = {
    "name": "living room",
    "type": "room",
}

outside_living_room = {
  "name": "outside living room"
}

all_rooms = [game_room, bedroom_1, bedroom_2, living_room, outside]

all_doors = [door_a, door_b, door_c, door_d]


# define which items/rooms are related game room

object_relations = {
    "game room": [couch, piano, door_a],
    "piano": [key_a],
    "outside": [door_d],
    "door a": [game_room, bedroom_1],
    "bedroom 1":[queen_bed, door_b, door_c],
    "queen bed":[key_b],
    "door b":[bedroom_1, bedroom_2],
    "door c":[bedroom_1, living_room],
    "bedroom 2":[dresser, double_bed, door_b],
    "double bed":[key_c],
    "dresser":[key_d],
    "living room":[dining_table, door_d],
    "door d":[living_room, outside]   
           
}


# define game state. Do not directly change this dict. 
# Instead, when a new game starts, make a copy of this
# dict and use the copy to store gameplay state. This 
# way you can replay the game multiple times.

INIT_GAME_STATE = {
    "current_room": game_room,
    "keys_collected": [],
    "target_room": outside
}


def linebreak():
    """
    Print a line break
    """
    print("\n\n")



#input_user = input('choose a language among portoguese (pt), italian (it), german (de), french (fr), spanish (es), indonesian (id)')

input_user = input('choose a language between english (en), spanish (es)')

def tr(sentence):
    global input_user
    from translate import Translator
    translator= Translator(to_lang= input_user)
    translation = translator.translate(sentence)
    
    return translation

tr('hello')


def start_game():
    """
    Start the game
    """
    print(tr("You wake up on a couch and find yourself in a strange house with no windows which you have never been to before. You don't remember why you are here and what had happened before. You feel some unknown danger is approaching and you must get out of the house, NOW!"))
    play_room(game_state["current_room"])

def play_room(room):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either 
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        print(tr("Congrats! You escaped the room!"))
    else:
        print(tr("You are now in " + room["name"]))
        intended_action = input(tr("What would you like to do? Type 'explore' or 'examine'?")).strip()
        if intended_action in ("explore", "explorar"):
            explore_room(room)
            play_room(room)
        elif intended_action in ("examine", "examinar"):
            examine_item(input(tr("What would you like to examine?")).strip())
        else:
            print(tr("Not sure what you mean. Type 'explore' or 'examine'."))
            play_room(room)
        linebreak()

def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [i["name"] for i in object_relations[room["name"]]]
    print(tr("You explore the room. This is " + room["name"] + ". You find " + ", ".join(items)))

def get_next_room_of_door(door, current_room):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """
    connected_rooms = object_relations[door["name"]]
    for room in connected_rooms:
        if(not current_room == room):
            return room

def examine_item(item_name):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been 
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"]
    next_room = ""
    output = None
    
    for item in object_relations[current_room["name"]]:
        if(item["name"] == item_name):
            output = "You examine " + item_name + ". "
            if(item["type"] == "door"):
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        have_key = True
                if(have_key):
                    output += "You unlock it with a key you have."
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output += "It is locked but you don't have the key."
            else:
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += "You find " + item_found["name"] + "."
                else:
                    output += "There isn't anything interesting about it."
            print(tr(output))
            break

    if(output is None):
        print(tr("The item you requested is not found in the current room."))
    
    if(next_room and input(tr("Do you want to go to the next room? Enter 'yes' or 'no'")).strip() in ('yes', 'si')):
        play_room(next_room)
    else:
        play_room(current_room)


game_state = INIT_GAME_STATE.copy()

start_game()