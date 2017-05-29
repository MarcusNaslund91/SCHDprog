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


""" Defines ship meta data and operational conditions """
class Ship:
    pass
    # User input (store):
        #ship_prop = {
#            'L_WL' : ?,  # m
#            'B_C' : ?,  # m
#            'm_LDC' : ?,  # kg
#            'Beta_04' : ?  # degrees
#            'H_T' : ?  # m,  Total hull height
#            'T_C' : ? # m, Canoe depth
#            }
        # Operational condition:
            # 'V' : ?,  # knots
            # Operations class (give user choices)
            
    # Methods:
        # Calculate craft mode (planing or displacement)
            # craft_V_LWL_ratio = V / math.sqrt(L_WL)
            # if V / math.sqrt(L_WL) < 5:
            #    craft_mode = 2
            # else:
            #    craft_mode = 1
            
    # Output: 
        # craft_mode
  
      
""" Available materials and their respective properties """
class MaterialsLibrary:
    pass
    # Input: 
        # Structural member type, Choosen material label.
    
    # Store:
        # Material label,
        # Yield strength, 
        # Tensile strenth, 
        # Elastic modulus,
        # Shear modulus,
        # Density
    
    # Output: 
        # Every structural member type gets associated with a material.

        
""" Defines and configures the structural model from user input, including topology.
    Calculates the weight of the vessel and the CoG.
"""
class Structure:
    pass
    # Input:
        # Longitudinal location of member (d)
        # Vertical location of member (d)
        # Spacing between two frames (d)
        # Spacing between two girders (d)
        
    # Methods:
        # Define topology (first model):  
        # Calculate weight:
            # Panels:
                # Area multilied by tickness
            # stiffeners:
                # Cross-section area multiplied by length.
        # Calculate CoG:
            # Adds the mass and centre of gravity of every structural member, 
            # then divide it by the total mass.
    
    # Output:
        # Ship weight
        # CoG


""" Defines what type of stiffener that will be analysed and gives it a 
    nomenclature as a identifier.
    Q: Calculates the actual stress?
"""
class Stiffener(Structure):
    pass
    # Input:
        # Stiffener type: girder, longitudinal, frame, bulkhead, deck.
        # Stiffener position (bottom, bottom & side, side, deck, superstructure)
    
    # Methods:
        # Assign nomenclature:
            # Type: frame = fr, longitudinal = L
            # ID nr: 1,2,3 ... n, from aft.
            # Panel span identifier: A-Z from aft (longi), 1 - n from bottom.(frame)
    
    # Output: Nomenclature


""" Defines the hull, deck and superstructure shell properties. 
    Contains a plating object, width distribution over a normalized length, 
    location according to the evaluating rules.
"""
class Shell(Structure):
    pass
    # Input:
        # Variables for 'Width distribution over normalized length'
        # Panel location (bottom, bottom & side, side, deck, superstructure)
    
    # Methods:
        # Calculate width distribution over normalized length
    
    # Output:
        # Width distribution over normalized length

""" Defines the panel dimensions according to the choosen rules and gives it a
    nomenclature as a identifier. Sends the information to the rules calculator.
"""
class Panel(Shell):
    pass
    # Input: 
        # Structure.'Girder spacing, frame spacing, stiffener spacing.'
        # Structure.'design location', Structure.Shell.panel_location
    
    # Methods:
        # Define panel dimensions according to choosen rules...
        # ... e.g. limited by stiffeners and/or chine boundaries accoring to ISO.
        # Define nomenclature:
            # Longtitudinal position: A-Z from aft
            # Transverse position: 1 - n from bottom
            # Minor divisions: a-z
    
    # Output: 
        # Panel width, Panel length
        # Nomenclature
    

""" Contains all the availible plates from manufacturers. The user can choose
    from between different thicknesses. The panel is then sent to the complience
    calculator.
"""
class PlatingLibrary:
    pass
    # Input: User chooses from available plating thicknesses
    
    #Q: Are all materials availible for all plate thicknesses?... 
    #Q: ... e.g can the material be choosen from the material library... 
    #Q: ... or do they have to stored together?
    
    # Store:
        # Plating label,
        # Material,?
        # Thickness
    
    # Output: Every panel gets associated with a thickness to be used in the...
    #         ... comparison of minimum vs offered.


""" Library containing structural profiles for e.g. stiffeners, girders
    and frames. User can choose between a set of available extrusions
    or define their own for machining.
"""
class ProfileLibrary:
    pass
    # Input: 
        # Structure.Stiffener.Nomenclature
        # Choosen profile label
    
    # Methods: 
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
        # Calculted web area
        # Cross-section area
    
    # Output: 
        # Profile properties gets associated with Structure.Stiffener.Nomenclature.


