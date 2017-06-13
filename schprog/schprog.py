#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
...

"""

# import sys
import logging
import math
#from schprog import __version__

__author__ = "Marcus Naslund"
__copyright__ = "Marcus Naslund"
__license__ = "none"

_logger = logging.getLogger(__name__)


""" Defines ship meta data and operational conditions """
class Vessel:
    def __init__(self, L_WL, B_C, m_LDC, Beta_04, H_T, T_C, V, op_class):
        self.L_WL = L_WL
        self.B_C = B_C
        self.m_LDC = m_LDC
        self.Beta_04 = Beta_04 # range 10 - 30 degrees
        self.H_T = H_T
        self.T_C = T_C
        self.V = V
        self.op_class = op_class
        # TODO: add variable check


#   Calculate craft mode (planing = 1 or displacement = 2)
    def calc_craft_mode(self):
        #craft_V_LWL_ratio = self.V / math.sqrt(self.L_WL)
        if self.V / math.sqrt(self.L_WL) < 5:
            craft_mode = 2
        else:
            craft_mode = 1
        return craft_mode


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
    def __init__(self, material_label,
                 yield_strength,
                 tensile_strenth, 
                 elastic_modulus,
                 shear_modulus,
                 density
                 ):
        
        self.material_label = material_label
        self.yield_strength = yield_strength
        self.tensile_strenth = tensile_strenth 
        self.elastic_modulus = elastic_modulus
        self.shear_modulus = shear_modulus
        self.density = density

    def __repr__(self):
        return """
        material_label = %s
        yield_strength = %d
        tensile_strenth = %d
        elastic_modulus = %d
        shear_modulus = %d
        density = %d
        """ % (self.material_label,
               self.yield_strength,
               self.tensile_strenth, 
               self.elastic_modulus,
               self.shear_modulus,
               self.density
               )
        
    

    
    # Input: 
        # Structural member type, Choosen material label.
        
#    def choose_material(self, struc_mem_type):
#        self.struc_mem_type = struc_mem_type
        
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
    def __init__(self, s_frames, s_girders, nr_stiffeners):
        self.s_frames = s_frames
        self.s_girders = s_girders
        self.nr_stiffeners = nr_stiffeners
    
    def stiffener_equal_spacing(self):
        s_stiffener = self.s_girders / (1 + self.nr_stiffeners)
        return s_stiffener
    
    # Input:
        # Spacing between two frames (d)
        # Spacing between two girders (d)
        # Number fo stiffeners between two girders (d)
        
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
        # Spacing between two stiffeners
        # Ship weight
        # CoG




""" Defines what type of stiffener that will be analysed and gives it a 
    nomenclature as a identifier.
    Q: Calculates the actual stress?
