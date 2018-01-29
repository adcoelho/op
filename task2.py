#!/usr/bin/python3

# For a new project purposes a simple hierarchical database was prepared.
# All data are kept in a single file. Each line inside the file contains single entity.
# Entities are placed in the random order inside the file.
# Format of the entity is as follow:
# {id:<entity_id>, key:<key_string>, value:<value_string>, parent:<parent_id>}
# where:
# <entity_id> - positive integer, unique throughout the database
# <key_string> - key (string) of the entity (there may be many entities with the same key)
# <value_string> - value (string) of the entity (there may be many entities with the same value)
# <parent_id> - entity_id of the parent of the entity. If the entity is the main
#     entity (doesn't have a parent) the parent_id is equal 0
#     (there may be only one main entity in the database).

# As an example, a simple scratch of database for a car structure is presented here:

# {id:13, key:"car_body", value:"black", parent:3}
# {id:1, key:"car", value:"Opel Astra G", parent:0}
# {id:3, key:"bodywork", value:"kombi", parent:1}
# {id:64, key:"under_body", value:"34382SDF23", parent:1}
# {id: 4, key:"driving_system", value:"DFG324", parent:64}
# {id: 15, key:"wheel", value:"xxx", parent:4}
# {id:13, key:"engine", value:"disel 2.0 DTI", parent:3}
# {id:23, key:"screw", value:"M4", parent:13}
# {id:18, key:"bearing", value:"AX65", parent:13}
# {id:18, key:"bearing", value:"AAH", parent:13}
# {id: 17, key:"bearing", value:"GGH321D", parent:4}

# Prepare an application that displays (on the screen) the value_string for all entities
# that match a selector given as an argument. The selector may be a single
# key_string or a list of those keys. If a single key is given, the application
# should display value of the value_string field for all entities that contain
# the key in the key_string field. Basing on the above example, the following result
# should be displayed for "bearing" key given as an argument for the application:

# > python selprint.py bearing
# AX65
# AAH
# GGH321D

# In the case of usage of multiple key elements in the selector,
# the value of the value_string field for the last key will be displayed.
# All preceding keys are used to specify the search range, i.e. selector
# in the form "underbody bearing" should cause displaying all bearings which constitute the underbody element. As an example:
# > python selprint.py underbody bearing
# GGH321D

# Similarly, selector "underbody driving_system bearing" should display the same bearing:
# > python selprint.py underbody driving_system bearing
# GGH321D

# In addition, please estimate the time and memory consumption of your algorithm with usage of the Big O notation (http://en.wikipedia.org/wiki/Big_O_notation).

"""
    # Algorithm

    My initial idea was to have two structures:
    1. A tree - where every node would have knowledge of its parent
    2. A dictionary of keys -> nodes
    
    Let's consider n to be the number of entities.

    Then the algorithm would run as follows:
    1. On input we would fetch all bottom nodes - O(1)
    2. For every node, navigate the tree bottom up to see if they match the preceding keys. - O(height of the tree)
    2.1 If all preceding keys are matched print the value
    
    The algorithm itself would have a decent complexity but the tree creation would be costly. 
    We would have to find the right place and insert every node in the tree, this is O(log(n)) on average in a Binary tree.
    
    This one isn't binary so the complexity would be worse.

    The alternative I decided on was to have a dictionary where every position has {key, value} = {entity_id: entity}.

    The creation is an insert(O(1)) for every entity. -> O(n), where n is the number of entities

    Then the algorithm works the same way but, instead of navigating in a tree by following parent nodes I just check for the parent key in the entity object and access the dictionary.

    # Time Complexity

    The time complexity here can be divided in two possibilities, let's assume the following:
    - n is the database size
    - h is the tree height - on average a binary tree has height log(n) without aditional information on the data we cannot estimate the tree height
    - tk_n is the number of nodes with the target key

    * Single key query *

    Structure creation + Fetching target key nodes =
    O(n)               + O(1) * tk_n =
    O(n + tk_n)

    worst case scenario every node has the key we are looking for so the complexity would be O(n + n) = O(n)

    * Multiple key queries *

    Structure creation + Fetching target key nodes + navigating the tree to confirm the parent_keys * every target key node=
    O(n)               + O(1) * tk_n               + O(h) * tk_n =
    O(n)               + O(tk_n)                   + O(h x tk_n) =
    O(n + tk_n + h x tk_n)

    The complexity is linear at first sight with only the O(h x tk_n) step deserves further consideration.

    The worst case scenario would be a tree like

    key_A
    |
    key_A
    |
    key_A

    And a query like:
    > python selprint.py key_A key_A key_A

    Here the number of nodes with the target key and the height of the tree would both be equal to n.

    Then the complexity would be something like O(n^2).
    
    I don't know how realistic this case is and I'd warrant this is far from the average scenario

    # Spatial Complexity

    Regarding the memory used by the data structures we simply store every entity twice.
    
    All other variables are of a constant complexity.
    
    The memory consumption is therefore - O(2n) = O(n)

    PS.: A few notes and assumptions regarding the provided examples:
    1. the structure was not a valid json so I added double quotes around the keys
    2. one of the examples has the query `> python selprint.py underbody bearing` but the key is `under_body`
    3. there are entities with a duplicated id contradicting the initial description(id: 18)

"""

import json
import sys

from collections import deque

# Entity field names
ENTITY_ID = 'id'
KEY_STRING = 'key'
VALUE_STRING = 'value'
PARENT_ID = 'parent'


class Database(object):
    def __init__(self, filename):
        self._entities = {}
        self._keys_dict = {}

        # Above the root entity
        # this will come in handy when navigating the tree on line 128
        self._entities[0] = None

        with open(filename, 'r') as f:
            for line in f:
                entity = json.loads(line)

                # the entity id is unique
                self._entities[entity[ENTITY_ID]] = entity

                # there can be duplicated keys
                if entity[KEY_STRING] in self._keys_dict:
                    self._keys_dict[entity[KEY_STRING]].append(entity)
                else:
                    self._keys_dict[entity[KEY_STRING]] = [entity]

    def print_values(self, key, parent_keys):
        
        # Fetch every entity with the desired key
        for entity in self._keys_dict[key]:

            # Single key queries should be immediate - O(1)
            if not parent_keys:
                print(entity[VALUE_STRING])
            else:

                # we need to queue the other keys so that we can look for them one by one
                dq = deque(parent_keys)
                current_node = entity
                target_key = dq.pop()

                # start navigating up the tree
                while current_node:

                    # does this node have the key we are looking for?
                    if current_node[KEY_STRING] == target_key:

                        # if we don't need any more keys we can just print the value of the entity
                        if not len(dq):
                            print(entity[VALUE_STRING])
                            break
                        
                        # otherwise, let's look for the next one
                        else:
                            target_key = dq.pop()
                    
                    # this wasn't the node we were looking for so let's check its parent
                    current_node = self._entities[current_node[PARENT_ID]]


if __name__=='__main__':
    db = Database('./my_file.txt')
    args = sys.argv[1:]
    main_key = args[-1]

    if len(args) > 1:
        parent_keys = args[:-1]
    else:
        parent_keys = []

    db.print_values(main_key, parent_keys)
