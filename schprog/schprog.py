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
    def __init__(self, L_WL, B_C, m_LDC, Beta_04, H_T, T_C, V):
        self.L_WL = L_WL
        self.B_C = B_C
        self.m_LDC = m_LDC
        self.Beta_04 = Beta_04 # range 10 - 30 degrees
        self.H_T = H_T
        self.T_C = T_C
        self.V = V
        # TODO: add variable check

    
#   Calculate craft mode (planing = 1 or displacement = 2)
    def calc_craft_mode(self):
        if self.V / math.sqrt(self.L_WL) < 5:
            craft_mode = 2
        else:
            craft_mode = 1
        return craft_mode
    
    def assign_structure(self,obj_Struct):
        self.Struct = obj_Struct
        pass

        
""" Defines and configures the structural model from user input, including topology.
    Calculates the weight of the vessel and the CoG.
"""
class Structure:
    def __init__(self):
        self.m_LDC = 4500 # TODO: Figure out how to get value from superclass object
        self.Panel=[]
        pass

    def assign_panel(self, obj_Panel):
        self.Panel = self.Panel + [obj_Panel] #TODO: Debug
    
    def assign_global_var(self, InputVec):
        self.RuleType = InputVec[0]
        if self.RuleType == 'ISO':
            self.k_DC = InputVec[1]
            self.n_CG = InputVec[2]


        
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
        pass

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
    
    def assign_material(self, material_obj):
        self.material = material_obj
        
    
    def assign_profile(self, profile_obj):
        self.profile = profile_obj
        
        
        

        

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
    def __init__(self, b, l):
        self.b = b
        self.l = l
        self.x_pos = 0.325 # TODO: change to method when creating topology
        self.location = 'bottom'
        pass

    def assign_press_factors(self, InputVec):
        self.RuleType = InputVec[0]
        if self.RuleType == 'ISO':
            #Assign ISO Values
            self.k_L = InputVec[1]
            self.k_AR_d = InputVec[2]
            self.k_AR_p = InputVec[3]
            self.A_D = InputVec[4]
            self.k_Z = InputVec[5]
        pass

    def assign_design_pressure(self, InputVec):
        self.RuleType = InputVec[0]
        if self.RuleType == 'ISO':
            #Assign ISO Values
            self.P_M = InputVec[1]

        pass
    
    def assign_material(self, material_obj):
        self.material = material_obj
        
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
    def __init__(self):
        pass
    # Input: 
        # Chosen rules
        # Variables common to all rules (tricky to know for this version)
    

