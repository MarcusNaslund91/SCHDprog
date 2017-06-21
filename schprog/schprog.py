#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
...

"""

#import sys
import logging
import math
#import numpy
from bisect import bisect_left

#from schprog import __version__

__author__ = "Marcus Naslund"
__copyright__ = "Marcus Naslund"
__license__ = "none"

_logger = logging.getLogger(__name__)


class Vessel:
    """ Defines vessel data and operational conditions.
        Gets structure object assigned to it.
    """

    def __init__(self, L_WL, B_C, m_LDC, Beta_04, H_T, T_C, V):
        self.L_WL = L_WL
        self.B_C = B_C
        self.m_LDC = m_LDC
        self.Beta_04 = Beta_04  # range 10 - 30 degrees
        self.H_T = H_T
        self.T_C = T_C
        self.V = V
        # TODO: add variable check

    def calc_craft_mode(self):
        #   Calculate craft mode (planing = 1 or displacement = 2)
        if self.V / math.sqrt(self.L_WL) < 5:
            craft_mode = 2
        else:
            craft_mode = 1
        return craft_mode

    def assign_structure(self, obj_Struct):
        self.Struct = obj_Struct
        pass


class Structure:
    """ Defines and configures the structural model from user input,
        including topology. Calculates the weight of the vessel and the CoG.
    """
    def __init__(self):
        self.m_LDC = 4500  # TODO: Figure out how to get value from superclass object
        self.Panel = []
        pass

    def assign_panel(self, obj_Panel):
        self.Panel = self.Panel + [obj_Panel]
        pass

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


class Stiffener(Structure):
    """ Defines what type of stiffener that will be analysed and gives it a
        nomenclature as a identifier.
        Q: Calculates the actual stress?
    """
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
        else:  # TODO: add further nomenclature
            pass
        return nomenclature

    def assign_material(self, material_obj):
        self.material = material_obj
        pass

    def assign_profile(self, profile_obj):
        self.profile = profile_obj
        pass


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


class Shell(Structure):
    """ Defines the hull, deck and superstructure shell properties.
        Contains a plating object, width distribution over a normalized length,
        location according to the evaluating rules.
    """
    pass
    # Input:
        # Variables for 'Width distribution over normalized length'
        # Panel location (bottom, bottom & side, side, deck, superstructure)
    
    # Methods:
        # Calculate width distribution over normalized length
    
    # Output:
        # Width distribution over normalized length


class Panel(Shell):
    """ Defines the panel dimensions according to the choosen rules and gives
        it a nomenclature as a identifier. Sends the information to the rules
        calculator.
    """
    def __init__(self, b, l, x_pos, y_pos, location):
        self.b = b
        self.l = l
        self.x_pos = x_pos  # TODO: change to method when creating topology
        self.y_pos = y_pos
        self.location = location
        pass

    def assign_press_factors(self, InputVec):
        self.RuleType = InputVec[0]
        if self.RuleType == 'ISO':
            # Assign ISO Values
            self.k_L = InputVec[1]
            self.k_AR_d = InputVec[2]
            self.k_AR_p = InputVec[3]
            self.A_D = InputVec[4]
            self.k_Z = InputVec[5]
        pass

    def assign_design_pressure(self, InputVec):
        self.RuleType = InputVec[0]
        if self.RuleType == 'ISO':
            # Assign ISO Values
            self.P_M = InputVec[1]
        pass

    def assign_material(self, obj_Material):
        self.material = obj_Material
        pass

    def assign_scantling_req(self, InputVec):
        self.RuleType = InputVec[0]
        if self.RuleType == 'ISO':
            # Assign ISO Values
            self.k_2 = InputVec[1]
            self.k_3 = InputVec[2]
            self.F_d = InputVec[3]
            self.M_d = InputVec[4]
            self.t_req = InputVec[5]
            self.t_MIN = InputVec[6]
        pass

    def assign_plate(self, obj_Plate):
        self.plate = obj_Plate
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


class MaterialsLibrary:
    """ Available materials and their respective properties """
    def __init__(self, material_label,
                 yield_strength,
                 tensile_strength,
                 elastic_modulus,
                 shear_modulus,
                 density
                 ):
        self.material_label = material_label
        self.yield_strength = yield_strength
        self.tensile_strength = tensile_strength
        self.elastic_modulus = elastic_modulus
        self.shear_modulus = shear_modulus
        self.density = density
        pass

    def __repr__(self):
        return """
        material_label = %s
        yield_strength = %d
        tensile_strength = %d
        elastic_modulus = %d
        shear_modulus = %d
        density = %d
        """ % (self.material_label,
               self.yield_strength,
               self.tensile_strength,
               self.elastic_modulus,
               self.shear_modulus,
               self.density
               )
        pass


class PlatingLibrary:
    """ Contains all the availible plates from manufacturers. The user can
        choose from between different thicknesses. The panel is then sent to
        the complience calculator.
    """
    def __init__(self):
        self.Plates = []
        pass

    def assign_plate(self, obj_Plate):
        self.Plates = self.Plates + [obj_Plate]
        pass

    def list_all_thicknesses(self):
        all_tp = []
        del all_tp[:]
        for i in range(0, self.Plates.__len__()):
            all_tp = all_tp + [self.Plates[i].t_p]
        return all_tp


class Plates(PlatingLibrary):
    """
        .....................
    """
    def __init__(self, plating_label, t_p):
        self.plating_label = plating_label
        self.t_p = t_p
        pass

    def __repr__(self):
        return """
        plating_label = %s
        t_p = %d
        """ % (self.plating_label,
               self.t_p)
        pass


class ProfileLibrary:
    """ Library containing structural profiles for e.g. stiffeners, girders
        and frames. User can choose between a set of available extrusions
        or define their own for machining.
    """
    def __init__(self, stiffener_nomenclature, chosen_profile_label):
        self.stiffener_nomenclature = stiffener_nomenclature
        self.chosen_profile_label = chosen_profile_label
        pass


class Extrusions(ProfileLibrary):
    """ Available extruded profiles """
    def __init__(self, profile_label, SM, A_w, t_w, type_):
        self.profile_label = profile_label
        self.SM = SM
        self.A_w = A_w
        self.t_w = t_w
        self.type_ = type_
        pass
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


class Machined(ProfileLibrary):
    """ User defined machined profiles """
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

        
class Rules:
    """ Stores the different structural rules for designing the structural
        properties and arrangment of the vessel, e.g. ISO12215, DNV, ABS and LR.
    """
    def __init__(self):
        pass
    # Input: 
        # Chosen rules
        # Variables common to all rules (tricky to know for this version)


class ISO12215(Rules):
    """ Calculates structural requirements according to ISO 12215 """
    def __init__(self, design_category):
        self.name = 'ISO'
        self.design_category = GlobalVariableCheck.check_inputs('init', design_category)
        pass

    def get_vessel_data(self, obj_Vess):
        L_WL = obj_Vess.L_WL
        B_C = obj_Vess.B_C
        m_LDC = obj_Vess.m_LDC
        Beta_04 = obj_Vess.Beta_04
        V = obj_Vess.V
        craft_mode = obj_Vess.calc_craft_mode()
        return [L_WL, B_C, m_LDC, Beta_04, V, craft_mode]

    def calc_global_var(self, InputVec):
        #GlobalVariableCheck.check_inputs('calc_global_var', self.design_category, ship_object)

        [L_WL, B_C, m_LDC, Beta_04, V, craft_mode] = InputVec

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
        n_CG1 = (0.32 * (L_WL / (10*B_C) + 0.084) * (50 - Beta_04) *
                 ((V**2 * B_C**2) / m_LDC)
                 )
        n_CG2 = (0.5 * V) / m_LDC**0.17

        """ Dynamimc load factor for planing motor craft in planing mode,
            section 7.3.2.
        """
        if craft_mode == 1:
            if n_CG1 <= 3.0:
                n_CG = n_CG1
            elif (3.0 > (n_CG1 and n_CG2) < 7):
                n_CG = max(n_CG1, n_CG2)
            else:
                n_CG = 7

            """ Dynamic load factor for displacement motor craft,
                section 7.3.2.
            """
        elif craft_mode == 2:
            if n_CG1 <= 3:
                n_CG = n_CG1
            else:
                print("Your vessel might be going too fast for a displacement craft!")

        GlobVar = ['ISO', k_DC, n_CG]
        return GlobVar

    def measure_panel(self, obj_panel):
        b = obj_panel.b
        l = obj_panel.l
        x_pos = obj_panel.x_pos
        y_pos = obj_panel.y_pos
        location = obj_panel.location
        return [b, l, x_pos, y_pos, location]

    """ PRESSURE ADJUSTING FACTORS, SECTION 7 """
    def calc_panel_pressure_factors(self, InputVec):

        [b, l , x_pos, y_pos, location, m_LDC, n_CG, L_WL] = InputVec

        """ LONGITUDINAL PRESSURE DISTRIBUTION FACTOR k_L, SECTION 7.4
            First the dynimic load factor has to be modified according to
            section 7.4.
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
                   (x_pos/L_WL) + 0.167 * n_CG_kL
                   )
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
            section 7.5.1.
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
            section 7.5.2-3.
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
        Z = 4.14 # meters
        h = 0.033 # meters
        k_Z = (Z - h) / Z
        #k_Z = 0.676  # TODO: calculate k_Z dynamically

        PressFact = ['ISO', k_L, k_AR_d, k_AR_p, A_D, k_Z]

        return PressFact

            
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

    def calc_panel_pressures(self, InputVec):
        """" DESIGN PRESSURES, SECTION 8. """
        """ MOTOR CRAFT DESIGN PRESSURE, SECTION 8.1 """

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
            P_MD = ((P_DMBASE + k_Z * (P_BMDBASE - P_DMBASE)) * k_AR_d *
                    k_DC * k_L
                    )

            """         Planing mode, section 8.1.5. """
            P_MP = ((P_DMBASE + k_Z * (0.25*P_BMPBASE - P_DMBASE)) * k_AR_p *
                    k_DC * k_L
                    )

            """         Maximum pressure """
            P_M = max(P_MD, P_MP, P_MMIN)  # kN/m2