"""
class Stiffener(Structure):
    def __init__(self, x, z, section, stiffener_type, stiffener_position, spans_panels):
        self.x = x
        self.z = z
        self.stiffener_type = stiffener_type
        self.stiffener_postition = stiffener_position
        self.spans_panels = spans_panels
        self.s = section.stiff_s
        self.l_u = section.s_frames

    def assign_nomenclature(self):
        if self.stiffener_type == 'longitudinal':
            nomenclature_1 = 'L'
            nomenclature_2 = input('stiffener location around vessel: ')
            nomenclature = '%s%s %s' % (nomenclature_1, nomenclature_2, self.spans_panels)
        elif self.stiffener_type == 'frame':
            nomenclature_1 = 'Fr'
            nomenclature_2 = input("frame number: ")
            nomenclature = '%s%s %s' % (nomenclature_1, nomenclature_2, self.spans_panels)
        else: # TODO: add further nomenclature
            pass
        return nomenclature
    
    def choose_material(self, stiffener_name, material_object):
        setattr(stiffener_name, 'material', material_object.material_label)
        setattr(stiffener_name, 'yield_strength', material_object.yield_strength)
        setattr(stiffener_name, 'tensile_strenth', material_object.tensile_strenth)
        setattr(stiffener_name, 'elastic_modulus', material_object.elastic_modulus)
        setattr(stiffener_name, 'shear_modulus', material_object.shear_modulus)
        setattr(stiffener_name, 'density', material_object.density)
        
        
    
    def choose_profile(self, stiffener_name, profile_name):
        setattr(stiffener_name, 'profile_label', profile_name.profile_label)
        setattr(stiffener_name, 'SM', profile_name.SM)
        setattr(stiffener_name, 'A_w', profile_name.A_w)
        setattr(stiffener_name, 't_w', profile_name.t_w)
        setattr(stiffener_name, 'type_', profile_name.type_)
        
        
        

        

    # Input:
        # Longitudinal location of member (d)
        # Vertical location of member (d)
        # Stiffener type: girder, longitudinal, frame, bulkhead, deck.
        # Stiffener position (bottom, bottom & side, side, deck, superstructure)
    
    # Methods:
        # Assign nomenclature:
            # Type: frame = fr, longitudinal = L
            # Frame nr: 1,2,3 ... n, from aft.
            # Position around the ship transvere/vertical - nr: 1,2,3 ... n, from bottom
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
    def __init__(self, stiffener_nomenclature, chosen_profile_label):
        self.stiffener_nomenclature = stiffener_nomenclature
        self.chosen_profile_label = chosen_profile_label
        
    
    

    # Input: 
        # Structure.Stiffener.Nomenclature
        # Choosen profile label
    
    # Methods: 
        # user chooses a set of profiles from:
            # Extrusions
            # Machined
    

""" Available extruded profiles """
class Extrusions(ProfileLibrary):
    def __init__(self, profile_label, SM, A_w, t_w, type_):
        self.profile_label = profile_label
        self.SM = SM
        self.A_w = A_w
        self.t_w = t_w
        self.type_ = type_
#        self.f_w = f_w
#        self.f_t = f_t
#        self.h_w = h_w
#        self.A_t = A_t

        
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
    def __init__(self, design_category, ship_object):
        self.design_category = GlobalVariableCheck.check_inputs('init', design_category, ship_object)
        
    def calc_global_var(self, ship_object):
        GlobalVariableCheck.check_inputs('calc_global_var', self.design_category, ship_object)
        
        """ Design catergory factor k_DC, section 7.2 """
        if self.design_category == 'A':
            self.k_DC = 1
        elif self.design_category == 'B':
            self.k_DC = 0.8
        elif self.design_category == 'C':
            self.k_DC = 0.6
        elif self.design_category == 'D':
            self.k_DC = 0.4
        #print ("k_DC = ", k_DC)
        
        """ DYNAMIC LOAD FACTOR n_CG, SECTION 7.3 """
        n_CG1 = (0.32 * (ship_object.L_WL / (10*ship_object.B_C) + 0.084) # eq.1.
        * (50 - ship_object.Beta_04) * ((ship_object.V**2 * ship_object.B_C**2)
        / ship_object.m_LDC)) # eq.1 cont.
        #print ("n_CG1 = ", n_CG1)
        n_CG2 = (0.5 * ship_object.V) / ship_object.m_LDC**0.17 # eq.2.
        #print ("n_CG2 = ", n_CG2)
        
        """ Dynamimc load factor for planing motor craft in planing mode,
            section 7.3.2 
        """   
        if ship_object.craft_mode == 1:
            
            if n_CG1 <= 3.0:
                self.n_CG = n_CG1
            elif (3.0 > (n_CG1 and n_CG2) < 7):
                self.n_CG = max(n_CG1, n_CG2)
            else:
                self.n_CG = 7    
            #print ("n_CG = ", n_CG)
            
            """ Dynamic load factor for displacement motor craft, section 7.3.2 """
        elif ship_object.craft_mode == 2:
            
            if n_CG1 <= 3:
                self.n_CG = n_CG1
            else:
                print("Your vessel might be going too fast for a displacement craft!")
  
    
    """ PRESSURE ADJUSTING FACTORS, SECTION 7 """
    def calc_pressure_factors(self, ship_object, structure_object, component_object):

        """ LONGITUDINAL PRESSURE DISTRIBUTION FACTOR k_L, SECTION 7.4
            First the dynimic load factor has to be modified according to 
            section 7.4 
        """
        if self.n_CG < 3:
            n_CG_kL = 3
        elif self.n_CG > 6:
            n_CG_kL = 6
        else:
            n_CG_kL = n_CG
        #print ("n_CG_kL = ", n_CG_kL)
        
        """ Now k_L can be calculated, section 7.4 eq 3. """    
        if (component_object.x/ship_object.L_WL) > 0.6:
            k_L = 1
        elif (component_object.x/ship_object.L_WL) <= 0.6:
            k_L = ((1 - 0.167 * n_CG_kL) / 0.6 *
            (component_object.x/ship_object.L_WL) + 0.167 * n_CG_kL)
            if k_L > 1:
                k_L = 1
            else:
                pass 
        else:
            pass
        
        #print ("x/L_WL = ", (x/L_WL))
        #print ("k_L = ", k_L)
        
        
        """ AREA PRESSURE REDUCTION FACTOR k_AR, SECTION 7.5 """
        """ k_R is the structural component and boat type factor """
        
        if isinstance(component_object, Panel):
            #if craft_mode == 1:
            k_R_p = 1
            #elif craft_mode == 2:
            k_R_d = 1.5 - 3e-4 * component_object.b
            #print ("k_R_panel = ", k_R_panel)
            
            """ A_D is the design area in m2 """
            A_D = (component_object.l * component_object.b)*1e-6
            #print ("A_D_panel = ", A_D)
            
            """ check maximum and minimum value and modify according to 
                section 7.5.1
            """
            if A_D > 2.5e-6 * component_object.b**2:
                A_D = 2.5e-6 * component_object.b**2
            else:
                A_D = A_D
            #print ("A_D_panel = ", A_D) 
            
            """ Calculate k_AR """
            #if craft_mode == 1:
            k_AR_p = ((k_R_p * 0.1 * ship_object.m_LDC**0.15) / 
            A_D**0.3)
            #elif craft_mode == 2:
            k_AR_d = ((k_R_d * 0.1 * ship_object.m_LDC**0.15) / 
            A_D**0.3)
            
            """ check maximum and minimum value and modify according to 
                section 7.5.2-3
            """
            if k_AR_p > 1: 
                k_AR_p = 1
            elif k_AR_p < 0.25:
                k_AR_p = 0.25
            else:
                k_AR_p = k_AR_p
            
            if k_AR_d > 1: 
                k_AR_d = 1
            elif k_AR_d < 0.25:
                k_AR_d = 0.25
            else:
                k_AR_d = k_AR_d

            #print ("k_AR_panel = ", k_AR_panel)
            
        elif isinstance(component_object, Stiffener): 
            #if craft_mode == 1:
            k_R_p = 1       
            #elif craft_mode == 2:
            k_R_d = 1 - 2e-4 * component_object.l_u
            #print ("k_R_stiffener = ", k_R_stiff)
            
            """ A_D is the design area in m2 """
            A_D = (component_object.l_u * component_object.s)*1e-6
            #print ("A_D_stiffener = ", A_D)
            
            """ check maximum and minimum value and modify according to 
                section 7.5.1 
            """   
            if A_D < 0.33e-6 * component_object.l_u**2:
                A_D = 0.33e-6 * component_object.l_u**2
            else:
                A_D = A_D
                
            """ Calculate k_AR """
            #if craft_mode == 1:
            k_AR_p = ((k_R_p * 0.1 * ship_object.m_LDC**0.15) / 
            A_D**0.3)
            #elif craft_mode == 2:
            k_AR_d = ((k_R_d * 0.1 * ship_object.m_LDC**0.15) / 
            A_D**0.3)
               
            """ check maximum and minimum value and modify according to 
                section 7.5.2-3
            """                
            if k_AR_p > 1:
                k_AR_p = 1
            elif k_AR_p < 0.25:
                k_AR_p = 0.25
            else:
                k_AR_p = k_AR_p
                
            if k_AR_d > 1:
                k_AR_d = 1
            elif k_AR_d < 0.25:
                k_AR_d = 0.25
            else:
                k_AR_d = k_AR_d
            #print ("k_AR_stiff = ", k_AR_stiff)
                  
            """ HULL SIDE PRESSURE REDUCTION FACTOR k_Z, SECTION 7.6. """
            # Z is the height from the fully loaded waterline to the top of the deck
            # h is the height from the fully loaded waterline to the middle/centre 
            # of the plate/stiffener.
            #k_Z = (Z - h) / Z
            k_Z = 0.676
            
            #k_P = (k_DC, n_CG, k_L, k_AR_panel, k_AR_stiff, k_Z)
            #print (k_P)
#        return (component_object.k_DC = k_DC, component_object.n_CG = n_CG, 
#                component_object.k_L = k_L, component_object.k_AR_p = k_AR_p, 
#                component_object.k_AR_d = k_AR_d, component_object.k_Z = k_Z
#                )
    #    
#    
#    ##pressure_factors(ship_prop, craft_mode, design_loc, panel_dim, stiff_dim)
    
    # Input: 
        # Panel:
            # Vessel
            # MaterialsLibrary
            # Structure
            # Structure.Shell
            # Structure.Shell.Panel
        # Stiffener (minimum req):
            # Vessel
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
        # Vessel
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
        # Create graph of nomenclature using the vessel dimensions and SA.(this
        # ...is for helping the user to assign nomenclature to each member but 
        # ...also to get a good overview of the initial SA.)
        
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
    
    def define_vessel(L_WL, B_C, m_LDC, Beta_04, H_T, T_C, V, op_class):
        VESSEL = Vessel(L_WL, B_C, m_LDC, Beta_04, H_T, T_C, V, op_class)
        return VESSEL
    
#    def assign_material(self, material_obj):
#        self.material_obj = material_obj
#    
#    def assign_profile(self, profile_obj):
#        self.profile_obj = profile_obj
#        
#    def create_topology(vessel, n_stiff):
#        stiff_y_pos = linspace(0, width, s_stiff)
#        panel_width = s_stiffener
#        panel_y_pos = stiff_y_pos - s_stiff/2
#        
#    def define_topology(stiff_y_pos, panel_y_pos, panel_width):
#        for i in range(0, stiff_y_pos.__len__()):
#            self.stiff_obj[i] = self.Stiffener(stiff_y_pos[0], static_length, static_x)
#            self.Stiffener.__init__(STRUCTURE, y_pos, x_pos, length)
#            VESSEL.STRUCTURE.define_topology(stiff_y_pos, panel_y_pos, panel_width)

"""
Design.CalScantling(Rule,Vessel)
[List1]=Structure.Panels[i].GetData(RuleType)
[List1]=Vessel.Structure.Panels[0].GetData(RuleType)
[List1]=Vessel.Structure.Stiffener[0].GetData(RuleType)
list1=[b,l,m_LDC]