""" Calculates structural requirements according to ISO 12215 """
class ISO12215(Rules):
    def __init__(self, design_category): # TODO: change inputs
        self.name = 'ISO'
        self.design_category = GlobalVariableCheck.check_inputs('init', design_category)
        
    def get_vessel_data(self, obj_Vess):
        L_WL = obj_Vess.L_WL
        B_C = obj_Vess.B_C
        m_LDC = obj_Vess.m_LDC
        Beta_04 = obj_Vess.Beta_04
        V = obj_Vess.V
        craft_mode = obj_Vess.calc_craft_mode()
        return [L_WL, B_C, m_LDC, Beta_04, V, craft_mode]
        

    def calc_global_var(self, InputVec): # TODO: change inputs
        #GlobalVariableCheck.check_inputs('calc_global_var', self.design_category, ship_object)
        
        [L_WL, B_C, m_LDC, Beta_04, V, craft_mode] = InputVec # TODO: add required inputs
        
        """ Design catergory factor k_DC, section 7.2 """
        if self.design_category == 'A':
            k_DC = 1
        elif self.design_category == 'B':
            k_DC = 0.8
        elif self.design_category == 'C':
            k_DC = 0.6
        elif self.design_category == 'D':
            k_DC = 0.4

        
        """ DYNAMIC LOAD FACTOR n_CG, SECTION 7.3 """
        n_CG1 = (0.32 * (L_WL / (10*B_C) + 0.084)
        * (50 - Beta_04) * ((V**2 * B_C**2) / m_LDC))

        n_CG2 = (0.5 * V) / m_LDC**0.17

        
        """ Dynamimc load factor for planing motor craft in planing mode,
            section 7.3.2 
        """   
        if craft_mode == 1:
            
            if n_CG1 <= 3.0:
                n_CG = n_CG1
            elif (3.0 > (n_CG1 and n_CG2) < 7):
                n_CG = max(n_CG1, n_CG2)
            else:
                n_CG = 7    

            
            """ Dynamic load factor for displacement motor craft, section 7.3.2 """
        elif craft_mode == 2:
            
            if n_CG1 <= 3:
                n_CG = n_CG1
            else:
                print("Your vessel might be going too fast for a displacement craft!")
                
        List2 = ['ISO', k_DC, n_CG]
        return List2

                
    def measure_panel(self,obj_panel):
        b = obj_panel.b
        l = obj_panel.l
        x_pos = obj_panel.x_pos
        location = obj_panel.location
        return [b, l, x_pos, location]
    
    """ PRESSURE ADJUSTING FACTORS, SECTION 7 """
    def calc_panel_pressure_factors(self, InputVec):
        
        [b, l , x_pos, location, m_LDC, n_CG, L_WL] = InputVec # TODO: add required inputs. Input might get 'location' as well
        
        """ LONGITUDINAL PRESSURE DISTRIBUTION FACTOR k_L, SECTION 7.4
            First the dynimic load factor has to be modified according to 
            section 7.4 
        """
        if n_CG < 3:
            n_CG_kL = 3
        elif n_CG > 6:
            n_CG_kL = 6
        else:
            n_CG_kL = n_CG

        """ Calculate k_L, section 7.4 eq 3. """    
        if (x_pos/L_WL) > 0.6:
            k_L = 1
        elif (x_pos/L_WL) <= 0.6:
            k_L = ((1 - 0.167 * n_CG_kL) / 0.6 *
            (x_pos/L_WL) + 0.167 * n_CG_kL)
            if k_L > 1:
                k_L = 1
            else:
                pass 
        else:
            pass
        
        
        """ AREA PRESSURE REDUCTION FACTOR k_AR, SECTION 7.5 """
        """ k_R is the structural component and boat type factor """
        k_R_p = 1 
        k_R_d = 1.5 - 3e-4 * b
            
        """ A_D is the design area in m2 """
        A_D = (l * b) * 1e-6
        
        """ check maximum and minimum value and modify according to 
            section 7.5.1
        """
        if A_D > 2.5e-6 * b ** 2:
            A_D = 2.5e-6 * b ** 2
        else:
            A_D = A_D

            """ Calculate k_AR """
        k_AR_p = ((k_R_p * 0.1 * m_LDC ** 0.15) /
                  A_D ** 0.3)
        k_AR_d = ((k_R_d * 0.1 * m_LDC ** 0.15) /
                  A_D ** 0.3)

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

        """ HULL SIDE PRESSURE REDUCTION FACTOR k_Z, SECTION 7.6. """
        # Z is the height from the fully loaded waterline to the top of the deck
        # h is the height from the fully loaded waterline to the middle/centre 
        # of the plate/stiffener.
        #k_Z = (Z - h) / Z
        k_Z = 0.676 # TODO: calculate k_Z dynamically
        
        List4 = ['ISO', k_L, k_AR_d, k_AR_p, A_D, k_Z]

        return List4

            
