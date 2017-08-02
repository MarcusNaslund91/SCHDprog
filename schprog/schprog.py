#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
...

"""

import logging
import math
import numpy
from bisect import bisect_left
import xlsxwriter
from collections import Counter


#from schprog import __version__

__author__ = "Marcus Naslund"
__copyright__ = "Marcus Naslund"
__license__ = "none"

_logger = logging.getLogger(__name__)


class Vessel:
    """ Defines vessel data and operational conditions.
        Gets structure object assigned to it.

        Attributes:
            ...__inti__...
            Objective:
                Inits the vessel object.
            Input:
                LWL: Length at the waterline (float, m)
                bC: Chine beam (float, m)
                mLDC: Loaded displacements mass of the vessel (float, kg)
                beta04: Deadrise angle at 0.4 LWL forward of its aft end (float,
                        10-30, degrees)
                V: Maximum speed at mLDC (float, knots)
                hT: Maximum height from keel to top of superstructure (float, m)
                tC: Canoe draft (float, m)
                fB: Freeboard, distance from fully loaded waterline to deck (float, m)
            Output:
                self.Input

            ...calc_craft_mode...
            Objective:
                Calculates the craft mode according to ISO rules.
            Input:
                self.V, self.LWL
            Output:
                self.craftMode: Running mode of the vessel,
                                displacement(2) or planing(1) (int)

            ...assign_structure...
            Objective:
                Assign Structure object as attribute to self (Vessel object).
            Input:
                objStruct: Object created from the Structure class.
            Output:
                self.objStruct
    """

    def __init__(self, LWL, bC, mLDC, beta04, V, hT, tC, fB):
        """ Inits the vessel object. """
        self.LWL = LWL
        self.bC = bC
        self.mLDC = mLDC
        self.beta04 = beta04  # range 10 - 30 degrees
        self.V = V
        self.hT = hT
        self.tC = tC
        self.fB = fB
        pass
        # TODO: add variable check

    def calc_craft_mode(self):
        """ Calculates the craft mode according to ISO rules:
            Return: 1 (planing) or 2 (displacement) (int)
        """
        if self.V / math.sqrt(self.LWL) < 5:
            craftMode = 2
        else:
            craftMode = 1
        return craftMode

    def assign_structure(self, objStruct):
        """ Assign Structure object as attribute to self (Vessel object). """
        self.Struct = objStruct
        pass


class Structure:
    """ Superclass, configures the structural model on the highest level,
        such as topology and global variables from Rules.

        Gets Panel and Stiffener objects assigned to it. Calculates the
        lightweight of the vessel and the centre of gravity.

        Attributes:
            ...__init__...
            Objective:
                Inits the Structure object.
            Input:
                objVess: Vessel object from Vessel class.
            Output:
                self.mLDC: Loaded displacements mass of the vessel (float, kg)
                self.Strake: Prepare empty list for Strake objects from Strake class.
                self.Panel: Prepare empty list for Panel objects from Panel class.
                self.Stiffener: Prepare empty list for Stiffener objects from Stiffener class.

            ...assign_strake...
            Objective:
                Assign Strake object as attribute to self (Structure object).
            Input:
                objStrak: Strake object
            Output:
                self.objStrak[i]
                
            ...assign_panel...
            Objective:
                Assign Panel object as attribute to self (Structure object).
            Input:
                objPan: Panel object
            Output:
                self.objPan[i]

            ...assign_stiffener...
            Objective:
                Assign Stiffener object as attribute to self (Structure object).
            Input:
                objStiff: Stiffener object
            Output:
                self.objStiff[i]

            ...assign_global_var...
            Objective:
                Assign global variables from Rules as attributes to self (Structure object).
            Input:
                ruleType: The rules that have been used for calculations (string)
                nCG: Dynamic load factor (float, -)
                kDC: Design category factor (float, 0-1 -)
            Output:
                self.Input

            ...calc_total_weight...
            Objective:
                Calculates the total weight of the entire structure
            Input:
                -
            Output:
                self.weight: Total weight of all the structural components (float, kg)

            ...calc_CoG...
            Objective:
                Calculates the centre of gravity (CoG) of the entire structure
            Input:
                -
            Output:
                self.CoG: Centre of gravity of the entire structure (float, m)
    """
    def __init__(self, objVess):
        """ Inits the Structure object. """
        self.mLDC = objVess.mLDC
        self.Strake = []
        self.Panel = []
        self.Stiffener = []
        pass
    
    def assign_strake(self, objStrak):
        """ Assign Strake object as attribute to self (Structure object). """
        self.Strake = self.Strake + [objStrak]
        pass

    def assign_panel(self, objPan):
        """ Assign Panel object as attribute to self (Structure object). """
        self.Panel = self.Panel + [objPan]
        pass

    def assign_stiffener(self, objStiff):
        """ Assign Stiffener object as attribute to self (Structure object). """
        self.Stiffener = self.Stiffener + [objStiff]
        pass

    def assign_global_var(self, inputVec):
        """ Assign global variables from Rules as attributes to self (Structure object). """
        self.ruleType = inputVec[0]
        if self.ruleType == 'ISO':
            self.kDC = inputVec[1]
            self.nCG = inputVec[2]
        pass

    def calc_total_weight(self):
        """ Calculates the total weight of the entire structure """
        panWeight = []
        stiffWeight = []
        for i in range(0, self.Panel.__len__()):
            self.Panel[i].calc_weight()
            panWeight = panWeight + [self.Panel[i].weight]
        panWeight = sum(panWeight)
        try:
            for i in range(0, self.Stiffener.__len__()):
                self.Stiffener[i].calc_weight()
                stiffWeight = stiffWeight + [self.Stiffener[i].weight]
            stiffWeight = sum(stiffWeight)
        except:
            stiffWeight = 0

        self.weight = panWeight + stiffWeight
        pass

    def calc_CoG(self):
        """ Calculates the centre of gravity (CoG) of the entire structure """
        panCoG = []
        stiffCoG = []
        for i in range(0, self.Panel.__len__()):
            self.Panel[i].calc_weight()
            panCoG = (panCoG + 
                      [[self.Panel[i].weight * self.Panel[i].xPos] +
                      [self.Panel[i].weight * self.Panel[i].yPos] +
                      [self.Panel[i].weight * self.Panel[i].zPos]
                      ]
                      )
        panCoG = numpy.array(panCoG) # convert to array in order to use numpy methods
        panCoG = panCoG.sum(axis=0) # sums all columns

        try:
            for i in range(0, self.Stiffener.__len__()):
                self.Stiffener[i].calc_weight()
                stiffCoG = (stiffCoG +
                            [
                             [self.Stiffener[i].weight * self.Stiffener[i].xPos] +
                             [self.Stiffener[i].weight * self.Stiffener[i].yPos] +
                             [self.Stiffener[i].weight * self.Stiffener[i].zPos]
                             ]
                            )
            stiffCoG = numpy.array(stiffCoG) # convert to array in order to use numpy methods
            stiffCoG = stiffCoG.sum(axis=0) # sums all columns

        except:
            stiffCoG = 0

        self.CoG = (panCoG + stiffCoG) / self.weight
        pass


class Stiffener(Structure):
    """ Defines stiffener data such as dimensions, location, material and
        profile, for e.g. longitudinals, frames and girders. Send the data to
        Rules calculator.

        Gets given a nomenclature as an identifier.

        Attributes:
            ...__init__...
            Objective:
                Inits the stiffener objects.
            Input:
                lStiff: Length of the stiffener (float, mm)
                xPos: x-coordinate of the centre of the stiffener from the
                        aft of the vessel. (float, m)
                yPos: y-coordinate of the centre of the stiffener from the
                        mid of the vessel. (float, mm)
                zPos: z-coordinate of the midpoint fo the bottom flange of the
                        stiffener from the keel of the vessel. (float, m)
                sStiff: Spacing/Distance between two stiffeners (float, mm)
                location: Design location of the stiffener e.g. 'bottom' or
                          'side' (string)
                stiffType: The type fo stiffener e.g. 'girder', 'longitudinal'
                           and 'frame'. (string)
                section: section name that the stiffener was created from (string)
            Output:
                self.Input

            ...assign_nomenclature...
            Objective:
                Assign nomenclature to stiffener objects as an identifier.
            Input:
                longiLoc: Transversal/Horizontal location around the vessel with
                      respect to the centreline. (int & 0.5)
                panSpan: Which panels is the stiffener attached to. (string)
            Output:
                self.stiffName

            ...assign_press_factors...
            Objective:
                Assigns the pressure factor as attributes to self (Stiffener objects).
            Input:
                ruleType: The rules that have been used for calculations (string)
                kL: Longitudinal pressure distribution factor (0-1, -)
                kAR_d: Displacement area pressure reduction factor (0-1, -)
                kAR_p: Planing area pressure reduction factor (0-1, -)
                AD: Design area under consideration (float, m2)
                kZ: Vertical pressure distribution factor (0-1, -)
            Output:
                self.Input

            ...assign_design_pressure...
            Objective:
                Assign design pressure as attribute to self (Stiffener object).
            Input:
                ruleType: The rules that have been used for calculations (string)
                pMax: Design pressure (float, kN/m2)
            Output:
                self.ruleType
                self.pMax

            ...assign_material...
            Objective:
                Assign a MaterialsLibrary object as attribute to self
                (stiffener object).
            Input:
                Material: Material object from MaterialsLibrary class.(object)
            Output:
               self.Material

            ...assign_scantling_req...
            Objective:
                Assigns scantling requirements for stiffeners as attributes to
                self (stiffener object).
            Input:
                ruleType: The rules that have been used for calculations (string)
                AwMin: Minimum allowed shear web area (float, m2)
                SMMin: Minimum allowed section modulus (float, m3)
            Output:
                self.Input

            ...assign_profile...
            Objective:
                Assigns a ProfilesLibrary object as attribute to self
                (stiffener object).
            Input:
                Profile: Profile object from ProfilesLibrary class. (object)
            Output:
                self.Profile

            ...calc_weight...
            Objective:
                Calculates weight of the stiffener and assignes it to self
                (stiffener object).
            Input:
                -
            Output:
                self.weight: Weight fo the stiffener. (float, kg)

    """
    def __init__(self, lStiff, xPos, yPos, zPos, sStiff, location, stiffType, section=None):
        """ Inits the stiffener objects. """
        self.lStiff = lStiff
        self.xPos = xPos
        self.yPos = yPos
        self.zPos = zPos
        self.sStiff = sStiff
        self.location = location
        self.stiffType = stiffType # e.g. longitudinal.
        self.section = section
        pass
    
#    def calc_location(self):
#        if self.stiffType in ('longitudinal', 'girder'):
#            if self.zPos < zWL:
#                self.location = 'bottom'
#            elif self.zPos > zWL and self.zPos < zDeck:
#                self.location = 'side'
#            elif self.zPos > zDeck and self.zPos < zSup:
#                self.location = 'deck'
#            elif self.zPos > zSup and self.zPos < zSupTop:
#                self.location = 'superstructures'
#            elif self.zPos > zSupTop:
#                self.location = 'superstructure top'
#            else:
#                print("Error: could not assign a location, check the z-coordinates")
#                
#        elif self.stiffType == 'frame':
#            zTop = self.zPos + self.lStiff/2
#            zBot = self.zPos - self.lStiff/2
#            if zTop < zWL:
#                self.location = 'bottom'
#            elif zTop > zWL and zBot < zWL:
#                self.location = 'bottom&side'
#            else:
#                self.location = 'side'
#            # TODO: add further locations
            

    def assign_nomenclature(self, longiLoc, panSpan): # TODO change this method later.
        """ Assigns nomenclature to the stiffener according to its configuration. """
        if self.stiffType == 'longitudinal':
            nomenclature1 = 'L'
            nomenclature2 = longiLoc
            nomenclature3 = panSpan
            nomenclature = '%s%d %s' % (nomenclature1, nomenclature2, nomenclature3)
        elif self.stiffType == 'frame':
            nomenclature1 = 'Fr'
            nomenclature2 = input("frame number: ")
            nomenclature3 = longiLoc
            nomenclature4 = panSpan
            nomenclature = '%s%s %s' % (nomenclature1, nomenclature2, nomenclature3,
                                        nomenclature4)
        else:  # TODO: add further nomenclature
            pass
        self.stiffName = nomenclature
        pass


    def assign_press_factors(self, inputVec):
        """ Assigns the pressure factor as attributes to self (Stiffener objects). """
        self.ruleType = inputVec[0]
        if self.ruleType == 'ISO':
            # Assign ISO Values
            self.kL = inputVec[1]
            self.kAR_d = inputVec[2]
            self.kAR_p = inputVec[3]
            self.AD = inputVec[4]
            self.kZ = inputVec[5]
        pass

    def assign_design_pressure(self, inputVec):
        """ Assign design pressure as attribute to self (Stiffener object). """
        self.ruleType = inputVec[0]
        if self.ruleType == 'ISO':
            # Assign ISO Values
            self.pMax = inputVec[1]
        pass

    def assign_material(self, objMat):
        """ Assign a MaterialsLibrary object as attribute to self (stiffener object). """
        self.Material = objMat
        pass

    def assign_scantling_req(self, inputVec):
        """ Assigns scantling requirements for stiffeners as attributes to self
        (stiffener object).
        """
        self.ruleType = inputVec[0]
        if self.ruleType == 'ISO':
            # Assign ISO Values
            self.AwMin = inputVec[1]
            self.SMMin = inputVec[2]
        pass

    def assign_profile(self, objProf):
        """ Assigns a ProfilesLibrary object as attribute to self (stiffener object). """
        self.Profile = objProf
        pass

    def calc_weight(self):
        """ Calculates weight of a stiffener and assignes it to self
            (stiffener object).
        """
        self.weight = (self.Profile.Atot*1e-6 * self.lStiff*1e-3
                       * self.Material.density
                       )
        pass


class Strake(Structure):
    """ Defines strakes, which are an assembly of panel between two girders
        and two bulkheads. Contains section objects.
        
        Attributes:
            
            ...__init__...
            Objective:
                inits the strake objects.
            Input:
                strakName: Strake ID name (string)
                sBulkhead: Bulkhead spacing (float, m)
                sGird: Girder spacing (float, mm)
                xPos: Longitudinal postion of the midpoint of the strake (float, m)
                yPos: Horizontal postsion of the migpoint of the strake (float, m)
                zPos: Transversal postsion of the migpoint of the strake (float, m)
                sections: Empty list to prepare for assignments of sections.
            Output:
                self.Input
                
            ...assign_section...
            Objective:
                Assign Section objects to Strake objects.
            Input:
                objSect: section object
            Output:
                self.sections[i]
                
    """
    def __init__(self,strakName, sBulkhead, sGird, xPos, yPos, zPos):
        """ inits the Strake object """
        self.strakName = strakName
        self.sBulkhead = sBulkhead
        self.sGird = sGird
        self.xPos = xPos
        self.yPos = yPos
        self.zPos = zPos
        self.sections = []
    
    def assign_section(self, objSect):
        """ Assigns Section objects to Strake objects """
        self.sections = self.sections + [objSect]
        pass
    
    # Input:
        # Variables for 'Width distribution over normalized length'
        # Panel location (bottom, bottom & side, side, deck, superstructure)

    # Methods:
        # Calculate width distribution over normalized length

    # Output:
        # Width distribution over normalized length
        
class Section(Strake):
    """ Defines a section which is a stiffened panel between two girders and
        two frames. Is assign to a strake and is used for create the topology
        for panel and stiffener objects.
        
        Attributes:
            
            ...__init__...
            Objective:
                inits the section objects
            Input:
                objStrak: Strake object
                secName: Section name (string)
                sGird: Girder spacing (float, mm) 
                sFram: Frame spacing (float, mm)
                xPosGlob: Longitudinal postion of the midpoint of the strake (float, m)
                yPosGlob: Horizontal postsion of the migpoint of the strake (float, m)
                zPosGlob: Transversal postsion of the migpoint of the strake (float, m)
                location: location according to ISO rules e.g. bottom.
            Output:
                self.Input
    """
    
    def __init__(self, objStrak, secName, sGird, sFram, xPosGlob, 
                       yPosGlob, zPosGlob, location):
        """ Create a section between two frames and two girder, consisting of
            panels and stiffeners.
        """
        self.secName = secName
        self.sGird = objStrak.sGird
        self.sFram = sFram
        self.xPosGlob = xPosGlob
        self.yPosGlob = yPosGlob
        self.zPosGlob = zPosGlob
        self.location =  location
        pass

class Panel(Strake):
    """ Defines the panel data according to the choosen rules, such as dimensions,
        location, material and plating. Sends information to the Rules
        calculator.

        User assigns a nomenclature as an identifier.

        Attributes:
            ...__init__...
            Objective:
                Inits the panel objects.
            Input:
                b: Width/Height of the panel (float, mm)
                lPan: Length of panel (float, mm)
                xPos: Distance of mid panel from aft end of LWL (float, m)
                yPos: Height of centre of panel above keel or waterline?? (float, m)
                location: Design location according to rules e.g 'bottom',
                          'side/bottom' and 'side'. (string)
                section: section name, whcih was used to create the panel (string)
            Output:
                self.Input
                self.area: Area of a panel, b x lPan (float, m2)

            ...assign_nomenclature...
            Objective:
                Assigns nomenclature to the Panel as an identifier.
            Input:
                longiLoc: longitudinal location of panel starting from aft.
                          (A-Z, string)
                stiffID: Transversal/Horizonal location around the vessel with
                         respect to attached stiffeners. (int & string indicating
                                                          lower subdivsions)
            Output:
                self.panName

            ...assign_press_factors...
            Objective:
                Assigns the pressure factor as attributes to self (panel objects).
            Input:
                ruleType: The rules that have been used for calculations (string)
                kL: Longitudinal pressure distribution factor (0-1, -)
                kAR_d: Displacement area pressure reduction factor (0-1, -)
                kAR_p: Planing area pressure reduction factor (0-1, -)
                AD: Design area under consideration (float, m2)
                kZ: Vertical pressure distribution factor (0-1, -)
            Output:
                self.Input

            ...assign_design_pressure...
            Objective:
                Assign design pressure as attribute to self (panel object).
            Input:
                ruleType: The rules that have been used for calculations (string)
                pMax: Design pressure (float, kN/m2)
            Output:
                self.ruleType
                self.pMax

            ...assign_material...
            Objetive:
                Assigns a material object as attribute to self (panel object).
            Input:
                Material: Material object from MaterialsLibrary class. (object)
            Output:
                self.Material

            ...assign_scantling_req...
            Objective:
                Assigns scantling requirements for panels as attributes to self
                (panel object).
            Input:
                ruleType: The rules that have been used for calculations (string)
                k2: Panel aspect ratio factor for bending strength (0.308-0.500, -)
                k3: Panel aspect ratio factor for bending stiffness (0.014-0.028, -)
                FShear: Shear force in the middle of the 'b' dimension (float, N/mm)
                MBend: Bending moment in the 'b' direction (float, N/mm)
                tReq: Required thickness for metal plating (float, mm)
                tMin: Single-skin plating minimum thickness for the hull (float, mm)
            Output:
                self.Input

            ...assign_plate...
            Objective:
                Assigns a plating object as attribute to self (panel object).
            Input:
                objPlate: Plating object from the Plating class.
            Output:
                self.objPlate

            ...calc_weight...
            Objective:
                Calculates weight of the panel and assignes it to self
                (panel object).
            Input:
                -
            Output:
                self.weight: Weight of the panel (float, kg)

    """
    def __init__(self, b, lPan, xPos, yPos, zPos, location, section=None):
        """ Inits the panel objects. """
        self.b = b
        self.lPan = lPan
        self.xPos = xPos
        self.yPos = yPos
        self.zPos = zPos
        self.location = location
        self.area = (self.b * self.lPan)*1e-6 #m2
        self.section = section
        pass

    def assign_nomenclature(self, longiLoc, stiffID, segment=' '): # TODO change this method later.
        """ Assigns nomenclature to the stiffener according to its cofiguration. """
        nomenclature1 = longiLoc
        nomenclature2 = stiffID
        nomenclature3 = segment
        nomenclature = '%s%s%s' % (nomenclature1, nomenclature2, nomenclature3)
        self.panName = nomenclature
        pass

    def assign_press_factors(self, inputVec):
        """ Assigns the pressure factor as attributes to self (panel objects). """
        self.ruleType = inputVec[0]
        if self.ruleType == 'ISO':
            # Assign ISO Values
            self.kL = inputVec[1]
            self.kAR_d = inputVec[2]
            self.kAR_p = inputVec[3]
            self.AD = inputVec[4]
            self.kZ = inputVec[5]
        pass

    def assign_design_pressure(self, inputVec):
        """ Assign design pressure as attribute to self (panel object). """
        self.ruleType = inputVec[0]
        if self.ruleType == 'ISO':
            # Assign ISO Values
            self.pMax = inputVec[1]
        pass

    def assign_material(self, objMat):
        """ Assigns a material object as attribute to self (panel object). """
        self.Material = objMat
        pass

    def assign_scantling_req(self, inputVec):
        """ Assigns scantling requirements for panels as attributes to self (panel object). """
        self.ruleType = inputVec[0]
        if self.ruleType == 'ISO':
            # Assign ISO Values
            self.k2 = inputVec[1]
            self.k3 = inputVec[2]
            self.FShear = inputVec[3]
            self.MBend = inputVec[4]
            self.tReq = inputVec[5]
            self.tMin = inputVec[6]
        pass

    def assign_plate(self, objPlate):
        """ Assigns a plating object as attribute to self (panel object). """
        self.Plate = objPlate
        pass

    def calc_weight(self):
        """ calculates the weight of the panel """
        self.weight = (self.area * self.Plate.tp*1e-3
                       * self.Material.density
                       )
        pass


class MaterialsLibrary:
    """ Defines available materials and their respective properties.

        Attributes:
            ...__init__... / ...__repr__...
            Objective:
                Inits material objects. / Format the print function
            Input:
                matLabel: Name of the material (string)
                yieldStrength: Yield strength / sigmaY (float, N/mm2)
                tensileStrength: Tensile strength / sigmaU (float, N/mm2)
                elasticModulus: Elasticity modulus (float, N/mm2)
                shearModulus: Shear modulus (float, N/mm2)
                density: Density (float, kg/m3)
            Output:
                self.Input
    """
    def __init__(self, matLabel,
                 yieldStrength,
                 tensileStrength,
                 elasticModulus,
                 shearModulus,
                 density
                 ):
        self.matLabel = matLabel
        self.yieldStrength = yieldStrength
        self.tensileStrength = tensileStrength
        self.elasticModulus = elasticModulus
        self.shearModulus = shearModulus
        self.density = density
        pass

    def __repr__(self):
        """ States how the print function should print out material instances. """
        return """
        matLabel = %s
        yieldStrength = %d (N/mm2)
        tensileStrength = %d (N/mm2)
        elasticModulus = %d (N/mm2)
        shearModulus = %d (N/mm2)
        density = %d (kg/m3)
        """ % (self.matLabel,
               self.yieldStrength,
               self.tensileStrength,
               self.elasticModulus,
               self.shearModulus,
               self.density
               )
        pass


class PlatingLibrary:
    """ Contains all the available plate data such as thickness from manufacturers.
        The plates are objects from the Plates class which are then assigned as
        attributes.

        Attributes:
            ...__init__...
            Objective:
                Inits plating library object and prepares for plate assignment.
            Input:
                -
            Output:
                self.Plates: Empty list for preperation of assigning plate objects (-)

            ...assign_plate...
            Objective:
                Assigns plating objects as attributes to self (PlatingLibrary object)
                from the Plates class.
            Input:
                Plates: List of plate objects from Plates class (-)
            Output:
                self.Plates

            ...list_all_thicknesses...
            Objective:
                List all of the available plate thicknesses with only numbers.
                Is used for recommended plating assignement.
            Input:
                -
            Output:
                self.allTP: List of all available pate thicknesses (int, mm)
    """
    def __init__(self):
        """ Inits the PlatingLibrary object. """
        self.Plates = []
        pass

    def assign_plate(self, objPlate):
        """ Assigns plating objects as attributes to self (PlatingLibrary object)
            from the Plates class.
        """
        self.Plates = self.Plates + [objPlate]
        pass

    def list_all_thicknesses(self):
        """ List all of the available plate thicknesses with only numbers. """
        allTP = []
        del allTP[:]
        for i in range(0, self.Plates.__len__()):
            allTP = allTP + [self.Plates[i].tp]
        return allTP


class Plates(PlatingLibrary):
    """ Defines plating objects with labels and thicknesses.

        Attributes:
            ...__init__... / ...__repr__...
            Objective:
                Inits the plates object. / Defines how the print function
                                           should print out the plates objects.
            Input:
                platLabel: Name/Label of the plate (string)
                tp: plate thickness (int, mm)
            Output:
                self.Input

    """
    def __init__(self, platLabel, tp):
        """ Inits the plates object. """
        self.platLabel = platLabel
        self.tp = tp
        pass

    def __repr__(self):
        """ Defines how the print function should print out the plates objects. """
        return """
        platLabel = %s
        tp = %d (mm)
        """ % (self.platLabel,
               self.tp)
        pass


class ProfileLibrary:
    """ Library containing structural profiles for e.g. stiffeners, girders
        and frames. User can choose between a set of available extrusions
        or define their own for machining.

    Attributes:
            ...__init__...
            Objective:
                Inits the ProfileLibrary object and prepares for profile assignment.
            Input:
                -
            Output:
                self.Extrusions: Empty list for preperation of assigning extruded
                                 profile objects (-)
                self.Machined: Empty list for preperation of assigning machined
                                profile objects (-)

            ...assign_extrusion...
            Objective:
                Assigns Extrusions objects as attributes to self (ProfileLibrary object)
            Input:
                objProf: Extrusions object from the Extrusions class.
            Output:
                self.Extrusions

            ...assign_machined...
            Objective:
                Assigns Machined objects as attributes to self (ProfileLibrary object)
            Input:
                objProf: Machined object from the Machined class.
            Output:
                self.Machined
                
            ...list_all_machined...
            Objective:
                Returns a list of all machined profile objects. Used for the 
                sweep_method if the user wants to loop through all created 
                machined profiles.
            Input:
                -
            Output:
                allMachined: list of all available Machined objects

    """

    def __init__(self):
        """ Inits the ProfileLibrary object. """
        self.Extrusions = []
        self.Machined = []
        pass

    def assign_extrusion(self, objProf):
        """ Assigns Extrusions objects as attributes to self
            (ProfileLibrary object)
        """
        self.Extrusions = self.Extrusions + [objProf]
        pass

    def assign_machined(self, objProf):
        """ Assigns Machined objects as attributes to self
            (ProfileLibrary object)
        """
        self.Machined = self.Machined + [objProf]
        pass

    def list_all_machined(self):
        """ Returns a list of all machined profile objects. Used for the 
        sweep_method if the user wants to loop through all created machined
        profiles """
        allMachined = []
        del allMachined[:]
        for i in range(0, self.Machined.__len__()):
            allMachined = allMachined + [self.Machined[i]]
        return allMachined

class Extrusions(ProfileLibrary):
    """ Defines the available extruded profiles.

        Attributes:

            ...__init__ / __repr__...
            Objective:
                Inits the Extrusion objects for the profile library. / Defines
                how the print function should print out the plates objects.
            Input:
                profLabel: Name/Label of the profile (string)
                SM: Section moudulus (float, cm3)
                Aw: Shear/Web crossection area (float, cm2)
                tw: Thickness of the web (float, mm)
                hw: Height of the web (float, mm)
                tf: Thickness of the flange (float, mm)
                wf: Width of the flange (float, mm)
                pType: Type of profile e.g. I-beam, L-beam, T-beam etc. (string)
            Output:
                self.Input
                self.Atot: Cross-section area of profile (float, mm2)
    """

    def __init__(self, profLabel, SM, Aw, tw, hw, tf, wf, pType):
        """ Inits the Extrusion objects for the profile library. """
        self.profLabel = profLabel
        self.SM = SM
        self.Aw = Aw
        self.tw = tw
        self.hw = hw
        self.tf = tf
        self.wf = wf
        self.Atot = (self.tw * self.hw) + (self.tf * self.wf)
        self.pType = pType
        pass

    def __repr__(self):
        """ Defines how the print function should print out the profile objects. """
        return """
        profLabel = %s
        SM = %.2f (cm3)
        Aw = %.2f (cm2)
        tw = %.1f (mm)
        hw = %.1f (mm)
        tf = %.1f (mm)
        wf = %.1f (mm)
        Atot = %.2f (mm2)
        pType = %s
        """ % (self.profLabel,
               self.SM,
               self.Aw,
               self.tw,
               self.hw,
               self.tf,
               self.wf,
               self.Atot,
               self.pType)
        pass


class Machined(ProfileLibrary):
    """ User defined machined profiles.

        Attributes:

            ...__init__ / __repr__...
            Objective:
                Inits the Extrusion objects for the profile library. / Defines
                how the print function should print out the plates objects.
            Input:
                profLabel: Name/Label of the profile (string)
                tw: Thickness of the web (float, mm)
                hw: Height of the web (float, mm)
                tf: Thickness of the flange (float, mm)
                wf: Width of the flange (float, mm)
                pType: Type of profile e.g. I-beam, L-beam, T-beam etc. (string)
                Atot: Total cross-section area (float, mm2)
                SM: Section moudulus (float, cm3)
                Aw: Shear/Web crossection area (float, cm2)
            Output:
                self.Input
                self.Atot: Cross-section area of profile (float, mm2)

            ...calc_SM...
            Objective:
                Calculates the section modulus of different types of
                cross-sections.
            Input:
                -
            Output:
                self.SM

    """
    def __init__(self, profLabel, tw, hw, tf, wf, pType):
        """ Inits the Machined objects for the profile library. """
        self.profLabel = profLabel
        self.tw = tw
        self.hw = hw
        self.tf = tf
        self.wf = wf
        self.pType = pType
        self.Atot = (self.tw * self.hw) + (self.tf * self.wf)
        self.SM = self.calc_SM()
        self.Aw = (self.tw * self.hw)*1e-2 # cm2
        pass

    def __repr__(self):
        """ Defines how the print function should print out the profile objects. """
        return """
        profLabel = %s
        SM = %.2f (cm3)
        Aw = %.2f (cm2)
        tw = %.1f (mm)
        hw = %.1f (mm)
        tf = %.1f (mm)
        wf = %.1f (mm)
        Atot = %.2f (mm2)
        pType = %s
        """ % (self.profLabel,
               self.SM,
               self.Aw,
               self.tw,
               self.hw,
               self.tf,
               self.wf,
               self.Atot,
               self.pType)
        pass

    def calc_SM(self):
        """ Calculates the section modulus of different types of cross-sections """
        tw = self.tw*1e-1
        hw = self.hw*1e-1
        tf = self.tf*1e-1
        wf = self.wf*1e-1
        Atot = self.Atot*1e-2
        if self.pType == 'Flat Bar':
            ycog = hw/2
            Ixx = (tw * hw**3) / 12
            SM = Ixx / ycog
        elif self.pType == 'L-shaped':
            Atot = tw * (wf + hw - tf)
            ycog = (hw**2 + wf * tf - tw**2) / (2*(wf + hw - tw))
            Ixx = (1/3)*(wf * hw**3 - (hw-tf) * (wf-tw)**3) - Atot * (hw - ycog)**2
            SM = Ixx / ycog
        elif self.pType == 'T-shaped':
            ycog = (((hw + tf/2) * tf * wf + hw**2 *
                    tw/2) / Atot)
            Ixx = (tw * hw * (ycog - hw/2)**2 +
                   (tw * hw**3)/12 +
                   tf * wf * (hw + tf/2 - ycog)**2 +
                   tf**3 * wf/12
                   )
            SM = Ixx / ycog
        return SM


class Rules:
    """ Stores the different structural rules for designing the structural
        properties and arrangment of the vessel, e.g. ISO12215, DNV, ABS and LR.
    """
    def __init__(self):
        """ Inits the Rules object. """
        pass

    # Input:
        # Variables common to all rules (tricky to know for this version)


class ISO12215(Rules):
    """ Calculates structural requirements according to ISO 12215.

        Attributes:
            ...__init__...
            Objective:
                Inits the ISO rules object.
            Input:
                name: Name of the rules used, set to 'ISO' as default for ISO12215.
                designCategory: Sea and wind conditions for which the vessel will be
                                assessed against. Four different categories can be
                                chosen:
                                    A: ocean
                                    B: offshore
                                    C: inshore
                                    D: sheltered waters
            Output:
                self.name
                self.designCategory

            ...get_vessel_data...
            Objective:
                Collects data from the Vessel object to be used as input for the rules.
            Input:
                objVess: Vessel class object
            Output:
                Vessel data = [LWL, bC, mLDC, beta04, V, craftMode]
                See Vessel class for more information.

            ...calc_global_var...
            Objective:
                Calculates rule variables that apply to the entire vessel.
            Input:
                [LWL, bC, mLDC, beta04, V, craftMode]
                See Vessel class for more information.
            Output:
                ruleType: type of rule that has been used, put to default as 'ISO' (string)
                kDC: Design category factor (0.4:0.2:1, int)
                nCG: Dynamic load factor (float, -)

            ...measure_panel...
            Objective:
                Collects data from Panel objects to be used as input for the rules.
            Input:
                objPan: Panel object from the Panel class
            Output:
                Panel data = [b, lPan, xPos, yPos, location]
                see Panel class for more information.

            ...calc_panel_pressure_factors...
            Objective:
                Calculates the panel PRESSURE ADJUSTING FACTORS from SECTION 7
            Input:
                [b, lPan , xPos, yPos, location, mLDC, nCG, LWL]
            Output:
                ruleType: type of rule that has been used, put to default as 'ISO' (string)
                kL: Longitudinal pressure distribution factor (0-1, -)
                kAR_d: Displacement area pressure reduction factor (0-1, -)
                kAR_p: Planing area pressure reduction factor (0-1, -)
                AD: Design area under consideration (float, m2)
                kZ: Vertical pressure distribution factor (0-1, -)

            ...measure_stiffener...
            Objective:
                Collects data from Stiffener objects to be used as input for the rules.
            Input:
                objStiff: Stiffener object from the stiffener class.
            Output:
                Stiffener data = [lStiff, xPos, yPos, zPos, sStiff, location, stiffType]

            ...calc_stiff_pressure_factors...
            Objective:
                Calculates the stiffener PRESSURE ADJUSTING FACTORS from SECTION 7
            Input:
                [lStiff, xPos, yPos, zPos, sStiff, location, stiffType, mLDC, nCG, LWL]
            Output:
                ruleType: type of rule that has been used, put to default as 'ISO' (string)
                kL: Longitudinal pressure distribution factor (0-1, -)
                kAR_d: Displacement area pressure reduction factor (0-1, -)
                kAR_p: Planing area pressure reduction factor (0-1, -)
                AD: Design area under consideration (float, m2)
                kZ: Vertical pressure distribution factor (0-1, -)

            ...get_press_factors...
            Objective:
                Collects the data for pressure factors from the structure and
                panel/stiffener objects, to be used as input for the rules.
            Input:
                objStruct: Structure object from the Structure class.
                objComp: Panel or Stiffener object from the Panel or Stiffener
                         class respectivly.
            Output:
                Pressure factors = [kDC, kL, kAR_d, kAR_p, kZ]

            ...calc_panel_pressures...
            Objective:
                Calculates the panel DESIGN PRESSURES from SECTION 8.
            Input:
                [kDC, kL, kAR_d, kAR_p, kZ, location, nCG, LWL, bC, mLDC]
            Output:
                ruleType: type of rule that has been used, put to default as 'ISO' (string)
                pMax: Maximum/Design pressure (float, kN/m2)

            ...calc_stiffener_pressures...
            Objective:
                Calculates the stiffener DESIGN PRESSURES from SECTION 8.
            Input:
                [kDC, kL, kAR_d, kAR_p, kZ, location, nCG, LWL, bC, mLDC]
            Output:
                ruleType: type of rule that has been used, put to default as 'ISO' (string)
                pMax: Maximum/Design pressure (float, kN/m2)

            ...get_design_pressures...
            Objective:
                Collects the design pressure for a Panel/Stiffener to be used as
                input for the rules.
            Input:
                objComp: Panel or Stiffener object from the Panel or Stiffener
                         class respectivly.
            Output:
                pMax: Maximum/Design pressure (float, kN/m2)

            ...calc_panel_req...
            Objective:
                Calculates the required thickness for panels.
            Input:
                [pMax, b, lPan, location, mLDC, V, sigmaUW, sigmaY, sigmaYW]
                where:
                    sigmaUW: Ulitimate strength at welded condition (float, N/mm2)
                    sigmaY: Yield strength (float, N/mm2)
                    sigmaYW: Yield strength at welded condition (float, N/mm2)
            Output:
                ruleType: The rules that have been used for calculations (string)
                k2: Panel aspect ratio factor for bending strength (0.308-0.500, -)
                k3: Panel aspect ratio factor for bending stiffness (0.014-0.028, -)
                FShear: Shear force in the middle of the 'b' dimension (float, N/mm)
                MBend: Bending moment in the 'b' direction (float, N/mm)
                tReq: Required thickness for metal plating (float, mm)
                tMin: Single-skin plating minimum thickness for the hull (float, mm)

            ...calc_stiff_req...
            Objective:
                Calculates the STIFFENING MEMBERS REQUIREMENTS, SECTION 11.
            Input:
                [pMax, lStiff, sStiff, sigmaYW]
            Output:
                ruleType: The rules that have been used for calculations (string)
                AwMin: Minimum allowed shear web area (float, m2)
                SMMin: Minimum allowed section modulus (float, m3)
                
            ...check_stiff_prop...
            Objective:
                Maximum proportions between dimensions within a stiffener,
                section 11.7.2.
            Input:
                i: Stiffener list ID nr, eg. objStruct.Stiffener[i] (int)
                sigmaYW: Welded yield strength of stiffener (float, N/mm2)
                Aw: Web area of chosen profile (float, cm2)
                AwMin: Minimum required web area of stiffener (float, cm2)
                sigmaActStiff: Actual stress of the stiffener calculated from
                                calc_stiff_stress (float, N/mm2)
                profType: profile type e.g. Flat Bar, L-shaped (string)
                hw: Profile web height (float, mm)
                tw: Profile web thickness (float, mm)
                wf: Profile flange width (float, mm)
                tf: Profile flange thickness (float, mm)
            Output:
                Error messages or pass if recommended proportion are exceeded.


    """
    def __init__(self, designCategory):
        """ Inits the ISO rules object. """
        self.name = 'ISO'
        self.designCategory = GlobalVariableCheck.check_inputs(GlobalVariableCheck,
                                                               'ISOinit',
                                                               designCategory)
        pass

    def get_vessel_data(self, objVess):
        """ Collects data from the Vessel object to be used as input for the rules. """
        LWL = objVess.LWL
        bC = objVess.bC
        mLDC = objVess.mLDC
        beta04 = objVess.beta04
        V = objVess.V
        hT = objVess.hT
        tC = objVess.tC
        fB = objVess.fB
        craftMode = objVess.calc_craft_mode()
        return [LWL, bC, mLDC, beta04, V, hT, tC, fB, craftMode]

    def calc_global_var(self, inputVec):
        """ Calculates rule variables that apply to the entire vessel. """

        [LWL, bC, mLDC, beta04, V, craftMode] = inputVec

        """ Design catergory factor kDC, section 7.2 """
        if self.designCategory == 'A':
            kDC = 1
        elif self.designCategory == 'B':
            kDC = 0.8
        elif self.designCategory == 'C':
            kDC = 0.6
        elif self.designCategory == 'D':
            kDC = 0.4

        """ DYNAMIC LOAD FACTOR nCG, SECTION 7.3 """
        nCG1 = (0.32 * (LWL / (10*bC) + 0.084) * (50 - beta04) *
                 ((V**2 * bC**2) / mLDC)
                 )
        nCG2 = (0.5 * V) / mLDC**0.17

        """ Dynamimc load factor for planing motor craft in planing mode,
            section 7.3.2.
        """
        if craftMode == 1:
            if nCG1 <= 3.0:
                nCG = nCG1
            elif (3.0 > (nCG1 and nCG2) < 7):
                nCG = max(nCG1, nCG2)
            else:
                nCG = 7

            """ Dynamic load factor for displacement motor craft,
                section 7.3.2.
            """
        elif craftMode == 2:
            if nCG1 <= 3:
                nCG = nCG1
            else:
                print("Your vessel might be going too fast for a displacement craft!")

        GlobVar = ['ISO', kDC, nCG]
        return GlobVar

    def measure_panel(self, objPan):
        """ Collects data from Panel objects to be used as input for the rules. """
        b = objPan.b
        lPan = objPan.lPan
        xPos = objPan.xPos
        zPos = objPan.zPos
        location = objPan.location
        return [b, lPan, xPos, zPos, location]


    def calc_panel_pressure_factors(self, inputVec):
        """ Calculates the panel PRESSURE ADJUSTING FACTORS from SECTION 7 """
        [b, lPan , xPos, zPos, location, mLDC, nCG, LWL, hT, tC, fB] = inputVec

        """ LONGITUDINAL PRESSURE DISTRIBUTION FACTOR 'kL', SECTION 7.4
            First the dynimic load factor has to be modified according to
            section 7.4.
        """
        if nCG < 3:
            nCG_kL = 3
        elif nCG > 6:
            nCG_kL = 6
        else:
            nCG_kL = nCG

        """ Calculate kL, section 7.4 eq 3. """
        if (xPos/LWL) > 0.6:
            kL = 1
        elif (xPos/LWL) <= 0.6:
            kL = ((1 - 0.167 * nCG_kL) / 0.6 *
                   (xPos/LWL) + 0.167 * nCG_kL
                   )
            if kL > 1:
                kL = 1
            else:
                pass
        else:
            pass

        """ AREA PRESSURE REDUCTION FACTOR kAR, SECTION 7.5 """
        """ kR is the structural component and boat type factor """
        kR_p = 1  # annotation "_p" stands for planing mode
        kR_d = 1.5 - 3e-4 * b  # annotation "_d" stands for displacement mode

        """ AD is the design area in m2 """
        AD = (lPan * b) * 1e-6

        """ check maximum and minimum value and modify according to
            section 7.5.1.
        """
        if AD > 2.5e-6 * b ** 2:
            AD = 2.5e-6 * b ** 2
        else:
            AD = AD

            """ Calculate kAR """
        kAR_p = ((kR_p * 0.1 * mLDC ** 0.15) /
                  AD ** 0.3)
        kAR_d = ((kR_d * 0.1 * mLDC ** 0.15) /
                  AD ** 0.3)

        """ check maximum and minimum value and modify according to
            section 7.5.2-3.
        """
        if kAR_p > 1:
            kAR_p = 1
        elif kAR_p < 0.25:
            kAR_p = 0.25
        else:
            kAR_p = kAR_p

        if kAR_d > 1:
            kAR_d = 1
        elif kAR_d < 0.25:
            kAR_d = 0.25
        else:
            kAR_d = kAR_d

        """ HULL SIDE PRESSURE REDUCTION FACTOR kZ, SECTION 7.6. """
        # Z is the height from the fully loaded waterline to the top of the deck
        # h is the height above from the fully loaded waterline to the middle/centre
        # of the plate/stiffener.
        
        if zPos > tC:
            Z = fB # meters
            h = zPos - tC # meters
            kZ = (Z - h) / Z
        else:
            kZ = 1

        PressFact = ['ISO', kL, kAR_d, kAR_p, AD, kZ]

        return PressFact

    def measure_stiffener(self, objStiff):
        """ Collects data from Stiffener objects to be used as input for the rules. """
        lStiff  = objStiff.lStiff
        xPos = objStiff.xPos
        zPos = objStiff.zPos
        sStiff = objStiff.sStiff
        location = objStiff.location
        stiffType = objStiff.stiffType
        return [lStiff, xPos, zPos, sStiff, location, stiffType]

    def calc_stiff_pressure_factors(self, inputVec):
        """ Calculates the stiffener PRESSURE ADJUSTING FACTORS from SECTION 7 """
        [lStiff, xPos, zPos, sStiff, location, stiffType, mLDC, nCG, LWL, hT, tC, fB] = inputVec

        """ LONGITUDINAL PRESSURE DISTRIBUTION FACTOR 'kL', SECTION 7.4
            First the dynimic load factor has to be modified according to
            section 7.4.
        """
        if nCG < 3:
            nCG_kL = 3
        elif nCG > 6:
            nCG_kL = 6
        else:
            nCG_kL = nCG

        """ Calculate kL, section 7.4 eq 3. """
        if (xPos/LWL) > 0.6:
            kL = 1
        elif (xPos/LWL) <= 0.6:
            kL = ((1 - 0.167 * nCG_kL) / 0.6 *
                   (xPos/LWL) + 0.167 * nCG_kL
                   )
            if kL > 1:
                kL = 1
            else:
                pass
        else:
            pass

        """ AREA PRESSURE REDUCTION FACTOR kAR, SECTION 7.5 """
        """ kR is the structural component and boat type factor """
        kR_p = 1
        kR_d = 1 - 2e-4 * lStiff

        """ AD is the design area in m2 """
        AD = (lStiff * sStiff)*1e-6

        """ check maximum and minimum value and modify according to
            section 7.5.1
        """
        if AD < 0.33e-6 * lStiff**2:
            AD = 0.33e-6 * lStiff**2
        else:
            AD = AD

        """ Calculate k_AR """
        kAR_p = ((kR_p * 0.1 * mLDC**0.15) /
        AD**0.3)
        kAR_d = ((kR_d * 0.1 * mLDC**0.15) /
        AD**0.3)

        """ check maximum and minimum value and modify according to
            section 7.5.2-3
        """
        if kAR_p > 1:
            kAR_p = 1
        elif kAR_p < 0.25:
            kAR_p = 0.25
        else:
            kAR_p = kAR_p

        if kAR_d > 1:
            kAR_d = 1
        elif kAR_d < 0.25:
            kAR_d = 0.25
        else:
            kAR_d = kAR_d

        """ HULL SIDE PRESSURE REDUCTION FACTOR kZ, SECTION 7.6. """
        # Z is the height from the fully loaded waterline to the top of the deck
        # h is the height above from the fully loaded waterline to the middle/centre
        # of the plate/stiffener.
        if zPos > tC:
            Z = fB # meters
            h = zPos - tC # meters
            kZ = (Z - h) / Z
        else:
            kZ = 1

        PressFact = ['ISO', kL, kAR_d, kAR_p, AD, kZ]

        return PressFact

    def get_press_factors(self, objStruct, objComp):
        """ Collects the data for pressure factors from the structure and
            panel/stiffener objects, to be used as input for the rules.
        """
        kDC = objStruct.kDC
        kL = objComp.kL
        kAR_d = objComp.kAR_d
        kAR_p = objComp.kAR_p
        kZ = objComp.kZ
        return [kDC, kL, kAR_d, kAR_p, kZ]

    def calc_panel_pressures(self, inputVec):
        """" Calculates the panel DESIGN PRESSURES from SECTION 8. """

        """ MOTOR CRAFT DESIGN PRESSURE, SECTION 8.1 """
        [kDC, kL, kAR_d, kAR_p, kZ, location, nCG, LWL, bC, mLDC] = inputVec

        # TODO: pBase could be moved to the global calculations
        pBBase_d = 2.4*mLDC**0.33 + 20  # displacement mode
        pBBase_p = (0.1*mLDC/(LWL * bC)) * (1 + kDC**0.5 * nCG)  # planing mode

        if location == 'bottom':
            """ BOTTOM DESIGN PRESSURE
                The bottom pressure shall be the greater or 8.1.2 or 8.1.3.
            """
            pMin = 0.45*mLDC**0.33 + (0.9*LWL * kDC)

            """         Displacement mode, section 8.1.2. """
            p_d = pBBase_d * kAR_d * kDC * kL

            """         Planing mode, section 8.1.3. """
            p_p = pBBase_p * kAR_p * kL

            """         Maximum pressure """
            pMax = max(p_d, p_p, pMin)

        elif location == 'side':
            """ SIDE DESIGN PRESSURE
                The side pressure shall be the greater or 8.1.4 or 8.1.5.
            """
            pMin = 0.9*LWL * kDC
            pDBase = 0.35*LWL + 14.6

            """         Displacement mode, section 8.1.4. """
            p_d = ((pDBase + kZ * (pBBase_d - pDBase)) * kAR_d *
                    kDC * kL
                    )

            """         Planing mode, section 8.1.5. """
            p_p = ((pDBase + kZ * (0.25*pBBase_p - pDBase)) * kAR_p *
                    kDC * kL
                    )

            """         Maximum pressure """
            pMax = max(p_d, p_p, pMin)