[List2] = Rule.CalcPressureFactors(List1)
List2=[ISO,k_AR_d,k_AR_p,A_D]

Vessel.Structure.Panels[i].AssignScant(List2)
if list2[0]==ISO:
    Dict=['ISO':List2]
    


Design.AssignMaterial(Vessel,Material)
def assign_material(self,obj_material)
    self. obj_material=obj_material
Vessel.Structure.Stiffener[0].AssignMaterial(obj_material)
Vessel.Structuture.Stiffener[0].obj_material

n_stiff = Vessel.Structure.Stiffeners.__len__()
Structure.Stiffeners=[list of stiffeners objects]

Design.CreateTopology(VESSEL,nstiff)
 stiff_y_pos=linspace(0,width,s_stiffener)
 panel_width=s_stiffener
 Panel_y=stiff_y_pos-s_stiff/2

VESSEL.STRUCTURE.DefineTopology(stiff_y_pos, panel_y_pos, panel_width)
for i in range(0,stiff_y_pos.__len__()):
    self.Stiff_obj[i] = self.Stiffener(stiff_y_pos[0], static_length, static_x)
    self.Stiffener.__init__(STRUCTURE, y_pos, x_pos, length)

Stiffener.__init__(STRUCTURE,y_pos, x_pos, length)
    self.y_pos=y_pos
    self.x_pos=x_pos
    self.length=length
    