#        elif isinstance(component_object, Stiffener): 
#            k_R_p = 1
#            k_R_d = 1 - 2e-4 * component_object.l_u
#            
#            """ A_D is the design area in m2 """
#            A_D = (component_object.l_u * component_object.s)*1e-6
#            
#            """ check maximum and minimum value and modify according to 
#                section 7.5.1 
#            """   
#            if A_D < 0.33e-6 * component_object.l_u**2:
#                A_D = 0.33e-6 * component_object.l_u**2
#            else:
#                A_D = A_D
#                
#            """ Calculate k_AR """
#            k_AR_p = ((k_R_p * 0.1 * ship_object.m_LDC**0.15) / 
#            A_D**0.3)
#            k_AR_d = ((k_R_d * 0.1 * ship_object.m_LDC**0.15) / 
#            A_D**0.3)
#               
#            """ check maximum and minimum value and modify according to 
#                section 7.5.2-3
#            """                
#            if k_AR_p > 1:
#                k_AR_p = 1
#            elif k_AR_p < 0.25:
#                k_AR_p = 0.25
#            else:
#                k_AR_p = k_AR_p
#                
#            if k_AR_d > 1:
#                k_AR_d = 1
#            elif k_AR_d < 0.25:
#                k_AR_d = 0.25
#            else:
#                k_AR_d = k_AR_d
#                  
#            """ HULL SIDE PRESSURE REDUCTION FACTOR k_Z, SECTION 7.6. """
#            # Z is the height from the fully loaded waterline to the top of the deck
#            # h is the height from the fully loaded waterline to the middle/centre 
#            # of the plate/stiffener.
#            #k_Z = (Z - h) / Z
#            k_Z = 0.676
            
            #k_P = (k_DC, n_CG, k_L, k_AR_panel, k_AR_stiff, k_Z)
#        return (component_object.k_DC = k_DC, component_object.n_CG = n_CG, 
#                component_object.k_L = k_L, component_object.k_AR_p = k_AR_p, 
#                component_object.k_AR_d = k_AR_d, component_object.k_Z = k_Z
#                )

    def get_pressure_factors(self, obj_Struct, obj_Comp):
        k_DC = obj_Struct.k_DC
        k_L = obj_Comp.k_L
        k_AR_d = obj_Comp.k_AR_d
        k_AR_p = obj_Comp.k_AR_p
        k_Z = obj_Comp.k_Z
        return [k_DC, k_L, k_AR_d, k_AR_p, k_Z]
        

    """" DESIGN PRESSURES, SECTION 8. """
    """ MOTOR CRAFT DESIGN PRESSURE, SECTION 8.1 """
    def calc_panel_pressures(self, InputVec):
        
        [k_DC, k_L, k_AR_d, k_AR_p, k_Z, location, n_CG, L_WL, B_C, m_LDC] = InputVec
        
        P_BMDBASE = 2.4*m_LDC**0.33 + 20  # kN/m2
        P_BMPBASE = (0.1*m_LDC/(L_WL * B_C)) * (1 + k_DC**0.5 * n_CG)  # kN/m2
        
        if location == 'bottom':
            """ BOTTOM DESIGN PRESSURE
                The bottom pressure shall be the greater or 8.1.2 or 8.1.3. 
            """

            P_MMIN = 0.45*m_LDC**0.33 + (0.9*L_WL * k_DC)  # kN/m2

            """         Displacement mode, section 8.1.2. """
            P_MD = P_BMDBASE * k_AR_d * k_DC * k_L  # kN/m2
            
            """         Planing mode, section 8.1.3. """
            P_MP = P_BMPBASE * k_AR_p * k_L  # kN/m2
            
            """         Maximum pressure """
            P_M = max(P_MD, P_MP, P_MMIN)  # kN/m2
        
        elif location == 'side':
            """ SIDE DESIGN PRESSURE
                The side pressure shall be the greater or 8.1.4 or 8.1.5. 
            """
            P_MMIN = 0.9*L_WL * k_DC  # kN/m2
            P_DMBASE = 0.35*L_WL + 14.6  # kN/m2
            
            """         Displacement mode, section 8.1.4. """
            P_MD = (P_DMBASE + k_Z * (P_BMDBASE - P_DMBASE)) * k_AR_d * k_DC * k_L
            
            """         Planing mode, section 8.1.5. """
            P_MP = (P_DMBASE + k_Z * (0.25*P_BMPBASE - P_DMBASE)) * k_AR_p * k_DC * k_L
            
            """         Maximum pressure """
            P_M = max(P_MD, P_MP, P_MMIN)  # kN/m2
        
