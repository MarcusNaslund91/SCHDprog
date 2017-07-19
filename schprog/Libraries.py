#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 15:00:22 2017

@author: Marcus Naslund
"""
import schprog as SP

""" LIBRARIES: Profiles, Plates and Materials """

""" PROFILES """
mProfLib = SP.ProfileLibrary()
# (profLabel, SM, Aw, tw, hw, tf, fw, pType)
mFlatBar40x5 = SP.Extrusions('Flat Bar 40 x 5', 1.333, 2.000, 5.0, 40, 0, 0, 'Flat Bar')
mFlatBar40x6 = SP.Extrusions('Flat Bar 40 x 6', 1.600, 2.400, 6.0, 40, 0, 0, 'Flat Bar')
mFlatBar50x6 = SP.Extrusions('Flat Bar 50 x 6', 2.500, 3.000, 6.0, 50, 0, 0, 'Flat Bar')
mFlatBar60x5 = SP.Extrusions('Flat Bar 60 x 5', 6.179, 3.000, 5.0, 60, 0, 0, 'Flat Bar')
mFlatBar80x6 = SP.Extrusions('Flat Bar 80 x 6', 6.400, 4.800, 6.0, 80, 0, 0, 'Flat Bar')

mAngle50x50x6 = SP.Extrusions('Angle 50 x 50 x 6'          , 8.928, 3.000, 6.0, 50, 6.0, 50.0, 'L-shaped')
mTee38_1x38_1x4_76 = SP.Extrusions('Tee 38.1 x 38.1 x 4.76', 2.148, 1.814, 4.76, 38.1, 4.76, 38.1, 'T-shaped')
mTee40x40x4 = SP.Extrusions('Tee 40 x 40 x 4'              , 1.944, 1.600, 4.0, 40.0, 4.0, 40.0, 'T-shaped')
mTee50x50x4 = SP.Extrusions('Tee 50 x 50 x 4'              , 2.983, 2.000, 4.0, 50.0, 4.0, 50.0, 'T-shaped')
mTee50_8x50_8x6_3 = SP.Extrusions('Tee 50.8 x 50.8 x 6.3'  , 5.049, 3.200, 6.3, 50.8, 6.3, 50.8, 'T-shaped')

mProfLib.assign_extrusion(mFlatBar40x5)
mProfLib.assign_extrusion(mFlatBar40x6)
mProfLib.assign_extrusion(mFlatBar50x6)
mProfLib.assign_extrusion(mFlatBar60x5)
mProfLib.assign_extrusion(mFlatBar80x6)
mProfLib.assign_extrusion(mAngle50x50x6)
mProfLib.assign_extrusion(mTee38_1x38_1x4_76)
mProfLib.assign_extrusion(mTee40x40x4)
mProfLib.assign_extrusion(mTee50x50x4)
mProfLib.assign_extrusion(mTee50_8x50_8x6_3)


""" PLATES """
""" create plates """
mPlaLib = SP.PlatingLibrary()
# (label, tp) 
mAL3 = SP.Plates('AL3', 3)
mAL4 = SP.Plates('AL4', 4)
mAL5 = SP.Plates('AL5', 5)
mAL6 = SP.Plates('AL6', 6)
mAL8 = SP.Plates('AL8', 8)
mAL10 = SP.Plates('AL10', 10)
mAL12 = SP.Plates('AL12', 12)
mAL15 = SP.Plates('AL15', 15)
mAL18 = SP.Plates('AL18', 18)
mAL20 = SP.Plates('AL20', 20)
mAL22 = SP.Plates('AL22', 22)
mAL25 = SP.Plates('AL25', 25)
mAL30 = SP.Plates('AL30', 30)

mPlaLib.assign_plate(mAL3)
mPlaLib.assign_plate(mAL4)
mPlaLib.assign_plate(mAL5)
mPlaLib.assign_plate(mAL6)
mPlaLib.assign_plate(mAL8)
mPlaLib.assign_plate(mAL10)
mPlaLib.assign_plate(mAL12)
mPlaLib.assign_plate(mAL15)
mPlaLib.assign_plate(mAL18)
mPlaLib.assign_plate(mAL20)
mPlaLib.assign_plate(mAL22)
mPlaLib.assign_plate(mAL25)
mPlaLib.assign_plate(mAL30)


""" MATERIALS """
# (matLabel, yieldStrength, tensileStrength, elasticModulus, shearModulus, density)
mAL_5083_O = SP.MaterialsLibrary('AL_5083_O'    , 125, 270, 7000, 2600, 2720)
mAL_5083_H32 = SP.MaterialsLibrary('AL_5083_H32', 250, 320, 7000, 2600, 2660)
mAL_5251_O = SP.MaterialsLibrary('AL_5251_O'    , 80, 180, 7000, 2600, 2690)
mAL_5251_H22 = SP.MaterialsLibrary('AL_5251_H22', 165, 210, 7000, 2600, 2690)
mAL_5251_H24 = SP.MaterialsLibrary('AL_5251_H24', 190, 230, 7000, 2600, 2690)
mAL_5251_H26 = SP.MaterialsLibrary('AL_5251_H26', 215, 255, 7000, 2600, 2690)

mAL_6061_T6 = SP.MaterialsLibrary('AL_6061_T6'          , 276, 310, 6890, 2600, 2700)
mAL_6082_T4 = SP.MaterialsLibrary('AL_6082_T4'          , 110, 205, 7000, 2692, 2700)
mAL_6082_T6_5 = SP.MaterialsLibrary('AL_6082_T6_<5'     , 250, 290, 7000, 2692, 2700)
mAL_6082_T6_5_25 = SP.MaterialsLibrary('AL_6082_T6_>5'  , 260, 310, 7000, 2692, 2700)
mAL_6106_T6 = SP.MaterialsLibrary('AL_6106_T6'          , 200, 250, 7000, 2692, 2700)