"""

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
     A: You define material objects for whatever kind of materials you are 
        going to use. Afterwards, when you define a structural member these 
        objects should be atributes of the structural member object.
     
    3.	Define Profiles
     Q:  What part of the profiles do you define?
     A:  At least the profile cross section, should calculate SM w/o attached plating
     
    4.	Define topology (stiffeners, girders and bulkheads position, 
    orientation using ASV nomenclature) and Areas (Side, Bottom, Superstructure, etc..)
     Q:  In what order do you define the topology?
     A: Don't know... Shell thickness, Frame spacing, Bulkheads 
        (in frame locations), Longitudinal girders, longitudinal reinforcements.
     
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
    
    def check_inputs(function, design_category, ship_object, 
                     structure_object=None, component_object=None):
        if function == 'init':
            while True:
                    if design_category in ('A', 'B', 'C', 'D'):
                        break
                    else:
                        design_category = input('Not a valid design category, choose A, B, C or D >>> ')
                        return design_category
        elif function == 'calc_global_var':
            if not hasattr(ship_object, 'craft_mode'):
                print("Error: calculate or choose craft mode; planing or displacement")
                while True:
                    craft_mode_ = input('1 = planing, 2 = disp, 3 = calculate >>> ')
                    if craft_mode_ in ('1', '2', '3'):
                        break
                    else:
                        print('Not a valid number')
                if craft_mode_ == '3':
                    ship_object.craft_mode = ship_object.calc_craft_mode()
                    #setattr(ship_object, 'craft_mode', ship_object.calc_craft_mode())
                else:
                    ship_object.craft_mode = int(craft_mode_)
                    #setattr(ship_object, 'craft_mode', int(craft_mode_))
            print("craft_mode = ", ship_object.craft_mode)
    
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


#ship_A = Vessel(6.851, 2.008, 4500, 30.0, 3.0, 0.875, 12.0, 'A')
##ship_A.craft_mode = ship_A.calc_craft_mode()
#
#AL_5083_O = MaterialsLibrary('AL_5083_O', 125, 270, 7000, 2692, 2720)
#AL_6082_T6 = MaterialsLibrary('AL_6082_T6', 115, 170, 7000, 2692, 2830)
#print(AL_5083_O)
#
#Flat_Bar_62_x_6 = Extrusions('Flat Bar 62 x 6', 8.824, 3.720, 6.0, 'Flat Bar')
#
#section1 = Structure(643, 1120, 1)
#section1.stiff_s = section1.stiffener_equal_spacing()
#print("s_stiffener = ", section1.stiff_s)
#
#stiffener1 = Stiffener(0.325, 0, section1, 'longitudinal', 'bottom', 'A')
#stiffener1.nomenclature = stiffener1.assign_nomenclature()
#stiffener1.choose_material(stiffener1, AL_6082_T6)
#stiffener1.choose_profile(stiffener1, Flat_Bar_62_x_6)
#print("stiffener name = ", stiffener1.nomenclature)
#print("stiffener material = ", stiffener1.material)
#print("stiffener profile = ", stiffener1.profile_label)
#
#global_ISO_var = ISO12215('a', ship_A)
#global_ISO_var.calc_global_var(ship_A)
#print("design_category = ", global_ISO_var.design_category)
#print("k_DC = ", global_ISO_var.k_DC)
#
#stiffener1.pressure_factors = global_ISO_var.calc_pressure_factors(ship_A, section1, stiffener1)
##print(stiffener1.pressurefactors.k_L)

Designer.define_vessel(6.851, 2.008, 4500, 30.0, 3.0, 0.875, 12.0, 'A')
print(VESSEL)