#        elif location == 'bulkhead': 
#            """ (ignore for now) WATERTIGHT BULKHEADS DESIGN PRESSURE, SECTION 8.3.1 """
#            
#            h = l  # m, This might be wrong.
#            h_b = (2/3) * h_panel  # m
#            P_M = 7 * h_b_panel   # kN/m2
        
        List4 = ['ISO', P_M] 

        return List4
        
#            """" DESIGN PRESSURES, SECTION 8. """
#    """ MOTOR CRAFT DESIGN PRESSURE, SECTION 8.1 """
#    def calc_panel_pressures(ship_prop, design_loc, panel_dim, stiff_dim, k_P):
#        
#        [L_WL, B_C, m_LDC] = ShipData
#        [k_DC, k_L, k_AR_d, k_AR_p, k_Z] = PressureFactors
#        [location] = StiffData
#        """ BOTTOM DESIGN PRESSURE
#            The bottom pressure shall be the greater or 8.1.2 or 8.1.3. 
#        """
#        P_BMDBASE = 2.4*m_LDC**0.33 + 20  # kN/m2
#        P_BMPBASE = (0.1*m_LDC/(L_WL * B_C)) * (1 + k_DC**0.5 * n_CG)  # kN/m2
#        P_BMMIN = 0.45*m_LDC**0.33 + (0.9*L_WL * k_DC)  # kN/m2
#        
#        """ ---- Stiffener ----- """
#        """         Displacement mode, section 8.1.2. """
#        P_BMD_stiff = P_BMDBASE * k_AR_stiff_d * k_DC * k_L  # kN/m2
#        
#        
#        """         Planing mode, section 8.1.3. """
#        P_BMP_stiff = P_BMPBASE * k_AR_stiff_p * k_L  # kN/m2
#        
#        """         Maximum pressure """
#        P_BP_stiff = max(P_BMD_stiff, P_BMP_stiff, P_BMMIN)  # kN/m2
#        
#        
#        """ SIDE DESIGN PRESSURE
#            The side pressure shall be the greater or 8.1.4 or 8.1.5. 
#        """
#        P_SMMIN = 0.9*L_WL * k_DC  # kN/m2
#        P_DMBASE = 0.35*L_WL + 14.6  # kN/m2
#        print ("P_DMBASE = ", P_DMBASE)
#        
#        """ ----- Stiffner ----- """
#        """         Displacement mode, section 8.1.4. """
#        P_SMD_stiff = (P_DMBASE + k_Z * (P_BMDBASE - P_DMBASE)) * k_AR_stiff_d * k_DC * k_L
#        
#        """         Planing mode, section 8.1.5. """
#        P_SMP_stiff = (P_DMBASE + k_Z * (0.25*P_BMPBASE - P_DMBASE)) * k_AR_stiff_p * k_DC * k_L
#        
#        """         Maximum pressure """
#        P_SM_stiff = max(P_SMD_stiff, P_SMP_stiff, P_SMMIN) # kN/m2

#        
#        """ (ignore for now) WATERTIGHT BULKHEADS DESIGN PRESSURE, SECTION 8.3.1 """

#        """ ----- Vertical stiffener ----- """
#        h_stiff_vert = l_u  # m, This might be wrong.
#        h_b_stiff_vert = (2/3) * h_stiff_vert  # m
#        P_WB_stiff_vert = 7 * h_b_stiff_vert   # kN/m2
#        
#        
#        """ ----- Horizontal stiffener ----- """
#        h_b_stiff_hori = z  # m, This will have to be changed later. 
#        P_WB_stiff_hori = 7 * h_b_stiff_hori   # kN/m2
#        
#        return (P_BP_stiff, P_BP_panel, P_SM_stiff, P_SM_panel, 
#                P_WB_panel,P_WB_stiff_vert, P_WB_stiff_hori)


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
#     Create graphs, messages, spreadsheets and all calculation outputs.
#     Input:
#         Vessel
#         MaterialsLibrary
#         Structure
#         Structure.Shell
#         Structure.Shell.Panel
#         PlatingLibrary
#         Structure.Stiffener
#         ProfileLibrary
#         ISO12215
#        
#     Methods:
#         List outputs with units
#         Create spreadsheets containing each structural member and the SA.
#         Add any important messages (different modes e.g. user mode, developer mode?)
#         Create graphs from e.g. the optimization or to help with other things.
#         Create graph of nomenclature using the vessel dimensions and SA.(this
#         ...is for helping the user to assign nomenclature to each member but 
#         ...also to get a good overview of the initial SA.)
#        
#     Output:
#         Calculation outputs
#         Spreadsheets
#         Messages
#         Graphs