#        elif location == 'bulkhead': 
#            """ (ignore for now) WATERTIGHT BULKHEADS DESIGN PRESSURE, SECTION 8.3.1 """
#            
#            h = l  # m, This might be wrong.
#            h_b = (2/3) * h  # m
#            P_M = 7 * h_b   # kN/m2

        DesPress = ['ISO', P_M]

        return DesPress

#            """" DESIGN PRESSURES, SECTION 8. """
#    """ MOTOR CRAFT DESIGN PRESSURE, SECTION 8.1 """
#    def calc_stiffener_pressures(ship_prop, design_loc, panel_dim, stiff_dim, k_P):
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

    def get_design_pressures(self, obj_Struct, obj_Comp):
        P_M = obj_Comp.P_M
        return [P_M]

    def calc_panel_req(self, InputVec):

        [P_M, b, l, location, m_LDC, V, sigma_uw, sigma_y, sigma_yw] = InputVec

        """ Panel aspect ratio factor, section 10.1.2. """

        """ ----- for strength k_2 ----- """
        if (l/b) < 2:
            k_2 = ((0.271*(l/b)**2 + 0.910*(l/b) - 0.554) /
                   ((l/b)**2 - 0.313*(l/b) + 1.351)
                   )
        else:
            k_2 = 0.5

        if k_2 > 0.5:
            k_2 = 0.5
        elif k_2 < 0.308:
            k_2 = 0.308
        else:
            k_2 = k_2

        """ ----- for stiffness k_3 (for sandwich) ----- """
        k_3 = ((0.027*(l/b)**2 - 0.029*(l/b) + 0.011) /
               ((l/b)**2 - 1.463*(l/b) + 1.108)
               )

        if k_3 > 0.028:
            k_3 = 0.028
        elif k_3 < 0.014:
            k_3 = 0.014
        else:
            k_3 = k_3

        """ Curvature correction factor k_C for curved plates,
            section 10.1.3.
        """
        k_C = 1  # this is for non-curvature, add the proper rules later!

        """ Shear force and bending moment of panel, section 10.1.5. """
        if (l/b) < 2:
            k_SHC = 0.035 + 0.394*(l/b) - 0.09*(l/b)**2
        elif (l/b) > 4:
            k_SHC = 0.5
        else:
            m = (2-4/0.463-0.500)
            k_SHC = 0.463 + m*((l/b) - 2)

        """ Design stress for metal plating, section 10.3.1. """
        sigma_d = min(0.6*sigma_uw, 0.9*sigma_yw)

        """ Variables for calculation of minimum thickness for the hull,
            section 10.6.2.
        """
        A = 1
        k_5 = math.sqrt(125/sigma_y)
        k_7_B = 0.02
        k_7_S = 0
        k_8 = 0.1

        if location == 'bottom':
            """ ---- Shear force ---- """
            F_d = (math.sqrt(k_C) * k_SHC * P_M * b)*1e-3  # N/mm , bottom

            """ ---- Bending moment ---- """
            M_d = (83.33 * k_C**2 * 2*k_2 * P_M * b**2)*1e-6  # Nmm/mm , bottom

            """ Required thikcness for metal plating, section 10.3.2. """
            t_req = b * k_C * math.sqrt((P_M*k_2) / (1000*sigma_d))  # mm

            """ Minimum thickness for the hull, section 10.6.2. """
            t_MIN = k_5 * (A + k_7_B * V + k_8 * m_LDC**0.33)  # mm

        if location == 'side':
            """ ---- Shear force ---- """
            F_d = (math.sqrt(k_C) * k_SHC * P_M * b)*1e-3  # N/mm , side

            """ ---- Bending moment ---- """
            M_d = (83.33 * k_C**2 * 2*k_2 * P_M * b**2)*1e-6  # Nmm/mm , side

            """ Required thikcness for metal plating, section 10.3.2. """
            t_req = b * k_C * math.sqrt((P_M*k_2) / (1000*sigma_d))  # mm

            """ Minimum thickness for the hull, section 10.6.2. """
            t_MIN = k_5 * (A + k_7_S * V + k_8 * m_LDC**0.33)  # mm

        if location == 'bulkhead':
            """ ---- Shear force ---- """
            F_d = (math.sqrt(k_C) * k_SHC * P_M * b)*1e-3  # N/mm , bulkehad

            """ ---- Bending moment ---- """
            M_d = (83.33 * k_C**2 * 2*k_2 * P_M * b**2)*1e-6  # Nmm/mm , bulkhead

            """ Required thikcness for metal plating, section 10.3.2. """
            t_req = b * k_C * math.sqrt((P_M*k_2) / (1000*sigma_d))  # mm

        PanReq = ['ISO', k_2, k_3, F_d, M_d, t_req, t_MIN]
        return PanReq

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


