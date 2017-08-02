# Current Status
Most of these files come from the PyScaffold and they are not edited, I have to learn how they work first.
The only files I am working on currently is SCHDprog/schprog/schprog.py, Libraries.py and MarcusPrototype.py.

__You need all of the files inside SCHDprog/schprog/, except \_\_init\_\_ for the program to work!

The program can create a stiffened panel located at the bottom or side between two girders and two frames. The stiffeners are longitudinals and equally spaced. It calculates a limited scope of the ISO rules for panels, e.g. required thickness and for stiffeners e.g. the minimum section modulus and web area. It has a materials library, plating library and a profile library with extrusions. It produces an excel report containing scantlings and requirements, used profiles, topology metadata input ad structural weight. 

It can perform a simple optimization by letting the user choose a range of number of stiffeners and a set of extruded and machined profiles. The user can also choose a set of materials for both plates and profiles.