""" User interface, receive user inputs and initialize the relevant objects 
    using the user input. 
"""
class Designer:
    def __init__(self):
        pass

    def calc_pressure_factors(self, obj_Rule, obj_Struct, obj_Vess):

        VessData = obj_Rule.get_vessel_data(obj_Vess)
        
        GlobVar = obj_Rule.calc_global_var(VessData)
        
        obj_Struct.assign_global_var(GlobVar)
        
        for i in range(0,obj_Struct.Panel.__len__()):

            PanData = obj_Rule.measure_panel(obj_Struct.Panel[i])

            InData = PanData + [obj_Struct.m_LDC] +[obj_Struct.n_CG] +[VessData[0]]  #TODO: Debug

            PressFac = obj_Rule.calc_panel_pressure_factors(InData)

            obj_Struct.Panel[i].assign_press_factors(PressFac)
            print("Testing1")

        #for i in range(0,obj_Struct.Stiff.__len__())
        
    def calc_design_pressures(self, obj_Rule, obj_Struct, obj_Vess):
        
        VessData = obj_Rule.get_vessel_data(obj_Vess)
        
        for i in range(0, obj_Struct.Panel.__len__()):
            
            PressFact = obj_Rule.get_pressure_factors(obj_Struct, obj_Struct.Panel[i])
            
            PanData = obj_Rule.measure_panel(obj_Struct.Panel[i])
            
            InData = PressFact + [PanData[3]] + [obj_Struct.n_CG] + VessData[:3]
            
            DesPress = obj_Rule.calc_panel_pressures(InData)
            
            obj_Struct.Panel[i].assign_design_pressure(DesPress)
            print("Testing2")
            
            

        
    def assign_profile(self, profile_obj):
        self.profile_obj = profile_obj

#    def initialize_rule(self,type):
#        import schprog as SP
#        self.Rule = SP.ISO12215(0,0)
#        print('test')
#        pass

#    def create_topology(vessel, n_stiff):
#        stiff_y_pos = linspace(0, width, s_stiff)
#        panel_width = s_stiffener
#        panel_y_pos = stiff_y_pos - s_stiff/2
#
#    
#    def define_topology(stiff_y_pos, panel_y_pos, panel_width):
#        VESSEL.STRUCTURE.define_topology(stiff_y_pos, panel_y_pos, panel_width)
    #        for i in range(0, stiff_y_pos.__len__()):
    #            self.stiff_obj[i] = self.Stiffener(stiff_y_pos[i], static_length, static_x)
    #            self.Stiffener.__init__(STRUCTURE, y_pos, x_pos, length)
#            

#    

#        
#    def calc_scantling(Rule,Vessel):
#        [list1]=Vessel.Structure.Panels[i].GetData(RuleType)
#        [list1]=Vessel.Structure.Stiffener[i].GetData(RuleType)
#        list1=[b,l,m_LDC]




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

        
""" Check input variables for typos, negatives and other errors, and promts the
    user to correct the value.   
"""
class GlobalVariableCheck:
    
    def check_inputs(function, design_category, ship_object=None, 
                     structure_object=None, component_object=None):
        if function == 'init':
            while True:
                    if design_category in ('A', 'B', 'C', 'D'):
                        return design_category
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


""" User chooses between different optimization methods depending on what type
    of structural member needs to be optimized.
"""
class Optimizer:
    pass
    # User chooses optimization method
    # User configures chosen method
    # Run optimization