class Report:
    """ Creates and updates all the relevant information that the user is
        interested in, such as structural arrangement report, graphs of the
        optimization etc.
    """
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


class Designer:
    """ User interface, receive user inputs and initialize the relevant objects
        using the user input.
    """
    def __init__(self):
        pass

    def calc_pressure_factors(self, obj_Rule, obj_Struct, obj_Vess):

        VessData = obj_Rule.get_vessel_data(obj_Vess)

        GlobVar = obj_Rule.calc_global_var(VessData)

        obj_Struct.assign_global_var(GlobVar)

        for i in range(0, obj_Struct.Panel.__len__()):

            PanData = obj_Rule.measure_panel(obj_Struct.Panel[i])

            InData = PanData + [obj_Struct.m_LDC] + [obj_Struct.n_CG] + [VessData[0]]
            # TODO: there might be a more stable way to do this.

            PressFac = obj_Rule.calc_panel_pressure_factors(InData)

            obj_Struct.Panel[i].assign_press_factors(PressFac)
            print("Testing1")
        # TODO: Stiffener
        #for i in range(0,obj_Struct.Stiff.__len__())

    def calc_design_pressures(self, obj_Rule, obj_Struct, obj_Vess):

        VessData = obj_Rule.get_vessel_data(obj_Vess)

        for i in range(0, obj_Struct.Panel.__len__()):

            PressFact = obj_Rule.get_pressure_factors(obj_Struct, obj_Struct.Panel[i])

            PanData = obj_Rule.measure_panel(obj_Struct.Panel[i])

            InData = PressFact + [PanData[4]] + [obj_Struct.n_CG] + VessData[:3]
            # TODO: there might be a more stable way to do this.

            DesPress = obj_Rule.calc_panel_pressures(InData)

            obj_Struct.Panel[i].assign_design_pressure(DesPress)
            print("Testing2")
        # TODO: stiffener

    def calc_scantling_req(self, obj_Rule, obj_Struct, obj_Vess):

        VessData = obj_Rule.get_vessel_data(obj_Vess)

        for i in range(0, obj_Struct.Panel.__len__()):

            DesPress = obj_Rule.get_design_pressures(obj_Struct, obj_Struct.Panel[i])

            PanData = obj_Rule.measure_panel(obj_Struct.Panel[i])

            InData = (DesPress + PanData[:2] + [PanData[4]] + [VessData[2]] +
                      [VessData[4]] +
                      [obj_Struct.Panel[i].material.tensile_strength] +
                      [obj_Struct.Panel[i].material.yield_strength] +
                      [obj_Struct.Panel[i].material.yield_strength]
                      )  # TODO: there might be a more stable way to do this.

            PanReq = obj_Rule.calc_panel_req(InData)

            obj_Struct.Panel[i].assign_scantling_req(PanReq)
            print("Testing3")
        # TODO: stiffener

    def assign_material_to_all_panels(self, obj_Struct, obj_Material):
        for i in range(0, obj_Struct.Panel.__len__()):
            obj_Struct.Panel[i].assign_material(obj_Material)
        pass

    def assign_recommended_plates(self, obj_Struct, obj_PlaLib):
        for i in range(0, obj_Struct.Panel.__len__()):
            min_t = max(obj_Struct.Panel[i].t_req, obj_Struct.Panel[i].t_MIN)
            all_tp = obj_PlaLib.list_all_thicknesses()
            pos = bisect_left(all_tp, min_t)

            try:
                InData = next((x for x in obj_PlaLib.Plates if x.t_p == all_tp[pos]), None)
            except:
                print("""ERROR: There is no plate with the required thickness,
       largest availaible has been assigned""")
                InData = obj_PlaLib.Plates[-1]

            obj_Struct.Panel[i].assign_plate(InData)
        pass

    def assign_profile(self, profile_obj):
        self.profile_obj = profile_obj
        pass