#        TODO: add bulkhead
#        elif location == 'bulkhead':
#            """ (ignore for now) WATERTIGHT BULKHEADS DESIGN PRESSURE, SECTION 8.3.1 """
#
#            h = lPan  # m, This might be wrong.
#            h_b = (2/3) * h  # m
#            pMax = 7 * h_b   # kN/m2

        DesPress = ['ISO', pMax]

        return DesPress


    def calc_stiffener_pressures(self, inputVec):
        """" Calculates the stiffener DESIGN PRESSURES, SECTION 8. """

        """ MOTOR CRAFT DESIGN PRESSURE, SECTION 8.1 """
        [kDC, kL, kAR_d, kAR_p, kZ, location, nCG, LWL, bC, mLDC] = inputVec

        # TODO: pBase could be moved to the global calculations
        pBBase_d = 2.4*mLDC**0.33 + 20  # kN/m2
        pBBase_p = (0.1*mLDC/(LWL * bC)) * (1 + kDC**0.5 * nCG)  # kN/m2

        if location == 'bottom':
            """ BOTTOM DESIGN PRESSURE
                The bottom pressure shall be the greater or 8.1.2 or 8.1.3.
            """
            pBMin = 0.45*mLDC**0.33 + (0.9*LWL * kDC)  # kN/m2

            """         Displacement mode, section 8.1.2. """
            pB_d = pBBase_d * kAR_d * kDC * kL  # kN/m2

            """         Planing mode, section 8.1.3. """
            pB_p = pBBase_p * kAR_p * kL  # kN/m2

            """         Maximum pressure """
            pMax = max(pB_d, pB_p, pBMin)  # kN/m2

        elif location == 'side':
            """ SIDE DESIGN PRESSURE
                The side pressure shall be the greater or 8.1.4 or 8.1.5.
            """
            pSMin = 0.9*LWL * kDC  # kN/m2
            pDBase = 0.35*LWL + 14.6  # kN/m2

            """         Displacement mode, section 8.1.4. """
            pS_d = (pDBase + kZ * (pBBase_d - pDBase)) * kAR_d * kDC * kL

            """         Planing mode, section 8.1.5. """
            pS_p = (pDBase + kZ * (0.25*pBBase_p - pDBase)) * kAR_p * kDC * kL

            """         Maximum pressure """
            pMax = max(pS_d, pS_p, pSMin) # kN/m2
        # TODO: add bulkhead
