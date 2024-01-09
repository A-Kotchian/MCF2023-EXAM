# MCF2023-EXAM
Welcome in the repository of MCF2023-EXAM of Alessandro Kotchian.
The purpose of this program is to simulate the High Altitude Atmospheric Shower with methods learned during lessons.

**REQUIREMENTS**:  
You need _Python_ with this libraries:


1. _Matplotlib_
2. _Numpy_
3. _Scipy_

**HOW TO USE IT**
Run the script _"Rossi simulation.py"_ in the terminal.

The program starts asking the user to insert:
- Starting Energy of a photon at 20km of altitude
- The step of advancement in terms of X_0. The value must be between 0 and 1.

Then the program starts asking if the user wants to see graph of statistical analyses for 50000 generated photons in range 1-100 TeV: 

If the users wants to see the graph, he needs to insert "_1_" else "_0_".

At final the program will show the mean of the simulation for all 3 different angles.


**HELP** :   
If you don't have any libraries follow this:

- Open the terminal 
- insert "_cd_ _<path\folder\of\directory>_"
- insert "_make_"
- done!

or

- Open the terminal in the "MCF2023-EXAM folder"
- insert "_pip_ _install_ _-r_ _requirements.txt_"
- done!

N.B: If you have linux and new version of Python maybe it's usefull to use:
- "_pip_ _install_ _-r_ _requirements.txt_ _--break-system-packages_"