#    def create_topology(self, s_girder, n_stiff):
#        self.stiff_y_pos = numpy.linspace(0, s_girder, n_stiff+2)
#        self.panel_width = self.stiff_y_pos[n_stiff]
#        self.panel_y_pos = self.stiff_y_pos[1:2+n_stiff] - self.panel_width/2
#        #return stiff_y_pos, panel_width, panel_y_pos
#
#    def define_topology(self, obj_Struct):
##        s_frames=643
##        x_pos=0.325
##        location='bottom'
#        for i in range(0, self.panel_y_pos.__len__()):
#            obj_Struct.Panel[i] = obj_Struct.Panel(self.panel_width, 643, 0.325, self.panel_y_pos[i], 'bottom')
#                
        #self.stiff_obj[i] = self.Stiffener(stiff_y_pos[i], static_length, static_x)



#    def initialize_rule(self,type):
#        import schprog as SP
#        self.Rule = SP.ISO12215(0,0)
#        print('test')
#        pass



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


class GlobalVariableCheck:
    """ Check input variables for typos, negatives and other errors, and promts
        the user to correct the value.
        """

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
                else:
                    ship_object.craft_mode = int(craft_mode_)
            print("craft_mode = ", ship_object.craft_mode)


class Optimizer:
    """ User chooses between different optimization methods depending on what
        type of structural member needs to be optimized.
    """
    pass
    # User chooses optimization method
    # User configures chosen method
    # Run optimization