#        elif location == 'bulkhead':
#            """ (ignore for now) WATERTIGHT BULKHEADS DESIGN PRESSURE, SECTION 8.3.1 """
#
#            """ ----- Vertical stiffener ----- """
#            h_stiff_vert = lStiff  # m, This might be wrong.
#            h_b_stiff_vert = (2/3) * h_stiff_vert  # m
#            P_WB_stiff_vert = 7 * h_b_stiff_vert   # kN/m2
#
#
#            """ ----- Horizontal stiffener ----- """
#            h_b_stiff_hori = z  # m, This will have to be changed later.
#            P_WB_stiff_hori = 7 * h_b_stiff_hori   # kN/m2

        DesPress = ['ISO', pMax]
        return DesPress

    def get_design_pressures(self, objComp):
        """ Collects the design pressure for a Panel/Stiffener to be used as
            input for the rules.
        """
        pMax = objComp.pMax
        return [pMax]

    def calc_panel_req(self, inputVec):
        """ Calculates the required thickness for panels. """
        [pMax, b, lPan, location, mLDC, V, sigmaUW, sigmaY, sigmaYW] = inputVec

        """ Panel aspect ratio factor, section 10.1.2. """
        """ ----- for strength k2 ----- """
        if (lPan/b) < 2:
            k2 = ((0.271*(lPan/b)**2 + 0.910*(lPan/b) - 0.554) /
                   ((lPan/b)**2 - 0.313*(lPan/b) + 1.351)
                   )
        else:
            k2 = 0.5

        if k2 > 0.5:
            k2 = 0.5
        elif k2 < 0.308:
            k2 = 0.308
        else:
            k2 = k2

        """ ----- for stiffness k3 (for sandwich) ----- """
        k3 = ((0.027*(lPan/b)**2 - 0.029*(lPan/b) + 0.011) /
               ((lPan/b)**2 - 1.463*(lPan/b) + 1.108)
               )

        if k3 > 0.028:
            k3 = 0.028
        elif k3 < 0.014:
            k3 = 0.014
        else:
            k3 = k3

        """ Curvature correction factor kC for curved plates,
            section 10.1.3.
        """
        kC = 1  # TODO: this is for non-curvature, add the proper rules later!

        """ Shear force and bending moment of panel, section 10.1.5. """
        if (lPan/b) < 2:
            kSHC = 0.035 + 0.394*(lPan/b) - 0.09*(lPan/b)**2
        elif (lPan/b) > 4:
            kSHC = 0.5
        else:
            m = (2-4/0.463-0.500)
            kSHC = 0.463 + m*((lPan/b) - 2)

        """ ---- Shear force ---- """
        FShear = (math.sqrt(kC) * kSHC * pMax * b)*1e-3

        """ ---- Bending moment ---- """
        MBend = (83.33 * kC**2 * 2*k2 * pMax * b**2)*1e-6

        """ Design stress for metal plating, section 10.3.1. """
        sigmaD = min(0.6*sigmaUW, 0.9*sigmaYW)

        """ Variables for calculation of minimum thickness for the hull,
            section 10.6.2.
        """
        A = 1
        k5 = math.sqrt(125/sigmaY)
        k7B = 0.02
        k7S = 0
        k8 = 0.1

        """ Required thickness for metal plating, section 10.3.2. """
        tReq = b * kC * math.sqrt((pMax*k2) / (1000*sigmaD))

        if location == 'bottom':
            """ Minimum thickness for the hull, section 10.6.2. """
            tMin = k5 * (A + k7B * V + k8 * mLDC**0.33)

        elif location == 'side':
            """ Minimum thickness for the hull, section 10.6.2. """
            tMin = k5 * (A + k7S * V + k8 * mLDC**0.33)

        PanReq = ['ISO', k2, k3, FShear, MBend, tReq, tMin]
        return PanReq


    def calc_stiff_req(self, inputVec):
        """ Calculates the STIFFENING MEMBERS REQUIREMENTS, SECTION 11. """
        [pMax, lStiff, sStiff, sigmaYW] = inputVec


        """ ADJUSTMENT FACTORS, SECITON 11.2 """
        """ Curvature factor kCS, section 11.2.1. """
        kCS = 1 # TODO: This is for non-curvature, add rules later!

        """ Stiffener shear area factor """

        kSA = 5 # This is for attached to plating
        #kSA = 7.5 # # TODO: This is for other arrangements e.g. floating.

        """ Design stresses, section 11.3. """
        sigmaDStiff = 0.7*sigmaYW
        tauDStiff = 0.4*sigmaYW

        #""" minimum shear strength ???, section 11.3. """
        #tau_min_stiff = 0.58*sigma_yw_stiff  # not sure if I use this or not?

        """ Minimum section modulus and shear/web area, section 11.4.1. """
        AwMin = (kSA * pMax * sStiff * lStiff / tauDStiff)*1e-6  # cm2
        SMMin = (83.33 * kCS * pMax * sStiff * lStiff**2 / sigmaDStiff)*1e-9  # cm3

        StiffReq = ['ISO', AwMin, SMMin]
        return StiffReq

    def check_stiff_prop(self, inputVec):
        """ Maximum proportions between dimensions within a stiffener,
            section 11.7.2
        """
        [i, sigmaYW, Aw, AwMin, sigmaActStiff, profType, hw, tw, wf, tf] = inputVec
        
        sigmaDStiff = 0.7*sigmaYW
        kAS = Aw / AwMin

        if sigmaActStiff > 0.8*sigmaDStiff:
            if profType == 'Flat Bar':
                if (hw/tw) > 12:
                    print ("Error: The stiffener", i, "proportion are bad, hw/tw > 12.")
                else:
                    pass
            elif profType == 'T-shaped':
                d = (wf-tw)/2
                if (d/tf) > 12:
                    print ("Error: The stiffener", i, "proportions are bad, d/tf > 12.")
                elif (hw/tw) > 40:
                    print ("Error: The stiffener", i, "proportions are bad, hw/tw > 40.")
                else:
                    pass
            elif profType == 'L-shaped':
                d = wf-tw
                if (d/tf) > 12:
                    print ("Error: The stiffener", i, "proportions are bad, d/tf > 12.")
                elif (hw/tw) > 40:
                    print ("Error: The stiffener", i, "proportions are bad, hw/tw > 40.")
                else:
                    pass
            else:
                print ("Error: Profile type is not valid (Flat bar, T-shaped, L-shaped)")

        elif sigmaActStiff < 0.8*sigmaDStiff:
            if profType == 'Flat Bar':
                if (hw/tw) > 12:
                    print ("Error: The stiffener", i, "proportions are bad, hw/tw > 12.")
                else:
                    pass
            elif profType == 'T-shaped':
                d = (wf-tw)/2
                if (d/tf) > 12:
                    print ("Error: The stiffener", i, "proportions are bad, d/tf > 12.")
                elif (hw/tw) > 40 * math.sqrt(kAS):
                    print ("Error: The stiffener", i, "proportions are bad, hw/tw > 40 * sqrt(kAS).")
                else:
                    pass
            elif profType == 'L-shaped':
                d = wf-tw
                if (d/tf) > 12:
                    print ("Error: The stiffener", i, "proportions are bad, d/tf > 12.")
                elif (hw/tw) > 40 * math.sqrt(kAS):
                    print ("Error: The stiffener", i, "proportions are bad, hw/tw > 40 * sqrt(kAS).")
                else:
                    pass
            else:
                print ("Error: Profile type is not valid (Flat bar, T-shaped, L-shaped)")
        else:
            pass


