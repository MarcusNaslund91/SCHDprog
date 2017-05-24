#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
...

"""

# import sys
import logging

#from schprog import __version__

__author__ = "Marcus Naslund"
__copyright__ = "Marcus Naslund"
__license__ = "none"

_logger = logging.getLogger(__name__)

""" Defines ship meta data """
class Ship:
    pass
    # User input:
        #ship_prop = {
#            'L_WL' : ?,  # m
#            'B_C' : ?,  # m
#            'm_LDC' : ?,  # kg
#            'V' : ?,  # knots
#            'Beta_04' : ?  # degrees
#            'H_T' : ?  # m,  Total hull height
#            'T_C' : ? # m, Canoe depth
#            }
    # Methods:
        # Calculate craft mode (planing or displacement)
            # craft_V_LWL_ratio = V / math.sqrt(L_WL)
            # if V / math.sqrt(L_WL) < 5:
            #    craft_mode = 2
            # else:
            #    craft_mode = 1


""" Defines and configures the structural model, including topology. """
class Structure:
    pass
    # Configure structural model from user input:
        # Define topology (first model):
            # Longitudinal location (d)
            # Vertical location (d)
            # Spacing between two frames (d)
            # Spacing between two girders (d)


""" Defines the what type of stiffener that will be analysed and gives it a 
    nomenclature as a identifier.
"""
class Stiffener(Structure):
    pass
    # Define stiffener type: girder, longitudinal, frame, bulkhead, deck.
    # Methods:
        # Define nomenclature:
            # Type: frame = fr, longitudinal = L
            # ID nr: 1,2,3 ... n, from aft.
            # Panel span identifier: A-Z from aft (longi), 1 - n from bottom.(frame)



""" Defines the hull, deck and superstructure shell properties. 
    Contains a plating object, width distribution over a normalized length, 
    location according to the evaluating rules.
    Q: Calculates the actual stress?
"""
class Shell(Structure):
    pass
    # Shell configuration from user input:
        # Width distribution over normalized length,
        # Panel location (bottom, bottom & side, side, deck, superstructure)
        

""" Defines the panel dimensions according to the choosen rules and gives it a
    nomenclature as a identifier. Sends the information to the rules calculator.
"""
class Panel(Shell):
    pass
    # Methods:
        # Define panel dimensions according to choosen rules...
        # ... e.g. limited by stiffeners and/or chine boundaries accoring to ISO.
        # Define nomenclature:
            # Longtitudinal position: A-Z from aft
            # Transverse position: 1 - n from bottom
            # Minor divisions: a-z
    

""" Contains all the availible plates from manufacturers. The user can choose
    from between different thicknesses. The panel is then sent to the complience
    calculator.
"""
class PlatingLibrary:
    pass
    # User chooses from available plating thicknesses
    
    #Q: Are all materials availible for all plate thicknesses?... 
    #Q: ... e.g can the material be choosen from the material library... 
    #Q: ... or do they have to stored together?
    
    # Store:
        # Plating label,
        # Material,?
        # Thickness


""" Library containing structural profiles for e.g. stiffeners, girders
    and frames. User can choose between a set of available extrusions
    or define their own for machining.
"""
class ProfileLibrary:
    pass
    # user chooses a set of profiles from:
        # Extrusions
        # Machined
    

""" Available extruded profiles """
class Extrusions(ProfileLibrary):
    pass
    # Store extruded profiles:
        # Profile label,
        # Flange width,
        # Flange thickness,
        # Web height,
        # Web thickness,
        # Type (flat-bar, T-shaped, L-shaped, C-shaped)
        # Section modulus
        # Cross-section area


""" User defined machined profiles """
class Machined(ProfileLibrary):
    pass
    # User defines:
        # Type (flat-bar, T-shaped, L-shaped, C-shaped)
        # Flange width,
        # Flange thickness,
        # Web height,
        # Web thickness
    
    # Calculate:
        # Section modulus
        # Web area
        # Cross-section Area        


""" Available materials and their respective properties """
class MaterialsLibrary:
    pass
    # Store:
        # Material label,
        # Yield strength, 
        # Tensile strenth, 
        # Elastic modulus,
        # Shear modulus,
        # Density


class Rules:
    pass
    # User chooses which rules to apply


class ISO12215(Rules):
    pass
    # Calculates structural requirements according to ISO 12215
    # Methods:
        # List of elements (panel and stiffener)


class Report:
    pass
    #Create graphs, messages, spreadsheets and all calculation outputs.


""" User interface, receive user inputs and initialize the relevant objects 
    using the user input. 
"""
class DesignEnvironment:
    pass
    # receive inputs
    # initialize relevant objects
    # Methods:
        # Designer.CreateStructReport(Structure,ISO12215,Report)
        
        
class GlobalVariableCheck:
    pass
    # Methods:
        # Check input variables for typos, negatives and other errors...
        # ... and promt user to correct the value.


class Optimizer:
    pass
    # User chooses optimization method
    # User configures chosen method
    # Run optimization