""" User defined machined profiles """
class Machined(ProfileLibrary):
    pass
    # User Input:
        # Type (flat-bar, T-shaped, L-shaped, C-shaped)
        # Flange width,
        # Flange thickness,
        # Web height,
        # Web thickness
    
    # Calculate:
        # Section modulus
        # Web area
        # Cross-section Area
        # Give random label name
    
    # Output: 
        # Profile properties gets associated with Structure.Stiffener.Nomenclature.

""" Stores the different structural rules for designing the structural 
    properties and arrangment of the vessel, e.g. ISO12215, DNV, ABS and LR.
"""
class Rules:
    pass
    # Input: 
        # Chosen rules
        # Variables common to all rules (tricky to know for this version)
    

""" Calculates structural requirements according to ISO 12215 """
class ISO12215(Rules):
    pass
    # Input: 
        # Panel:
            # Ship
            # MaterialsLibrary
            # Structure
            # Structure.Shell
            # Structure.Shell.Panel
        # Stiffener (minimum req):
            # Ship
            # MaterialsLibrary
            # Structure
            # PlatingLibrary (panel thickness)
            # Structure.Stiffener
        # Stiffener (maximum prop):
            # Structure.Stiffener
            # MaterialLibrary
            # ProfileLibrary
            # Actual stress calculator
        
    # Methods:
        # List of elements (panel and stiffener)
        # Calculate minimal structural requirements for each member
        # Check maximum proportions between dimensions within a stiffener
    
    # Output:
        # Required panel thickness
        # Minimum panel thickness
        # Minimum stiffener web area 
        # Minimum stiffener section modulus
        # Dimension proportions
        


""" Creates and updates all the relevant information that the user is interested in,
    such as structural arrangment report, graphs of the optimization etc.
"""
class Report:
    pass
    # Create graphs, messages, spreadsheets and all calculation outputs.
    # Input:
        # Ship
        # MaterialsLibrary
        # Structure
        # Structure.Shell
        # Structure.Shell.Panel
        # PlatingLibrary
        # Structure.Stiffener
        # ProfileLibrary
        # ISO12215
        
    # Methods:
        # List outputs with units
        # Create spreadsheets containing each structural member and the SA.
        # Add any important messages (different modes e.g. user mode, developer mode?)
        # Create graphs from e.g. the optimization or to help with other things.
        
    # Output:
        # Calculation outputs
        # Spreadsheets
        # Messages
        # Graphs

""" User interface, receive user inputs and initialize the relevant objects 
    using the user input. 
"""
class Designer:
    pass
    # receive inputs
    
    # Methods:
        # Designer.CreateStructReport(Structure,ISO12215,Report)
        """
            This method will check if the structure has all the dependent 
            variables already calculated, if not it will follow a particular 
            workflow in order to populate all the necessary object attributes, 
            after which will call a method inside the Report object to generate 
            the output data in the chosen format (ie: excel spreadsheet).
        """
        # Change/update topology
        # Change/update profiles
        # Change/update material
        # Change/update optimization
    
    # Output:
        # Outputs from other classses, highlighting the changes if there are any.
       
   
""" Typical user workflow:
   
    1.	Define Vessel Properties and Operational Conditions
    2.	Define Materials
     Q:  Do you assign materials to each member type?
     
    3.	Define Profiles
     Q:  What part of the profiles do you define?
     
    4.	Define topology (stiffeners, girders and bulkheads position, 
    orientation using ASV nomenclature) and Areas (Side, Bottom, Superstructure, etc..)
     Q:  In what order do you define the topology?
     
    5.	Calculate Pressures
    6.	Calculate Minimum vs offered for plating and reinforcements
    7.	Evaluate passing and failing locations
    8.	Iterate from 4 onward
    9.	Iterate from 3 onward
    10.	Iterate from 2 onward
    11.	Calculate Weight and CoG
    12.	Produce Report
"""

        
""" Check input variables for typos, negatives and other errors, and promts the
    user to correct the value.   
"""
class GlobalVariableCheck:
    pass
    # Input:
        # All variables
    
    # Methods:
        # Check input variables for typos
        # Check input variables for negatives
        # Check input variables for other errors...
        
    # Output:
        # Error messages and promt user to fix.
       

""" User chooses between different optimization methods depending on what type
    of structural member needs to be optimized.
"""
class Optimizer:
    pass
    # User chooses optimization method
    # User configures chosen method
    # Run optimization