class Report:
    """ Creates and updates all the relevant information that the user is
        interested in, such as structural arrangement report, graphs of the
        optimization etc.

        Attributes:
            ...__init__...
            Objective:
                Inits the report object.
            Input:
                -
            Output:
                self

            ...create_scantling_report...
            Objective:
                Create an excel report using 'xlsxwriter' that shows the
                scantlings and requirements, used profiles, topology metadata
                input and structural weight.
            Input:
                filename: name of the excel file. (string)
                objStruct: Structure object
                objDes: Designer object
            Output:
                excel report

            ...create_optimization_report...
            Objective:
                Create an excel report using 'xlsxwriter' that helps the user
                to optimize the structural design.
            Input:
                filename: name of the excel file. (string)
                objOpt: Optimization object e.g. from the sweep method.
            Output:
                excel report
    """
    def __init__(self):
        """ Inits the report object """
        pass

    def create_scantling_report(self, filename, objStruct, objDes):
        # Add a workbook and a worksheet.
        name = '%s.xlsx' % (filename)
        workbook = xlsxwriter.Workbook(name)
        worksheet1 = workbook.add_worksheet('Calculation Results')
        worksheet2 = workbook.add_worksheet('Used Profiles')
        worksheet3 = workbook.add_worksheet('Topology Input')
        worksheet4 = workbook.add_worksheet('Structural Weight')

        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': True, 'text_wrap': True})
        # Add a bold format with a bottom border for table titles.
        tabletitle = workbook.add_format({'bold': True, 'bottom': True,
                                          'align': 'center', 'valign': 'vcenter',})
        # Add colour formats to use for highlighting
        red = workbook.add_format({'bg_color': '#E74C3C'})
        yellow = workbook.add_format({'bg_color': '#F7DC6F'})

        # Add numerical formats
        oneDec = workbook.add_format()
        twoDec = workbook.add_format()
        threeDec = workbook.add_format()
        # Set numerical formats to x decimals
        oneDec.set_num_format('0.0')
        twoDec.set_num_format('0.00')
        threeDec.set_num_format('0.000')


        """____________________WORKSHEET 1_______________________"""
        # Adjust the column width.
        worksheet1.set_column('A:A', 10.5)
        worksheet1.set_column('B:B', 19.5)
        worksheet1.set_column('C:C', 20)
        worksheet1.set_column('D:D', 19)
        worksheet1.set_column('E:E', 19.5)
        worksheet1.set_column('F:F', 19.5)

        """ Panel topology """
        """ BOTTOM """
        # Write some data headers for bottom panel data
        worksheet1.merge_range('A1:F1', 'Bottom Panels', tabletitle)
        worksheet1.write('A2', 'Plating Panel', bold)
        worksheet1.write('B2', 'Length (mm)', bold)
        worksheet1.write('C2', 'Width (mm)', bold)
        worksheet1.write('D2', 'Aspect ratio', bold)
        worksheet1.write('E2', 'Longitudinal Position (m)', bold)
        worksheet1.write('F2', 'Design Pressure (kN/m2)', bold)

        # Panel data we want to write to the worksheet.
        inputList = []
        for i in range(0, objStruct.Panel.__len__()):
            if objStruct.Panel[i].location == 'bottom':
                aspRat = objStruct.Panel[i].lPan/objStruct.Panel[i].b
                assList = ([objStruct.Panel[i].panName] 
                            + [objStruct.Panel[i].lPan]
                            + [objStruct.Panel[i].b] 
                            + [aspRat] 
                            + [objStruct.Panel[i].xPos]
                            + [objStruct.Panel[i].pMax]
                           )
                inputList = inputList + [assList]
            else:
                pass

        # Start from the first cell below the headers.
        row = 2
        col = 0

        # Iterate over the data and write it out row by row.
        for panName, lPan, wPan, AR, xPos, desPress in (inputList):
            worksheet1.write(row, col,     panName)
            worksheet1.write(row, col + 1, lPan)
            worksheet1.write(row, col + 2, wPan)
            worksheet1.write(row, col + 3, AR, threeDec)
            worksheet1.write(row, col + 4, xPos, threeDec)
            worksheet1.write(row, col + 5, desPress, oneDec)
            row += 1
            
        """ SIDE """
        # Write some data headers for side panel data
        merge = 'A%d:F%d' % (row + 2, row + 2)
        h1 = 'A%d' % (row + 3)
        h2 = 'B%d' % (row + 3)
        h3 = 'C%d' % (row + 3)
        h4 = 'D%d' % (row + 3)
        h5 = 'E%d' % (row + 3)
        h6 = 'F%d' % (row + 3)
        worksheet1.merge_range(merge, 'Side Panels', tabletitle)
        worksheet1.write(h1, 'Plating Panel', bold)
        worksheet1.write(h2, 'Length (mm)', bold)
        worksheet1.write(h3, 'Width (mm)', bold)
        worksheet1.write(h4, 'Aspect ratio', bold)
        worksheet1.write(h5, 'Longitudinal Position (m)', bold)
        worksheet1.write(h6, 'Design Pressure (kN/m2)', bold)
        
        # Panel data we want to write to the worksheet.
        inputList = []
        for i in range(0, objStruct.Panel.__len__()):
            if objStruct.Panel[i].location == 'side':
                aspRat = objStruct.Panel[i].lPan/objStruct.Panel[i].b
                assList = ([objStruct.Panel[i].panName] 
                            + [objStruct.Panel[i].lPan]
                            + [objStruct.Panel[i].b] 
                            + [aspRat] 
                            + [objStruct.Panel[i].xPos]
                            + [objStruct.Panel[i].pMax]
                           )
                inputList = inputList + [assList]
            else:
                pass
        
        # Iterate over the data and write it out row by row.
        row = row + 3
        for panName, lPan, wPan, AR, xPos, desPress in (inputList):
            worksheet1.write(row, col,     panName)
            worksheet1.write(row, col + 1, lPan)
            worksheet1.write(row, col + 2, wPan)
            worksheet1.write(row, col + 3, AR, threeDec)
            worksheet1.write(row, col + 4, xPos, threeDec)
            worksheet1.write(row, col + 5, desPress, oneDec)
            row += 1
            
        row_e = row + 3
        
        """ Panel requirements """
        """ BOTTOM """
        # Write some data headers for panel results
        merge = 'A%d:F%d' % (row + 2, row + 2)
        h1 = 'A%d' % (row + 3)
        h2 = 'B%d' % (row + 3)
        h3 = 'C%d' % (row + 3)
        h4 = 'D%d' % (row + 3)
        h5 = 'E%d' % (row + 3)
        h6 = 'F%d' % (row + 3)
        worksheet1.merge_range(merge, 'Bottom Panels Results', tabletitle)
        worksheet1.write(h1, 'Plating Panel', bold)
        worksheet1.write(h2, 'Required Thickness (mm)', bold)
        worksheet1.write(h3, 'Min. Req. Thickness (mm)', bold)
        worksheet1.write(h4, 'Offered Thickness (mm)', bold)
        worksheet1.write(h5, 'Thickness Ratio', bold)
        worksheet1.write(h6, 'Min. Thickness Ratio', bold)

        # Panel data we want to write to the worksheet.
        inputList2 = []
        for i in range(0, objStruct.Panel.__len__()):
            if objStruct.Panel[i].location == 'bottom':
                tRat = objStruct.Panel[i].Plate.tp/objStruct.Panel[i].tReq
                tMinRat = objStruct.Panel[i].Plate.tp/objStruct.Panel[i].tMin
                assList2 = ([objStruct.Panel[i].panName] 
                            + [objStruct.Panel[i].tReq]
                            + [objStruct.Panel[i].tMin] 
                            + [objStruct.Panel[i].Plate.tp]
                            + [tRat] 
                            + [tMinRat]
                            )
                inputList2 = inputList2 + [assList2]

        # Start from the first cell below the headers.
        row = row + 3
        col = 0

        # Iterate over the data and write it out row by row.
        for panName, tReq, tMin, tp, tRat, tMinRat in (inputList2):
            worksheet1.write(row, col,     panName)
            worksheet1.write(row, col + 1, tReq, twoDec)
            worksheet1.write(row, col + 2, tMin, twoDec)
            worksheet1.write(row, col + 3, tp)
            worksheet1.write(row, col + 4, tRat, threeDec)
            worksheet1.write(row, col + 5, tMinRat, threeDec)
            row += 1
            
        row_e2 = row + 3

        rowlenEF = 'E%d:F%d' % (row_e, row)
        rowlenFG = 'F%d:G%d' % (row_e, row)

        # Write a conditional format over a range.
        worksheet1.conditional_format(rowlenEF, {'type': 'cell',
                                              'criteria': '<',
                                              'value': 1.0,
                                              'format': red})
        worksheet1.conditional_format(rowlenEF, {'type': 'cell',
                                              'criteria': 'between',
                                              'minimum':  1.0,
                                              'maximum':  1.06,
                                              'format': yellow})
        """ SIDE """
        # Write some data headers for panel results
        merge = 'A%d:F%d' % (row + 2, row + 2)
        h1 = 'A%d' % (row + 3)
        h2 = 'B%d' % (row + 3)
        h3 = 'C%d' % (row + 3)
        h4 = 'D%d' % (row + 3)
        h5 = 'E%d' % (row + 3)
        h6 = 'F%d' % (row + 3)
        worksheet1.merge_range(merge, 'Side Panels Results', tabletitle)
        worksheet1.write(h1, 'Plating Panel', bold)
        worksheet1.write(h2, 'Required Thickness (mm)', bold)
        worksheet1.write(h3, 'Min. Req. Thickness (mm)', bold)
        worksheet1.write(h4, 'Offered Thickness (mm)', bold)
        worksheet1.write(h5, 'Thickness Ratio', bold)
        worksheet1.write(h6, 'Min. Thickness Ratio', bold)

        # Panel data we want to write to the worksheet.
        inputList2 = []
        for i in range(0, objStruct.Panel.__len__()):
            if objStruct.Panel[i].location == 'side':
                tRat = objStruct.Panel[i].Plate.tp/objStruct.Panel[i].tReq
                tMinRat = objStruct.Panel[i].Plate.tp/objStruct.Panel[i].tMin
                assList2 = ([objStruct.Panel[i].panName] 
                            + [objStruct.Panel[i].tReq]
                            + [objStruct.Panel[i].tMin] 
                            + [objStruct.Panel[i].Plate.tp]
                            + [tRat] 
                            + [tMinRat]
                            )
                inputList2 = inputList2 + [assList2]

        # Start from the first cell below the headers.
        row = row + 3
        col = 0

        # Iterate over the data and write it out row by row.
        for panName, tReq, tMin, tp, tRat, tMinRat in (inputList2):
            worksheet1.write(row, col,     panName)
            worksheet1.write(row, col + 1, tReq, twoDec)
            worksheet1.write(row, col + 2, tMin, twoDec)
            worksheet1.write(row, col + 3, tp)
            worksheet1.write(row, col + 4, tRat, threeDec)
            worksheet1.write(row, col + 5, tMinRat, threeDec)
            row += 1
            
        rowlenEF = 'E%d:F%d' % (row_e2, row)
        rowlenFG = 'F%d:G%d' % (row_e2, row)

        # Write a conditional format over a range.
        worksheet1.conditional_format(rowlenEF, {'type': 'cell',
                                              'criteria': '<',
                                              'value': 1.0,
                                              'format': red})
        worksheet1.conditional_format(rowlenEF, {'type': 'cell',
                                              'criteria': 'between',
                                              'minimum':  1.0,
                                              'maximum':  1.06,
                                              'format': yellow})

        """ Stiffener topology """
        """ BOTTOM """
        # Write some data headers for stiffener data
        merge = 'A%d:E%d' % (row + 2, row + 2)
        h1 = 'A%d' % (row + 3)
        h2 = 'B%d' % (row + 3)
        h3 = 'C%d' % (row + 3)
        h4 = 'D%d' % (row + 3)
        h5 = 'E%d' % (row + 3)
        worksheet1.merge_range(merge, 'Bottom Stiffeners', tabletitle)
        worksheet1.write(h1, 'Stiffener', bold)
        worksheet1.write(h2, 'Length (mm)', bold)
        worksheet1.write(h3, 'Spacing (mm)', bold)
        worksheet1.write(h4, 'Longitudinal Position (m)', bold)
        worksheet1.write(h5, 'Design Pressure (kN/m2)', bold)

        # Stiffener data we want to write to the worksheet.
        inputList3 = []

        if objStruct.Stiffener != []:

            for i in range(0, objStruct.Stiffener.__len__()):
                if objStruct.Stiffener[i].location == 'bottom':
                    assList3 = ([objStruct.Stiffener[i].stiffName] 
                                + [objStruct.Stiffener[i].lStiff]
                                + [objStruct.Stiffener[i].sStiff] 
                                + [objStruct.Stiffener[i].xPos]
                                + [objStruct.Stiffener[i].pMax]
                                )
                    inputList3 = inputList3 + [assList3]

            # Start from the first cell below the headers.
            row = row + 3
            col = 0

            # Iterate over the data and write it out row by row.
            for stiffName, lStiff, sStiff, xPos, pMax in (inputList3):
                worksheet1.write(row, col,     stiffName)
                worksheet1.write(row, col + 1, lStiff)
                worksheet1.write(row, col + 2, sStiff)
                worksheet1.write(row, col + 3, xPos, threeDec)
                worksheet1.write(row, col + 4, pMax, oneDec)
                row += 1

        else:
            inputList3 = 'None'
            # Start from the first cell below the headers.
            row = row + 3
            col = 0
            worksheet1.write(row, col,     inputList3)
            
        
            
        """ SIDE """
        # Write some data headers for stiffener data
        merge = 'A%d:E%d' % (row + 2, row + 2)
        h1 = 'A%d' % (row + 3)
        h2 = 'B%d' % (row + 3)
        h3 = 'C%d' % (row + 3)
        h4 = 'D%d' % (row + 3)
        h5 = 'E%d' % (row + 3)
        worksheet1.merge_range(merge, 'Side Stiffeners', tabletitle)
        worksheet1.write(h1, 'Stiffener', bold)
        worksheet1.write(h2, 'Length (mm)', bold)
        worksheet1.write(h3, 'Spacing (mm)', bold)
        worksheet1.write(h4, 'Longitudinal Position (m)', bold)
        worksheet1.write(h5, 'Design Pressure (kN/m2)', bold)
        
        # Stiffener data we want to write to the worksheet.
        inputList3 = []

        if objStruct.Stiffener != []:

            for i in range(0, objStruct.Stiffener.__len__()):
                if objStruct.Stiffener[i].location == 'side':
                    assList3 = ([objStruct.Stiffener[i].stiffName] 
                                + [objStruct.Stiffener[i].lStiff]
                                + [objStruct.Stiffener[i].sStiff] 
                                + [objStruct.Stiffener[i].xPos]
                                + [objStruct.Stiffener[i].pMax]
                                )
                    inputList3 = inputList3 + [assList3]

            # Start from the first cell below the headers.
            row = row + 3
            col = 0

            # Iterate over the data and write it out row by row.
            for stiffName, lStiff, sStiff, xPos, pMax in (inputList3):
                worksheet1.write(row, col,     stiffName)
                worksheet1.write(row, col + 1, lStiff)
                worksheet1.write(row, col + 2, sStiff)
                worksheet1.write(row, col + 3, xPos, threeDec)
                worksheet1.write(row, col + 4, pMax, oneDec)
                row += 1

        else:
            inputList3 = 'None'
            # Start from the first cell below the headers.
            row = row + 3
            col = 0
            worksheet1.write(row, col,     inputList3)
        
        row_e = row + 3


        """ Stiffener requirements """
        """ BOTTOM """
        # Write some data headers for stiffener results
        merge = 'A%d:G%d' % (row + 2, row + 2)
        h1 = 'A%d' % (row + 3)
        h2 = 'B%d' % (row + 3)
        h3 = 'C%d' % (row + 3)
        h4 = 'D%d' % (row + 3)
        h5 = 'E%d' % (row + 3)
        h6 = 'F%d' % (row + 3)
        h7 = 'G%d' % (row + 3)
        worksheet1.merge_range(merge, 'Bottom Stiffeners Results', tabletitle)
        worksheet1.write(h1, 'Stiffener', bold)
        worksheet1.write(h2, 'Req. SM (cm3)', bold)
        worksheet1.write(h3, 'Req. Aw (cm2)', bold)
        worksheet1.write(h4, 'Offered SM (cm3)', bold)
        worksheet1.write(h5, 'Offered Aw (cm2)', bold)
        worksheet1.write(h6, 'SM Ratio', bold)
        worksheet1.write(h7, 'Aw Ratio', bold)

        # Stiffener data we want to write to the worksheet.
        inputList4 = []
        if objStruct.Stiffener != []:
            for i in range(0, objStruct.Stiffener.__len__()):
                if objStruct.Stiffener[i].location == 'bottom':
                    SMRat = objStruct.Stiffener[i].Profile.SM/objStruct.Stiffener[i].SMMin
                    AwRat = objStruct.Stiffener[i].Profile.Aw/objStruct.Stiffener[i].AwMin
                    assList4 = ([objStruct.Stiffener[i].stiffName]
                                + [objStruct.Stiffener[i].SMMin]
                                + [objStruct.Stiffener[i].AwMin]
                                + [objStruct.Stiffener[i].Profile.SM]
                                + [objStruct.Stiffener[i].Profile.Aw]
                                + [SMRat] 
                                + [AwRat]
                                )
                    inputList4 = inputList4 + [assList4]

            # Start from the first cell below the headers.
            row = row + 3
            col = 0

            # Iterate over the data and write it out row by row.
            for stiffName, SMMin, AwMin, SM, Aw, SMRat, AwRat in (inputList4):
                worksheet1.write(row, col,     stiffName, threeDec)
                worksheet1.write(row, col + 1, SMMin, threeDec)
                worksheet1.write(row, col + 2, AwMin, threeDec)
                worksheet1.write(row, col + 3, SM, threeDec)
                worksheet1.write(row, col + 4, Aw, threeDec)
                worksheet1.write(row, col + 5, SMRat, threeDec)
                worksheet1.write(row, col + 6, AwRat, threeDec)
                row += 1

        else:
            # Start from the first cell below the headers.
            row = row + 3
            col = 0
            # Write data
            worksheet1.write(row, col, 'None')

        row_e2 = row + 3
        
        rowlenFG = 'F%d:G%d' % (row_e, row)

        # Write a conditional format over a range.
        worksheet1.conditional_format(rowlenFG, {'type': 'cell',
                                              'criteria': '<',
                                              'value': 1.0,
                                              'format': red})
        worksheet1.conditional_format(rowlenFG, {'type': 'cell',
                                              'criteria': 'between',
                                              'minimum':  1.0,
                                              'maximum':  1.06,
                                              'format': yellow})
        
        """ SIDE """
        # Write some data headers for stiffener results
        merge = 'A%d:G%d' % (row + 2, row + 2)
        h1 = 'A%d' % (row + 3)
        h2 = 'B%d' % (row + 3)
        h3 = 'C%d' % (row + 3)
        h4 = 'D%d' % (row + 3)
        h5 = 'E%d' % (row + 3)
        h6 = 'F%d' % (row + 3)
        h7 = 'G%d' % (row + 3)
        worksheet1.merge_range(merge, 'Side Stiffeners Results', tabletitle)
        worksheet1.write(h1, 'Stiffener', bold)
        worksheet1.write(h2, 'Req. SM (cm3)', bold)
        worksheet1.write(h3, 'Req. Aw (cm2)', bold)
        worksheet1.write(h4, 'Offered SM (cm3)', bold)
        worksheet1.write(h5, 'Offered Aw (cm2)', bold)
        worksheet1.write(h6, 'SM Ratio', bold)
        worksheet1.write(h7, 'Aw Ratio', bold)

        # Stiffener data we want to write to the worksheet.
        inputList4 = []
        if objStruct.Stiffener != []:
            for i in range(0, objStruct.Stiffener.__len__()):
                if objStruct.Stiffener[i].location == 'side':
                    SMRat = objStruct.Stiffener[i].Profile.SM/objStruct.Stiffener[i].SMMin
                    AwRat = objStruct.Stiffener[i].Profile.Aw/objStruct.Stiffener[i].AwMin
                    assList4 = ([objStruct.Stiffener[i].stiffName]
                                + [objStruct.Stiffener[i].SMMin]
                                + [objStruct.Stiffener[i].AwMin]
                                + [objStruct.Stiffener[i].Profile.SM]
                                + [objStruct.Stiffener[i].Profile.Aw]
                                + [SMRat] 
                                + [AwRat]
                                )
                    inputList4 = inputList4 + [assList4]

            # Start from the first cell below the headers.
            row = row + 3
            col = 0

            # Iterate over the data and write it out row by row.
            for stiffName, SMMin, AwMin, SM, Aw, SMRat, AwRat in (inputList4):
                worksheet1.write(row, col,     stiffName, threeDec)
                worksheet1.write(row, col + 1, SMMin, threeDec)
                worksheet1.write(row, col + 2, AwMin, threeDec)
                worksheet1.write(row, col + 3, SM, threeDec)
                worksheet1.write(row, col + 4, Aw, threeDec)
                worksheet1.write(row, col + 5, SMRat, threeDec)
                worksheet1.write(row, col + 6, AwRat, threeDec)
                row += 1

        else:
            # Start from the first cell below the headers.
            row = row + 3
            col = 0
            # Write data
            worksheet1.write(row, col, 'None')

        rowlenFG = 'F%d:G%d' % (row_e2, row)

        # Write a conditional format over a range.
        worksheet1.conditional_format(rowlenFG, {'type': 'cell',
                                              'criteria': '<',
                                              'value': 1.0,
                                              'format': red})
        worksheet1.conditional_format(rowlenFG, {'type': 'cell',
                                              'criteria': 'between',
                                              'minimum':  1.0,
                                              'maximum':  1.06,
                                              'format': yellow})

        """____________________WORKSHEET 2_______________________"""
        """ Used Profiles """
        # Adjust the column width.
        worksheet2.set_column('A:A', 20)
        worksheet2.set_column('B:B', 15)
        worksheet2.set_column('C:C', 17.5)
        worksheet2.set_column('D:D', 14)
        worksheet2.set_column('E:E', 16.5)
        worksheet2.set_column('F:F', 6)

        # Write some data headers for panel data
        worksheet2.write('A1', 'Profile Label', bold)
        worksheet2.write('B1', 'Flange Width (mm)', bold)
        worksheet2.write('C1', 'Flange Thickness (mm)', bold)
        worksheet2.write('D1', 'Web Height (mm)', bold)
        worksheet2.write('E1', 'Web Thickness (mm)', bold)
        worksheet2.write('F1', 'Type', bold)

        # Stiffener data we want to write to the worksheet.
        profiles = []
        for i in range(0, objStruct.Stiffener.__len__()):
            profiles = profiles + [objStruct.Stiffener[i].Profile]

        uniqueItems = list(set(profiles))
        inputList5 = []
        for i in range(0, uniqueItems.__len__()):
            assList5 = ([uniqueItems[i].profLabel] 
                        + [uniqueItems[i].wf]
                        + [uniqueItems[i].tf] 
                        + [uniqueItems[i].hw]
                        + [uniqueItems[i].tw] 
                        + [uniqueItems[i].pType]
                        )
            inputList5 = inputList5 + [assList5]

                # Start from the first cell below the headers.
        row = 1
        col = 0

        if inputList5 != []:
            # Iterate over the data and write it out row by row.
            for profLabel, wf, tf, hw, tw, pType in (inputList5):
                worksheet2.write(row, col,     profLabel)
                worksheet2.write(row, col + 1, wf, oneDec)
                worksheet2.write(row, col + 2, tf, twoDec)
                worksheet2.write(row, col + 3, hw, twoDec)
                worksheet2.write(row, col + 4, tw, twoDec)
                worksheet2.write(row, col + 5, pType)
                row += 1
        else:
            worksheet2.write(row, col, 'None')

        """____________________WORKSHEET 3_______________________"""
        """ Topology Input """
        # Adjust the column width.
        worksheet3.set_column('A:A', 9)
        worksheet3.set_column('B:B', 8.5)
        worksheet3.set_column('C:C', 10.5)
        worksheet3.set_column('D:D', 8.5)
        worksheet3.set_column('E:E', 12)
        worksheet3.set_column('F:F', 12)
        worksheet3.set_column('G:G', 11)
        worksheet3.set_column('H:H', 11)
        worksheet3.set_column('I:I', 11)
        worksheet3.set_column('J:J', 6.5)
        worksheet3.set_column('K:K', 8.5)

        # insert image explaining structure nomenclature
        worksheet3.insert_image('L2', '../schprog/nomenclature_longi.png')
        worksheet3.insert_image('L17', '../schprog/nomenclature_trans.png')


        # Write some data headers for stiffener data
        worksheet3.write('A1', 'Strake ID, strakName', bold)
        worksheet3.write('B1', 'Section ID, secName', bold)
        worksheet3.write('C1', 'Component', bold)
        worksheet3.write('D1', 'ID Name, panName & stiffName', bold)
        worksheet3.write('E1', 'Section Width, sGird (mm)', bold)
        worksheet3.write('F1', 'Section Length, sFram (mm)', bold)
        worksheet3.write('G1', 'x-coordinate, xPosGlob, (m)', bold)
        worksheet3.write('H1', 'y-coordinate, yPosGlob, (m)', bold)
        worksheet3.write('I1', 'z-coordinate, zPosGlob, (m)', bold)
        worksheet3.write('J1', 'location', bold)
        worksheet3.write('K1', 'Number of Stiffeners, nStiff', bold)


        # Stiffener data we want to write to the worksheet.
        inputList6 = []
        
        for i in range(0, objStruct.Strake.__len__()):
            for j in range(0, objStruct.Strake[i].sections.__len__()):
                for k in range(0, objStruct.Panel.__len__()):
                    if objStruct.Strake[i].sections[j].secName == objStruct.Panel[k].section:
                        assList6 = ([objStruct.Strake[i].strakName]
                                    + [objStruct.Strake[i].sections[j].secName]
                                    + ['Panel' + ' ' + str(j+1)]
                                    + [objStruct.Panel[k].panName]
                                    + [objStruct.Strake[i].sections[j].sGird] 
                                    + [objStruct.Strake[i].sections[j].sFram]
                                    + [objStruct.Strake[i].sections[j].xPosGlob] 
                                    + [objStruct.Strake[i].sections[j].yPosGlob]
                                    + [objStruct.Strake[i].sections[j].zPosGlob]
                                    + [objStruct.Strake[i].sections[j].location]
                                    + [objStruct.Strake[i].sections[j].nStiff]
                                    )
                        inputList6 = inputList6 + [assList6]
        
            if objStruct.Stiffener != []:
                    for j in range(0, objStruct.Strake[i].sections.__len__()):
                        for k in range(0, objStruct.Stiffener.__len__()):
                            if objStruct.Strake[i].sections[j].secName == objStruct.Stiffener[k].section:
                                assList6b = ([objStruct.Strake[i].strakName]
                                            + [objStruct.Strake[i].sections[j].secName]
                                            + [objStruct.Stiffener[i].stiffType + ' ' + str(i+1)]
                                            + [objStruct.Stiffener[i].stiffName]
                                            + [objStruct.Strake[i].sections[j].sGird] 
                                            + [objStruct.Strake[i].sections[j].sFram]
                                            + [objStruct.Strake[i].sections[j].xPosGlob] 
                                            + [objStruct.Strake[i].sections[j].yPosGlob]
                                            + [objStruct.Strake[i].sections[j].zPosGlob]
                                            + [objStruct.Strake[i].sections[j].location]
                                            + [objStruct.Strake[i].sections[j].nStiff]
                                            )
                                inputList6 = inputList6 + [assList6b]
            else:
                pass
            

        # Start from the first cell below the headers.
        row = 1
        col = 0

        # Iterate over the data and write it out row by row.
        for (strakName, secName, comp, compID, sGird, sFrame, xPos, yPos, zPos, 
             location, nStiff) in (inputList6):
            worksheet3.write(row, col,     strakName)
            worksheet3.write(row, col + 1, secName)
            worksheet3.write(row, col + 2, comp)
            worksheet3.write(row, col + 3, compID)
            worksheet3.write(row, col + 4, sGird)
            worksheet3.write(row, col + 5, sFrame)
            worksheet3.write(row, col + 6, xPos)
            worksheet3.write(row, col + 7, yPos)
            worksheet3.write(row, col + 8, zPos)
            worksheet3.write(row, col + 9, location)
            worksheet3.write(row, col + 10, nStiff)
            row += 1

        """____________________WORKSHEET 4_______________________"""
        """ Structural Weight """

        """     Stiffeners weight """
        # Adjust the column width.
        worksheet4.set_column('A:A', 7)
        worksheet4.set_column('B:B', 16.5)
        worksheet4.set_column('C:C', 9)

        # Write some data headers for stiffener data
        worksheet4.write('A1', 'Stiffener', bold)
        worksheet4.write('B1', 'Length Perimeter (m)', bold)
        worksheet4.write('C1', 'Weigth (kg)', bold)

        # Stiffener data we want to write to the worksheet.
        inputList7 = []
        if objStruct.Stiffener != []:
            for i in range(0, objStruct.Stiffener.__len__()):
                objStruct.Stiffener[i].calc_weight()
                length = objStruct.Stiffener[i].lStiff*1e-3

                assList7 = ([objStruct.Stiffener[i].stiffName]
                            + [length]
                            + [objStruct.Stiffener[i].weight]
                            )
                inputList7 = inputList7 + [assList7]
            inputList7 = sorted(inputList7)

            # Start from the first cell below the headers.
            row = 1
            col = 0

            # Iterate over the data and write it out row by row.
            for stiffName, lStiff, sWeight in (inputList7):
                worksheet4.write(row, col,     stiffName)
                worksheet4.write(row, col + 1, lStiff, threeDec)
                worksheet4.write(row, col + 2, sWeight, oneDec)
                row += 1

            rowt = row + 1 # this is used for the total structural weigth

            # Write a total using a formula.
            formula1 = '=SUM(B2:B%d)' % (row)
            formula2 = '=SUM(C2:C%d)' % (row)
            worksheet4.write(row, 0, 'Total', bold)
            worksheet4.write(row, 1, formula1, threeDec)
            worksheet4.write(row, 2, formula2, oneDec)

        else:
            # Start from the first cell below the headers.
            row = 1
            col = 0
            # Write data
            worksheet4.write(row, col,     'None')



        """     Plating weight """
        # Adjust the column width.
        worksheet4.set_column('E:E', 13.5)
        worksheet4.set_column('F:F', 8)
        worksheet4.set_column('G:G', 9)

        # Write some data headers for stiffener data
        worksheet4.write('E1', 'Plating', bold)
        worksheet4.write('F1', 'Area (m2)', bold)
        worksheet4.write('G1', 'Weigth (kg)', bold)

        # Gather all plates that have been used.
        inputList8 = []
        for i in range(0, objStruct.Panel.__len__()):
            objStruct.Panel[i].calc_weight()

            assList8 = ([objStruct.Panel[i].Plate.platLabel]
                        + [objStruct.Panel[i].area]
                        + [objStruct.Panel[i].weight]
                        )
            inputList8 = inputList8 + [assList8]

        # Sum up all areas and weight with respect plate label/thickness.
        a = Counter()
        w = Counter()
        for label, area, weight in inputList8:
            a[label] += area
            w[label] += weight
        label = list(a.keys())
        area = list(a.values())
        weight = list(w.values())

        # Plating data we want to write to worksheet.
        inputList9 = []
        for i in range(0, label.__len__()):
            sumList = [label[i]] + [area[i]] + [weight[i]]
            inputList9 = inputList9 + [sumList]
        inputList9 = sorted(inputList9, reverse=True)

        # Start from the first cell below the headers.
        row = 1
        col = 4

        # Iterate over the data and write it out row by row.
        for label, area, weight in (inputList9):
            worksheet4.write(row, col,     label)
            worksheet4.write(row, col + 1, area, twoDec)
            worksheet4.write(row, col + 2, weight, oneDec)
            row += 1

        # Write a total using a formula.
        formula1 = '=SUM(C2:C%d)' % (row)
        formula2 = '=SUM(G2:G%d)' % (row)
        worksheet4.write(row, col,      'Total', bold)
        worksheet4.write(row, col + 1, formula1, twoDec)
        worksheet4.write(row, col + 2, formula2, twoDec)

        # format cells with colors

        red = workbook.add_format({'bg_color': '#E74C3C'})
        purple = workbook.add_format({'bg_color': '#AF7AC5'})
        darkblue = workbook.add_format({'bg_color': '#3498DB'})
        blue = workbook.add_format({'bg_color': '#85C1E9'})
        green = workbook.add_format({'bg_color': '#82E0AA'})

        # Write a conditional format over a range.
        worksheet4.conditional_format('E2:E7', {'type': 'cell',
                                                'criteria': '==',
                                                'value': '"AL10"',
                                                'format': red})
        worksheet4.conditional_format('E2:E7', {'type': 'cell',
                                                'criteria': '==',
                                                'value': '"AL8"',
                                                'format': purple})
        worksheet4.conditional_format('E2:E7', {'type': 'cell',
                                                'criteria': '==',
                                                'value': '"AL5"',
                                                'format': darkblue})
        worksheet4.conditional_format('E2:E7', {'type': 'cell',
                                                'criteria': '==',
                                                'value': '"AL4"',
                                                'format': blue})
        worksheet4.conditional_format('E2:E7', {'type': 'cell',
                                                'criteria': '==',
                                                'value': '"AL3"',
                                                'format': green})

        # Write a total using a formula.
        row = row + 2
        merge = 'E%d:F%d' % (row+1, row+1)
        formula1 = '=C%d' % (rowt)
        formula2 = '=G%d' % (row - 1)
        formula3 = '=SUM(F%d:F%d)' % (row+2, row+3)
        worksheet4.merge_range(merge, 'Total Structural Weight (kg)', tabletitle)
        worksheet4.write(row + 1,     col,       'Stiffeners Weight')
        worksheet4.write(row + 2,     col,           'Panels Weight')
        worksheet4.write(row + 3,     col,                   'Total', bold)
        worksheet4.write(row + 1, col + 1,                  formula1, twoDec)
        worksheet4.write(row + 2, col + 1,                  formula2, twoDec)
        worksheet4.write(row + 3, col + 1,                  formula3, twoDec)

        workbook.close()
        pass

    def create_optimization_report(self, filename, objOpt):
        """ creates an excel report of the optimization methods """
        # Add a workbook and a worksheet.
        name = '%s.xlsx' % (filename)
        workbook = xlsxwriter.Workbook(name)
        worksheet1 = workbook.add_worksheet('Sweep Method')

        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': True, 'text_wrap': True})
        # Add a bold format with a bottom border for table titles.
        tabletitle = workbook.add_format({'bold': True, 'bottom': True,
                                          'align': 'center', 'valign': 'vcenter',})

        # Add numerical formats
        oneDec = workbook.add_format()
        twoDec = workbook.add_format()
        threeDec = workbook.add_format()
        # Set numerical formats to x decimals
        oneDec.set_num_format('0.0')
        twoDec.set_num_format('0.00')
        threeDec.set_num_format('0.000')

        """____________________WORKSHEET 1_______________________"""
        # Adjust the column width.
        worksheet1.set_column('A:A', 8.5)
        worksheet1.set_column('B:B', 12.5)
        worksheet1.set_column('C:C', 12.5)
        worksheet1.set_column('D:D', 8.0)
        worksheet1.set_column('E:E', 12.0)
        worksheet1.set_column('F:F', 4.5)
        worksheet1.set_column('G:G', 4.5)
        worksheet1.set_column('H:H', 6.5)
        worksheet1.set_column('I:I', 6.5)
        worksheet1.set_column('J:J', 5.5)
        worksheet1.set_column('K:K', 5.5)
        worksheet1.set_column('L:L', 7.0)
        worksheet1.set_column('M:M', 6.0)
        worksheet1.set_column('N:N', 6.0)

        """ Extrusions """
        # Write some data headers for optimization data
        worksheet1.merge_range('A1:N1', 'Extruded Profiles', tabletitle)
        worksheet1.merge_range('A2:E2', 'Input Data', tabletitle)
        worksheet1.write('A3', 'Number of Stiffeners', bold)
        worksheet1.write('B3', 'Plating Material', bold)
        worksheet1.write('C3', 'Profile Material', bold)
        worksheet1.write('D3', 'Plating Thickness (mm)', bold)
        worksheet1.write('E3', 'Profile (mm)', bold)
        worksheet1.merge_range('F2:G2', 'Offered', tabletitle)
        worksheet1.write('F3', 'SM (cm3)', bold)
        worksheet1.write('G3', 'Aw (cm2)', bold)
        worksheet1.merge_range('H2:I2', 'Required', tabletitle)
        worksheet1.write('H3', 'SM Min (cm3)', bold)
        worksheet1.write('I3', 'Aw Min (cm2)', bold)
        worksheet1.merge_range('J2:N2', 'Results', tabletitle)
        worksheet1.write('J3', 'SM ratio', bold)
        worksheet1.write('K3', 'Aw Ratio', bold)
        worksheet1.write('L3', 'Stiffener Weight (kg)', bold)
        worksheet1.write('M3', 'Plating Weight (kg)', bold)
        worksheet1.write('N3', 'Total Weight (kg)', bold)

        # optimization data we want to write to the worksheet.
        inputList = objOpt.sweep[0]


        # Start from the first cell below the headers.
        row = 3
        col = 0

        # Iterate over the data and write it out row by row.
        for (nStiff, panMat, stiffMat, tp, profile, SM, Aw, SMMin, AwMin, SMRat,
             AwRat, platWeight, stiffWeight, totWeight) in (inputList):
            worksheet1.write(row, col,     nStiff)
            worksheet1.write(row, col + 1, panMat)
            worksheet1.write(row, col + 2, stiffMat)
            worksheet1.write(row, col + 3, tp)
            worksheet1.write(row, col + 4, profile)
            worksheet1.write(row, col + 5, SM, threeDec)
            worksheet1.write(row, col + 6, Aw, threeDec)
            worksheet1.write(row, col + 7, SMMin, threeDec)
            worksheet1.write(row, col + 8, AwMin, threeDec)
            worksheet1.write(row, col + 9, SMRat, threeDec)
            worksheet1.write(row, col + 10, AwRat, threeDec)
            worksheet1.write(row, col + 11, platWeight, twoDec)
            worksheet1.write(row, col + 12, stiffWeight, twoDec)
            worksheet1.write(row, col + 13, totWeight, twoDec)
            row += 1

        row_e = row + 4 # used in formatting for machined

        # format cells with colors

        red = workbook.add_format({'bg_color': '#E74C3C'})
        yellow = workbook.add_format({'bg_color': '#F7DC6F'})
        green = workbook.add_format({'bg_color': '#82E0AA'})

        # calculate the minimum weight with a section modulus ratio > 1
        # TODO: This only checks the SM ratio, add Aw ratio later.
        secMs = []
        for i in range(0, objOpt.sweep[0].__len__()):
            # Gather all SMs ratios that are > 1
            if objOpt.sweep[0][i][9] > 1:
                secMs = secMs + [[i] + [objOpt.sweep[0][i][9]] + [objOpt.sweep[0][i][-1]]]
            else:
                pass

        allW = []
        for j in range(0, secMs.__len__()):
            # Gather all the weights from the SMs list above and find the minimum
            allW = allW + [secMs[j][-1]]
        minw = min(allW)
        indices = [ind for ind, val in enumerate(allW) if val == minw]

        minWs = []
        for k in indices:
            # Gather all the property combinations that give the minimum weight
            minWs = minWs + [secMs[k][0]]

        for ind in range(0, minWs.__len__()):
            # fill the background color of all the minimums
            rowmin = minWs[ind] + 4
            cellMin = 'N$%d' % rowmin
            worksheet1.conditional_format(cellMin, {'type': 'cell',
                                                    'criteria': '==',
                                                    'value': cellMin,
                                                    'format': green})


        # Write a conditional format over a range.
        rowlenJ = 'J4:J%d' % row # SM ratio
        rowlenK = 'K4:K%d' % row # Aw ratio

        worksheet1.conditional_format(rowlenJ, {'type': 'cell',
                                              'criteria': '<',
                                              'value': 1,
                                              'format': red})
        worksheet1.conditional_format(rowlenK, {'type': 'cell',
                                              'criteria': '<',
                                              'value': 1,
                                              'format': red})
        worksheet1.conditional_format(rowlenJ, {'type': 'cell',
                                              'criteria': 'between',
                                              'minimum':  1,
                                              'maximum':  1.15,
                                              'format': yellow})

        """ Machined """
        # Write some data headers for optimization data
        TT = 'A%d:N%d' % (row+2, row+2)
        T1 = 'A%d:E%d' % (row+3, row+3)
        H1 = 'A%d' % (row + 4)
        H2 = 'B%d' % (row + 4)
        H3 = 'C%d' % (row + 4)
        H4 = 'D%d' % (row + 4)
        H5 = 'E%d' % (row + 4)
        T2 = 'F%d:G%d' % (row+3, row+3)
        H6 = 'F%d' % (row + 4)
        H7 = 'G%d' % (row + 4)
        T3 = 'H%d:I%d' % (row+3, row+3)
        H8 = 'H%d' % (row + 4)
        H9 = 'I%d' % (row + 4)
        T4 = 'J%d:N%d' % (row+3, row+3)
        H10 = 'J%d' % (row + 4)
        H11 = 'K%d' % (row + 4)
        H12 = 'L%d' % (row + 4)
        H13 = 'M%d' % (row + 4)
        H14 = 'N%d' % (row + 4)


        worksheet1.merge_range(TT, 'Machined Profiles', tabletitle)
        worksheet1.merge_range(T1, 'Input Data', tabletitle)
        worksheet1.write(H1, 'Number of Stiffeners', bold)
        worksheet1.write(H2, 'Plating Material', bold)
        worksheet1.write(H3, 'Profile Material', bold)
        worksheet1.write(H4, 'Plating Thickness (mm)', bold)
        worksheet1.write(H5, 'Profile (mm)', bold)
        worksheet1.merge_range(T2, 'Offered', tabletitle)
        worksheet1.write(H6, 'SM (cm3)', bold)
        worksheet1.write(H7, 'Aw (cm2)', bold)
        worksheet1.merge_range(T3, 'Required', tabletitle)
        worksheet1.write(H8, 'SM Min (cm3)', bold)
        worksheet1.write(H9, 'Aw Min (cm2)', bold)
        worksheet1.merge_range(T4, 'Results', tabletitle)
        worksheet1.write(H10, 'SM ratio', bold)
        worksheet1.write(H11, 'Aw Ratio', bold)
        worksheet1.write(H12, 'Stiffener Weight (kg)', bold)
        worksheet1.write(H13, 'Plating Weight (kg)', bold)
        worksheet1.write(H14, 'Total Weight (kg)', bold)

        # optimization data we want to write to the worksheet.
        inputList = objOpt.sweep[1]

        # Start from the first cell below the headers.
        row = row + 4
        col = 0

        # Iterate over the data and write it out row by row.
        for (nStiff, panMat, stiffMat, tp, profile, SM, Aw, SMMin, AwMin, SMRat,
             AwRat, platWeight, stiffWeight, totWeight) in (inputList):
            worksheet1.write(row, col,     nStiff)
            worksheet1.write(row, col + 1, panMat)
            worksheet1.write(row, col + 2, stiffMat)
            worksheet1.write(row, col + 3, tp)
            worksheet1.write(row, col + 4, profile)
            worksheet1.write(row, col + 5, SM, threeDec)
            worksheet1.write(row, col + 6, Aw, threeDec)
            worksheet1.write(row, col + 7, SMMin, threeDec)
            worksheet1.write(row, col + 8, AwMin, threeDec)
            worksheet1.write(row, col + 9, SMRat, threeDec)
            worksheet1.write(row, col + 10, AwRat, threeDec)
            worksheet1.write(row, col + 11, platWeight, twoDec)
            worksheet1.write(row, col + 12, stiffWeight, twoDec)
            worksheet1.write(row, col + 13, totWeight, twoDec)
            row += 1


        # calculate the minimum weight with a section modulus ratio > 1
        # TODO: This only checks the SM ratio, add Aw ratio later.
        secMs2 = []
        for i in range(0, objOpt.sweep[1].__len__()):
            # Gather all SMs ratios that are > 1
            if objOpt.sweep[1][i][9] > 1:
                secMs2 = secMs2 + [[i] + [objOpt.sweep[1][i][9]] + [objOpt.sweep[1][i][-1]]]
            else:
                pass

        if secMs2 != []:
            allW2 = []
            for j in range(0, secMs2.__len__()):
                # Gather all the weights from the SMs list above and find the minimum
                allW2 = allW2 + [secMs2[j][-1]]
            minw2 = min(allW2)
            indices2 = [ind for ind, val in enumerate(allW2) if val == minw2]

            minWs2 = []
            for k in indices2:
                minWs2 = minWs2 + [secMs2[k][0]]

            for ind in range(0, minWs2.__len__()):
                # fill the background color of all the minimums
                rowmin2 = minWs2[ind] + row_e + 1
                cellMin2 = 'N$%d' % rowmin2
                worksheet1.conditional_format(cellMin2, {'type': 'cell',
                                                        'criteria': '==',
                                                        'value': cellMin2,
                                                        'format': green})

        else:
            pass

        # Write a conditional format over a range.
        rowlenJ = 'J%d:J%d' % (row_e, row) # SM ratio
        rowlenK = 'K%d:K%d' % (row_e, row) # Aw ratio

        worksheet1.conditional_format(rowlenJ, {'type': 'cell',
                                              'criteria': '<',
                                              'value': 1,
                                              'format': red})
        worksheet1.conditional_format(rowlenK, {'type': 'cell',
                                              'criteria': '<',
                                              'value': 1,
                                              'format': red})
        worksheet1.conditional_format(rowlenJ, {'type': 'cell',
                                              'criteria': 'between',
                                              'minimum':  1,
                                              'maximum':  1.15,
                                              'format': yellow})

