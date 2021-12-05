"""
A printable Christmas ornament
that consists of a parametrised cable stayed bridge model

Bridges, as the pinackle of the art of engineering, do OFF CAUSE make
the best christmas ornament shapes, as they NATURALLY spread feelings 
of happyness, accomplishment and safety, and symbolise the bringing 
together of people, the bridging of otherwise unsurmountable odds, of 
both new beginnings and the safety to return home and of hope*.
Who would not want all of that on their christmas tree?

You can choose:
-scale/ height of tower
-number of cable stays
-number of towers

to be printed laying flat on the side

please excuse weird code bits, I used the challenge to try out OOP for the first time.
*source: the internet. Apparently, bridges can symbolize pretty much whatever you want.
"""
import numpy as np
from stl import mesh
from BridgeElements import Bridge

"""----------------- please choose parameters ------------------"""
span_length = 5 # cm
stays = 3   # number of cable stays
towers = 3  # number of towers - min 2, max 5 for reasonable dimensions
"""--------------------------------------------------------------"""

thickness=0.2  # cm, thickness of the model
cable_thickness=0.2 #cm, width of the cables
deck_thickness = span_length*0.1    #cm, width of the deck
x=span_length*towers

# first tower with attachment point for a beautiful satin ribbon 
# to hang it on the tree
this_bridge=Bridge(span_length,thickness,deck_thickness,stays,cable_thickness)
this_tower=this_bridge.tower()
this_deck=this_bridge.deck()
these_cables=this_bridge.cables()
attachment_point=this_bridge.nissehue()
bridge_ornament = mesh.Mesh(np.concatenate([this_tower.data.copy(),this_deck.data.copy(),these_cables.data.copy(),attachment_point.data.copy(),]))

# add the other towers
for i in range(towers-1):
    bridge_ornament.x+=span_length
    next_bridge=Bridge(span_length,thickness,deck_thickness,stays,cable_thickness)
    next_tower=next_bridge.tower()
    next_deck=next_bridge.deck()
    next_cables=next_bridge.cables()
    bridge_ornament = mesh.Mesh(np.concatenate([bridge_ornament.data.copy(),next_tower.data.copy(),next_deck.data.copy(),next_cables.data.copy()]))

# Write the mesh to file and inform user about size of print
bridge_ornament.save('bridge_ornament.stl')
print(f"The print will be {x}cm wide")