#     Create graphs, messages, spreadsheets and all calculation outputs.
#
#     Methods:
#         Add any important messages (different modes e.g. user mode, developer mode?)
#         Create graphs from e.g. the optimization or to help with other things.
#         Create graph of nomenclature using the vessel dimensions and SA.(this
#         ...is for helping the user to assign nomenclature to each member but
#         ...also to get a good overview of the initial SA.)
#
#     Output:
#         Spreadsheets
#         Messages
#         Graphs


class Designer:
    """ User interface, recieves inputs from multiple classes and calls relevant
        functions for each structural member. All the high level logic of the
        code is contained here.

        Attributes:
            ...__init__...
            Objective:
                Inits the Designer objects.
            Input:
                -
            Output:
                self

            ...create_section...
            Objective:
                Create a section between two frames and two girder, consisting of
                panels and stiffeners and then assigns it to a Strake object.
            Input:
                objStrak: Strake object
                secName: Section name (string)
                sGird: Girder spacing (float, mm) 
                sFram: Frame spacing (float, mm)
                xPosGlob: Longitudinal postion of the midpoint of the strake (float, m)
                yPosGlob: Horizontal postsion of the migpoint of the strake (float, m)
                zPosGlob: Transversal postsion of the migpoint of the strake (float, m)
                location: location according to ISO rules e.g. bottom. (string)
            Output:
                Section.Input
                objStrak.sections[i].Input

            ...create_section_topology...
            Objective:
                Create the topology for a section using the number of stiffeners
                and the section properties. Inits panel and stiffener objects and
                assigns them to the structure object.
            Input:
                objSect: Section object
                objStruct: Structure object
                nStiff: Number of stiffeners on one section (int, -)
            Output:
                panWidth: Panel width(b) (float, mm)
                panYPos: y-coordinate for a panel with respect to the
                         sections girder spacing from zero. (float, mm)
                panZPos: z-coordinate for a panel with respect to the keel (float, mm)
                stiffYPos: y-coordinate for a stiffener with respect to the
                           sections girder spacing from zero. (float, mm)
                stiffZPos: z-coordinate for a stiffener with respect to the keel (float, mm)
                sStiff: Spacing/Distance between two stiffeners (float, mm)
                objSect.nStiff: Number of stiffeners get assigned to Section object (int)

                objPan: Panel object
                objStruct.Panel[i]: Panel objects assigned to structure object
                objStiff: Stiffener object
                objStruct.Stiffener[i]: Stiffener objects assigned to structure object

            ...calc_pressure_factors...
            Objective:
                Loops through all structural members and calculates the pressure
                factors.
            Input:
                objRule: Rules child object. The rules that will be used for requirements.
                objStruct: Structure object from the Structure class.
                objVess: Vessel object from the Vessel class.
            Output:
                objStruct.Panel[i].'pressure factors'
                objStruct.Stiffener[i].'pressure factors'
                [ruleType, kDC, kL, kAR_d, kAR_p, kZ]

            ...calc_design_pressures...
            Objective:
                Loops through all structural members and calculates the design
                pressures.
            Input:
                [objRule, objStruct, objVess]
            Output:
                objStruct.Panel[i].pMax: Maximum/Design pressure (float, kN/m2)
                objStruct.Stiffener[i].pMax: Maximum/Design pressure (float, kN/m2)
                [ruleType, pMax]

            ...calc_scantling_req...
            Objective:
                Loops through all structural members and calculates the scantling
                requirements.
            Input:
                [objRule, objStruct, objVess]
            Output:
                objStruct.Panel[i].'scantling requirements'
                [ruleType, k2, k3, FShear, MBend, tReq, tMin]
                objStruct.Stiffener[i].'scantling requirements'
                [ruleType, AwMin, SMMin]
                
            ...calc_stiff_max_prop...
            Objective:
                Calculates and checks so that the stiffener profile does not exceed
                the recommended dimensional proportion, in order to reduce risk
                of buckling.
            Input:
                objStress: StreesCalculator object
                objStruct: Structure object
                objRule: Rule object

            ...assign_material_to_all_panels...
            Objective:
                Assigns the same material object to all panels.
            Input:
                objStruct
                objMat: Material object from the MaterialsLibrary class
            Output:
                objStruct.Panel[i].Material
                See more information in the MaterialsLibary class.

            ...assign_material_to_all_stiffeners...
            Objective:
                Assigns the same material object to all stiffeners.
            Input:
                objStruct
                objMat: Material object from the MaterialsLibrary class
            Output:
                objStruct.Stiffener[i].Material
                See more information in the MaterialsLibary class.

            ...assign_recommended_plates...
            Objective:
                Assigns the recommended Plating object to all Panel objects.
                It collects all the available thicknesses and put them in a list.
                For each panel it will find the position in the list of the closest
                required thickness rounded up. It will then find the plating
                object that has the same thickness as the one found in the list and
                assign it to the panel. If there is there is not plate with the
                required thickness an error will occur and the largest/thickest
                plate will be assigned.
            Input:
                objStruct
                objPlaLib: Plating library from the PlatingLibrary class
            Output:
                objStruct.Panel[i].Plate
                See more information in the Plates and PlatingLibrary class.
    """
    def __init__(self):
        """ Inits the Designer objects. """
        pass

    def create_section(self, objStrak, secName, sGird, sFram, xPosGlob, 
                       yPosGlob, zPosGlob, location):
        """ Create a section between two frames and two girder, consisting of
            panels and stiffeners.
        """
        section = Section(objStrak, secName, sGird, sFram, xPosGlob, 
                          yPosGlob, zPosGlob, location)
        
        objStrak.assign_section(section)
        pass

    def create_section_topology(self, objSect, objStruct, nStiff):
        """ Create the topology for a section using the number of stiffeners
            and the section properties. Inits panel and stiffener objects and
            assigns them to the structure object.
        """
        
        secName = objSect.secName 
        sGird = objSect.sGird
        sFram = objSect.sFram
        xPosGlob = objSect.xPosGlob
        yPosGlob = objSect.yPosGlob
        zPosGlob = objSect.zPosGlob
        location = objSect.location

        objSect.nStiff = nStiff
        panWidth = []
        panYPos = []
        panZPos = []
        """ Create equally spaced stiffener coordinates using a horizontal plane. """
        if location in ('bottom', 'deck', 'superstructure top'):
            # create local coordinates
            stiffYPos = numpy.linspace(0, sGird, nStiff+2)
            for i in range(0, nStiff+1):
                sStiff = stiffYPos[i+1] - stiffYPos[i]
                panWidth = panWidth + [stiffYPos[i+1] - stiffYPos[i]]
                panYPos = panYPos + [stiffYPos[i+1] - panWidth[i]/2]
            # create panel objects
            for i in range(0, panYPos.__len__()):
                Pan = (Panel(panWidth[i], 
                             sFram,
                             xPosGlob, 
                             (yPosGlob - (sGird/2)*1e-3 + panYPos[i]*1e-3), 
                             zPosGlob, 
                             location,
                             secName)
                       )
                objStruct.assign_panel(Pan)
            # create stiffener objects
            for i in range(0, stiffYPos.__len__()-2):
                Stiff = (Stiffener(sFram, 
                                   xPosGlob, 
                                   (yPosGlob - (sGird/2)*1e-3 + stiffYPos[i+1]*1e-3), 
                                   zPosGlob, 
                                   sStiff, 
                                   location, 
                                   'longitudinal',
                                   secName)
                         )
                objStruct.assign_stiffener(Stiff)
                
            """ Create equally spaced stiffener coordinates using a vertical plane. """
        elif location in ('side', 'bottom&side', 'superstructure'):
            # create local coordinates
            stiffZPos = numpy.linspace(0, sGird, nStiff+2)
            for i in range(0, nStiff+1):
                sStiff = stiffZPos[i+1] - stiffZPos[i]
                panWidth = panWidth + [stiffZPos[i+1] - stiffZPos[i]]
                panZPos = panZPos + [stiffZPos[i+1] - panWidth[i]/2]
            # create panel objects
            for i in range(0, panZPos.__len__()):
                Pan = (Panel(panWidth[i], 
                             sFram,
                             xPosGlob, 
                             yPosGlob, 
                             (zPosGlob - (sGird/2)*1e-3 + panZPos[i]*1e-3), 
                             location,
                             secName)
                       )
                objStruct.assign_panel(Pan)
            # create stiffener objects
            for i in range(0, stiffZPos.__len__()-2):
                Stiff = (Stiffener(sFram, 
                                   xPosGlob, 
                                   yPosGlob, 
                                   (zPosGlob - (sGird/2)*1e-3 + stiffZPos[i+1]*1e-3), 
                                   sStiff, 
                                   location, 
                                   'longitudinal',
                                   secName)
                         )
                objStruct.assign_stiffener(Stiff)
                
        nrpan = objStruct.Panel.__len__()
        nrstiff = objStruct.Stiffener.__len__()
        print('%d panels and %d stiffeners have been created' % (nrpan, nrstiff))
        pass


    def calc_pressure_factors(self, objRule, objStruct, objVess):
        """ Loops through all structural members and calculates the pressure
            factors.
        """
        VessData = objRule.get_vessel_data(objVess)
        inVessData = VessData[:5]+[VessData[-1]]

        GlobVar = objRule.calc_global_var(inVessData)

        objStruct.assign_global_var(GlobVar)

        for i in range(0, objStruct.Panel.__len__()):
            """ Panel pressure factors """
            PanData = objRule.measure_panel(objStruct.Panel[i])

            InData = (PanData + [objStruct.mLDC] + [objStruct.nCG] + [VessData[0]]
                      + VessData[5:8]
                      )

            PressFac = objRule.calc_panel_pressure_factors(InData)

            objStruct.Panel[i].assign_press_factors(PressFac)
            print("Panel %d pressure factors calculated" % i)

        for i in range(0,objStruct.Stiffener.__len__()):
            """ Stiffener pressure factors """
            StiffData = objRule.measure_stiffener(objStruct.Stiffener[i])

            InData = (StiffData + [objStruct.mLDC] + [objStruct.nCG] + [VessData[0]]
                      + VessData[5:8]
                      )

            PressFac = objRule.calc_stiff_pressure_factors(InData)

            objStruct.Stiffener[i].assign_press_factors(PressFac)
            print("Stiffener %d pressure factors calculated" % i)
        pass



    def calc_design_pressures(self, objRule, objStruct, objVess):
        """ Loops through all structural members and calculates the design
            pressures.
        """
        VessData = objRule.get_vessel_data(objVess)

        for i in range(0, objStruct.Panel.__len__()):
            """ Panel design pressures """
            PressFact = objRule.get_press_factors(objStruct, objStruct.Panel[i])

            PanData = objRule.measure_panel(objStruct.Panel[i])

            InData = (PressFact + [PanData[4]] + [objStruct.nCG] + VessData[:2]
                      + [objStruct.mLDC]
                      )

            DesPress = objRule.calc_panel_pressures(InData)

            objStruct.Panel[i].assign_design_pressure(DesPress)
            print("Panel %d design pressure calculated" % i)

        for i in range(0, objStruct.Stiffener.__len__()):
            """ Stiffener design pressures """
            PressFact = objRule.get_press_factors(objStruct, objStruct.Stiffener[i])

            StiffData = objRule.measure_stiffener(objStruct.Stiffener[i])

            InData = (PressFact + [StiffData[4]] + [objStruct.nCG] + VessData[:2]
                      + [objStruct.mLDC]
                      )

            DesPress = objRule.calc_stiffener_pressures(InData)

            objStruct.Stiffener[i].assign_design_pressure(DesPress)
            print("Stiffener %d design pressure calculated" % i)
        pass

    def calc_scantling_req(self, objRule, objStruct, objVess):
        """ Loops through all structural members and calculates the scantling
            requirements.
        """
        VessData = objRule.get_vessel_data(objVess)

        for i in range(0, objStruct.Panel.__len__()):
            """ Panel requirements """
            DesPress = objRule.get_design_pressures(objStruct.Panel[i])

            PanData = objRule.measure_panel(objStruct.Panel[i])

            InData = (DesPress + PanData[:2] + [PanData[4]] + [objStruct.mLDC] +
                      [VessData[4]] +
                      [objStruct.Panel[i].Material.tensileStrength] +
                      [objStruct.Panel[i].Material.yieldStrength] +
                      [objStruct.Panel[i].Material.yieldStrength] ###
                      )
            ### TODO: welded and non-welded should be used but that data does not exist yet.


            PanReq = objRule.calc_panel_req(InData)

            objStruct.Panel[i].assign_scantling_req(PanReq)
            print("Panel %d requirements calculated" % i)

        for i in range(0, objStruct.Stiffener.__len__()):
            """ Stiffener requirements """
            DesPress = objRule.get_design_pressures(objStruct.Stiffener[i])

            StiffData = objRule.measure_stiffener(objStruct.Stiffener[i])

            InData = (DesPress + [StiffData[0]] + [StiffData[3]] +
                      [objStruct.Stiffener[i].Material.yieldStrength]
                      )

            StiffReq = objRule.calc_stiff_req(InData)

            objStruct.Stiffener[i].assign_scantling_req(StiffReq)
            print("Stiffener %d requirements calculated" % i)
        pass
    
    def calc_stiff_max_prop(self, objStress, objStruct, objRule):
        """ Calculates and checks so that the stiffener profiles do not exceed
            the recommended dimensional proportions, in order to reduce risk
            of buckling. 
        """
        for i in range(0, objStruct.Stiffener.__len__()):
            stress = objStress.calc_stiff_stress(objStruct.Stiffener[i], objStruct)
            
            inData = ([i] 
                      + [objStruct.Stiffener[i].Material.yieldStrength]
                      + [objStruct.Stiffener[i].Profile.Aw]
                      + [objStruct.Stiffener[i].AwMin]
                      + [stress]
                      + [objStruct.Stiffener[i].Profile.pType]
                      + [objStruct.Stiffener[i].Profile.hw]
                      + [objStruct.Stiffener[i].Profile.tw]
                      + [objStruct.Stiffener[i].Profile.wf]
                      + [objStruct.Stiffener[i].Profile.tf]
                      )
            
            objRule.check_stiff_prop(inData)
        pass

    def assign_material_to_all_panels(self, objStruct, objMat):
        """ Assigns the same material object to all panels. """
        for i in range(0, objStruct.Panel.__len__()):
            objStruct.Panel[i].assign_material(objMat)
        pass

    def assign_material_to_all_stiffeners(self, objStruct, objMat):
        """ Assigns the same material object to all stiffeners. """
        for i in range(0, objStruct.Stiffener.__len__()):
            objStruct.Stiffener[i].assign_material(objMat)
        pass

    def assign_recommended_plates(self, objStruct, objPlaLib):
        """ Assigns the recommended Plating object to all Panel objects.
            It collects all the available thicknesses and put them in a list.
            For each panel it will find the position in the list of the closest
            required thickness rounded up. It will then find the plating
            object that has the same thickness as the one found in the list and
            assign it to the panel. If there is there is not plate with the
            required thickness an error will occur and the largest/thickest
            plate will be assigned.
        """
        for i in range(0, objStruct.Panel.__len__()):
            minTP = max(objStruct.Panel[i].tReq, objStruct.Panel[i].tMin)
            allTP = objPlaLib.list_all_thicknesses()
            pos = bisect_left(allTP, minTP)

            try:
                InData = next((x for x in objPlaLib.Plates if x.tp == allTP[pos]), None)
            except:
                print("""ERROR: There is no plate with the required thickness,
       largest availaible has been assigned""")
                InData = objPlaLib.Plates[-1]

            objStruct.Panel[i].assign_plate(InData)
        pass

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

        Attributes:

            ...check_inputs...
            Objective:
                Check if variables are valid or missing for calculations of
                certain methods. This method is meant to be called from inside
                other methods, wherever a variable check is required.
            Input:
                function: Which method/function is being checked for inputs (string)
                inputVec: Which variable is being checked.
            Output:
                returns value if valid otherwise rutern valid value after user input.
    """
    def __init__(self):
        pass

    def check_inputs(self, function, inputVec):
        """ Check inputs for typos, other errors etc. """
        if function == 'ISOinit':
            """ Checks the ISO12215 __init__ function. """
            designCategory = inputVec
            while True:
                    if designCategory in ('A', 'B', 'C', 'D'):
                        return designCategory
                    else:
                        designCategory = input('Not a valid design category, choose A, B, C or D >>> ')
                        return designCategory
        elif function == 'calc_global_var':
            """Checks the ISO12215 calc_global_var function. """
            objVess = inputVec
            if not hasattr(objVess, 'craftMode'):
                print("Error: calculate or choose craft mode; planing or displacement")
                while True:
                    craftMode_ = input('1 = planing, 2 = disp, 3 = calculate >>> ')
                    if craftMode_ in ('1', '2', '3'):
                        break
                    else:
                        print('Not a valid number')
                if craftMode_ == '3':
                    objVess.craftMode = objVess.calc_craft_mode()
                else:
                    objVess.craftMode = int(craftMode_)
            print("craftMode = ", objVess.craftMode)
        pass


class Optimizer:
    """ User chooses between different optimization methods depending on what
        type of structural member needs to be optimized.

        Attributes:

            ...__init__...
            Objective:
                Inits the Optimizer object
            Input:
                -
            Output:
                self

            ...objective_function...
            Objective:
                Calculates the objective function of the optimization.
                Currently only covers the total weight.
            Input:
                objStruct: Structure object
            Output:
                weight: total weight of the entire structure (float, kg)

            ...sweep_method...
            Objective:
                Loops through choosen set of number of stiffeners, creates the
                topology for a chosen section and structure child objects and
                calculates the rules. It then assigns the recommended plating 
                and loops through a list of user-specified profiles from 
                extrusions and machined.
            Input:
                objVess: Vessel object for calculating requirements
                objStruct: Structure object for panel and stiffener objects
                objRule: Rules child object
                objDes: Designer object for creating topology
                objPlaLib: PlatingLibrary object for plate assignment
                minNrStiff: Minimum number of stiffeners for the section (int)
                maxNrStiff: Maximum number of stiffeners for the section (int)
                panMat: List of material objects to be assigned to the panels
                stiffMat: List of material objects to be assigned to the stiffeners
                extrusions: List of Extrusion objects to be assigned to the
                            stiffeners
                machined: List of Machined objects to be assigned to the
                          stiffeners
            Output:
                self[0]
                    extrWeights[0:n]:
                       [0]: Number of stiffeners (int)
                       [1]: Panel material (string)
                       [2]: Stiffener material (string)
                       [3]: Plating thickness (float, mm)
                       [4]: Extruded profile (string)
                       [5]: Profile section modulus (float, cm3)
                       [6]: Profile web area (float, cm2)
                       [7]: Required stiffener section modulus (float, cm3)
                       [8]: Required stiffener web area (float, cm2)
                       [9]: Offered vs required section modulus ratio (float, -)
                       [10]: Offered vs required web area ratio (float, -)
                       [11]: Total weight for stiffeners (float, kg)
                       [12]: Total weight for panels (float, kg) ,
                       [13]: Total weight for entire section (float, kg)
                self[1]:
                    machWeights[0:n]:
                       [0]: Number of stiffeners (int)
                       [1]: Panel material (string)
                       [2]: Stiffener material (string)
                       [3]: Plating thickness (float, mm)
                       [4]: Machined profile (string)
                       [5]: Profile section modulus (float, cm3)
                       [6]: Profile web area (float, cm2)
                       [7]: Required stiffener section modulus (float, cm3)
                       [8]: Required stiffener web area (float, cm2)
                       [9]: Offered vs required section modulus ratio (float, -)
                       [10]: Offered vs required web area ratio (float, -)
                       [11]: Total weight for stiffeners (float, kg)
                       [12]: Total weight for panels (float, kg) ,
                       [13]: Total weight for entire section (float, kg)

            ...assign_sweep...
            Objective:
                assign sweep to Optimizer object
            Input:
                objSweep: Sweep method object
            Output:
                self.input

    """
    def __init__(self):
        """ Inits the Optimizer object """
        pass

    def objective_function(self, objStruct):
        """ Calls a weight calculator and returns the value """
        objStruct.calc_total_weight()
        weight = objStruct.weight
        return weight

    def constraints(self, objStruct):
        pass

    def sweep_method(self, objVess, objStruct, objRule, objDes, objPlaLib,
                     objStress, minNrStiff, maxNrStiff, panMat, stiffMat, 
                     extrusions, machined, strakeListID, secListID):
        """ Loops through choosen set of number of stiffeners, creates the
            topology, structure child objects and calculates the rules. It then
            assigns the recommended plating and loops through a list of
            user-specified profiles from either extrusions or machined or both.
        """
        
        extrWeights = [] # total weight using extrusions
        machWeights = [] # total weight using machined profiles
        for i in range(minNrStiff, maxNrStiff+1):
            objStruct.Panel = []
            objStruct.Stiffener = []
            objDes.create_section_topology(objStruct.Strake[strakeListID].sections[secListID],
                                           objStruct, 
                                           i
                                           )

            for pm in panMat:
                objDes.assign_material_to_all_panels(objStruct, pm)
                for sm in stiffMat:
                    objDes.assign_material_to_all_stiffeners(objStruct, sm)

                    objDes.calc_pressure_factors(objRule, objStruct, objVess)
                    objDes.calc_design_pressures(objRule, objStruct, objVess)
                    objDes.calc_scantling_req(objRule, objStruct, objVess)
                    objDes.assign_recommended_plates(objStruct, objPlaLib)

                    # TODO: give user option to assign a specific plate to all panels.
                        # objStruct.Panel[i].assign_plate(LB.mAL5)

                    panWeight = []
                    for p in range(0, objStruct.Panel.__len__()):
                        objStruct.Panel[p].calc_weight()
                        panWeight = panWeight + [objStruct.Panel[p].weight]
                    panWeight = sum(panWeight)

                    if i != 0: # if the numbers of stiffeners is not zero.
                        
                        for profiles in extrusions:

                            stiffWeight = []
                            for j in range(0, objStruct.Stiffener.__len__()):
                                objStruct.Stiffener[j].assign_profile(profiles)
                                objStruct.Stiffener[j].calc_weight()
                                stiffWeight = stiffWeight + [objStruct.Stiffener[j].weight]
                            stiffWeight = sum(stiffWeight)
                            
                            objDes.calc_stiff_max_prop(objStress, objStruct, objRule)
                            # TODO: add pass and fail to report
                            
                            ratSM = []
                            ratAw = []
                            for a in range(0, objStruct.Stiffener.__len__()):
                                ratSM = [profiles.SM/objStruct.Stiffener[a].SMMin]
                                ratAw = [profiles.Aw/objStruct.Stiffener[a].AwMin]
                            ratSM = min(ratSM)
                            ratAw = min(ratAw)

                            weightEProf = [i,
                                           objStruct.Panel[0].Material.matLabel,
                                           objStruct.Stiffener[0].Material.matLabel,
                                           objStruct.Panel[0].Plate.tp,
                                           profiles.profLabel, profiles.SM, profiles.Aw,
                                           objStruct.Stiffener[0].SMMin,
                                           objStruct.Stiffener[0].AwMin,
                                           ratSM, ratAw,
                                           stiffWeight, panWeight,
                                           self.objective_function(objStruct)]

                            extrWeights = extrWeights + [weightEProf]

                        for profiles in machined:

                            stiffWeight = []
                            for k in range(0, objStruct.Stiffener.__len__()):
                                objStruct.Stiffener[k].assign_profile(profiles)
                                objStruct.Stiffener[k].calc_weight()
                                stiffWeight = stiffWeight + [objStruct.Stiffener[k].weight]
                            stiffWeight = sum(stiffWeight)
                            
                            objDes.calc_stiff_max_prop(objStress, objStruct, objRule)
                            # TODO: add pass and fail to report

                            ratSM = profiles.SM/objStruct.Stiffener[0].SMMin
                            ratAw = profiles.Aw/objStruct.Stiffener[0].AwMin

                            weightMProf = [i,
                                           objStruct.Panel[0].Material.matLabel,
                                           objStruct.Stiffener[0].Material.matLabel,
                                           objStruct.Panel[0].Plate.tp,
                                           profiles.profLabel, profiles.SM, profiles.Aw,
                                           objStruct.Stiffener[0].SMMin,
                                           objStruct.Stiffener[0].AwMin,
                                           ratSM, ratAw,
                                           stiffWeight, panWeight,
                                           self.objective_function(objStruct)]
                            machWeights = machWeights + [weightMProf]
                            
                    else: # if there are no stiffeners
                        weightPan = [i, objStruct.Panel[0].Material.matLabel,
                                     '-',
                                     objStruct.Panel[0].Plate.tp,
                                     'None',0,0,0,0,0,0,0,
                                     panWeight,
                                     self.objective_function(objStruct)]
                        extrWeights = extrWeights + [weightPan]
                        machWeights= machWeights + [weightPan]

        return (extrWeights, machWeights)


    def assign_sweep(self, objSweep):
        """ Assigns a optimization object as attribute to self (opti object). """
        self.sweep = objSweep
        pass

class StressCalculator:
    """ Calculates the stress of different components, currently only for
        stiffeners using regular beam theory.
        
        Attributes:
            
            ...__init__...
            Objective:
                Inits the stress calculator object
            Input:
                -
            Output:
                self
                
            ...calc_stiff_stress...
            Objective:
                Calculates the maximum stress of a stiffener assuming it is 
                simply supported and subjected to bending around the x-axis
                with a distributed load from the design pressure. The plating 
                attached to the stiffener is also taken into consideration, 
                assuming that the plate thickness is the same for all plates
                within a section (which is not true at the moment when using
                                  assign_recommended_plates.)
            Input:
                objStiff: Stiffener object
                objStruct: Structure object
            Output:
                sigmaActStiff: Maximum stress of stiffener (float, N/mm2)
    
    """
    def __init__(self):
        """ Intits the StressCalculator object """
        pass

    def calc_stiff_stress(self, objStiff, objStruct):
        """ calculates the maximum stress of a stiffener from bending around the x-axis."""
        tw = objStiff.Profile.tw
        hw = objStiff.Profile.hw
        tf = objStiff.Profile.tf
        wf = objStiff.Profile.wf
        Atot = objStiff.Profile.Atot
        
        # Get thickness from attached plate assuming the same thickness for all
        # plates within a section.
        for i in range(0, objStruct.Panel.__len__()):
            if objStiff.section == objStruct.Panel[i].section:
                tp = objStruct.Panel[i].Plate.tp
            else:
                pass
        
        # Effective plating b_e, section 11.6.
        be = 60*tp
        if be > objStiff.sStiff:
            be = objStiff.sStiff
        else:
            be = be
            
        # Each part (web, flange, plate) is divided and calculated seperately
        # then they are put together in the end.
        if objStiff.Profile.pType == 'Flat Bar':
            # plate
            A1 = be*tp
            y1 = tp/2
            I1 = (be*tp**3)/12
            # web
            A2 = tw*hw
            y2 = tp + hw/2
            I2 = (tw*hw**3)/12
            # centroid
            Atot = A1 + A2
            ycog = (A1*y1 + A2*y2) / Atot
            # inertia
            Ixx = (I1+A1*(ycog-y1)**2 + I2+A2*(y2-ycog)**2)
        elif objStiff.Profile.pType == 'L-shaped':
            # plate
            A1 = be*tp
            y1 = tp/2
            I1 = (be*tp**3)/12
            # web
            A2 = tw*hw
            y2 = tp + hw/2
            I2 =  (tw*hw**3)/12
            # flange
            A3 = wf*tf
            y3 = tp+hw+tf/2
            I3 = (wf*tf**3)/12
            # centroid
            Atot = A1 + A2 + A3
            ycog = (A1*y1 + A2*y2 + A3*y3) / Atot
            # intertia
            Ixx = (I1+A1*(ycog-y1)**2 + I2+A2*(y2-ycog)**2 + I3+A3*(y3-ycog)**2)
        elif objStiff.Profile.pType == 'T-shaped':
            # plate
            A1 = be*tp
            y1 = tp/2
            I1 = (be*tp**3)/12
            # web
            A2 = tw*hw
            y2 = tp + hw/2
            I2 =  (tw*hw**3)/12
            # flange
            A3 = wf*tf
            y3 = tp+hw+tf/2
            I3 = (wf*tf**3)/12
            # centroid
            Atot = A1 + A2 + A3
            ycog = (A1*y1 + A2*y2 + A3*y3) / Atot
            # intertia
            Ixx = (I1+A1*(ycog-y1)**2 + I2+A2*(y2-ycog)**2 + I3+A3*(y3-ycog)**2)
        
        # Distributed load converted from area to line
        q = objStiff.pMax*1e-6 * objStiff.sStiff # N/mm
        
        # Maximum bending moment assuming simply supported beams
        MMax = (q * objStiff.lStiff**2) / 8 # Nmm
        
        # Maximum distance from CoG (mm)
        if (hw + tp) > (hw + tf):
            zMax = hw + tp
        else:
            zMax = hw + tf
        
        # Actual stress
        sigmaActStiff = MMax * zMax / Ixx # N/mm2
        
        return sigmaActStiff
