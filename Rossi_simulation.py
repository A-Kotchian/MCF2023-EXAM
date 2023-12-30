import numpy as np 
from scipy import optimize
import matplotlib.pyplot as plt


#######################################################################################
#
#Constants
#        
#######################################################################################
h_in=2*10**(4)                          #m      #Particles starting Altidude at t=0
h_det=4*10**(3)                         #m      #Detector Altidude
X_0=700                                 #m      #radiation length of particle at 20km of altitude
deep=h_in-h_det                         #m      #depth of material
m_e=9,109*10**(-31)                     #kg     #mass of electron
c=299792458                             #m/s    #speed of light
kappa= 1.6396891*10**(-13)              #kgm/s  #kappa=2*m_e*c**2
t=deep/X_0                              #number of radiation length/depth of material
Critical_energy_e=87.92                 #MeV    #Critical energy of electrons
Critical_energy_p=85.97                 #MeV    #Critical energy of positrons
#######################################################################################
#
#Functions
#        
#######################################################################################

def deriv_energy(E_0, X_0, step):
    """
    Calculate the energy deriv_energyation of a particle swarm.

    This function computes the energy deriv_energyation of a particle swarm
    based on the starting energy, radiation length, and the step of advancement.

    Parameters:
    - E_0 (float): The starting energy of the particle swarm (MeV).
    - X_0 (float): The radiation length of the particle (m).
    - step (float): The step of advancement in terms of X_0. The value must be between 0 and 1.

    Returns:
    - float: The deriv_energyed energy value.
    """
    return ((E_0 / X_0)* step)/np.e

def simulate(s, d ,Particles):
    """
    Simulate the behavior of particles with given energy and altitude.

    Parameters:
    -s (float): The step size.
    -deep (int): The depth.
    -Particles (class): The class representing the particles.

    """

    particle_Energy = Particles.particles[0]['Energy']
    step = 0
    stop_while = 0
    while particle_Energy > 0:

        step +=1
        new_particles = []
        N_electrons = 0 
        N_photons = 0 
        N_positrons = 0 

        for p in Particles.particles:
            type = p['Type']
            particle_Energy = p['Energy']
            altitude=h_in-s*(d)*step        #Altiude of the particle
            
            if type == 'Electron':
                if particle_Energy > deriv_energy(starting_energy, X_0, s) and altitude> h_det:
                    Energy_after_process = particle_Energy - deriv_energy(starting_energy, X_0, s)
                    N_electrons += 1


                    if Energy_after_process > Critical_energy_e:
                        probabilità = 1-np.exp(-s)
                        
                        if (np.random.uniform() < probabilità):
                            
                            new_particles.append({'Type': 'Photon', 'Energy': Energy_after_process/2, 'High': altitude})
                            new_particles.append({'Type': 'Electron', 'Energy': Energy_after_process/2, 'High': altitude}) 
                            N_photons +=1 
                            Altitude_event.append(altitude)
                            
                        else:
                            altitude=h_in-step*(h_in-h_det)
                            new_particles.append({'Type': 'Electron', 'Energy': Energy_after_process, 'High': altitude})
                                 
                    else:
                        stop_while = 1
                else:
                    stop_while = 1
                

            
            elif type == 'Photon':
                if particle_Energy > kappa and altitude>h_det:
                    N_photons +=1 
                    probabilità = 1 - np.exp(-(7/9)*s)
                    if (np.random.uniform() < probabilità):

                        
                        new_particles.append({'Type': 'Electron', 'Energy': particle_Energy/2, 'High': altitude})
                        new_particles.append({'Type': 'Positron', 'Energy': particle_Energy/2, 'High': altitude}) 
                        N_electrons += 1
                        N_positrons += 1
                        N_photons -= 1 
                        Altitude_event.append(altitude)
                        
                    else:
                        new_particles.append({'Type': 'Photon', 'Energy': particle_Energy, 'High': altitude}) 
 
                        
                
                else:
                    stop_while = 1
                        

            else: #Type_particella == 'Positron':
                if particle_Energy > deriv_energy(starting_energy, X_0, s) and altitude>h_det: 
                    Energy_after_process = particle_Energy - deriv_energy(starting_energy, X_0, s)
                    
                    if Energy_after_process > Critical_energy_p:
                        N_positrons += 1 
                        probabilità = 1-np.exp(-s)
                        if (np.random.uniform() < probabilità):

                    
                            new_particles.append({'Type': 'Photon', 'Energy': Energy_after_process/2, 'High': altitude}) 
                            new_particles.append({'Type': 'Positron', 'Energy': Energy_after_process/2, 'High': altitude}) 
                            N_photons +=1 
                            Altitude_event.append(altitude)
                            
                        else:
                
                            new_particles.append({'Type': 'Positron', 'Energy': Energy_after_process, 'High': altitude})
                            
                    else:
                        stop_while = 1

                else:
                    stop_while = 1

            if stop_while == 1: break
                        
        if stop_while == 1: break 
                    
        Particles.particles = new_particles   
    
        n_elettroni_totali.append(N_electrons)
        n_fotoni_totali.append(N_photons)
        n_positroni_totali.append(N_positrons)
        total_particles.append(N_electrons+N_photons+N_positrons)

def u_misure(value):
    """
    Returns a unit symbol based on the given value.

    Parameters:
    - value (int): The value.

    Returns:
    - u (str): The unit symbol ('M', 'G', 'T', or 'P').
    """

    if value < 10**3: u = 'M'
    if value < 10**6 and value > 10**3: u = 'G'
    if value < 10**9 and value > 10**6: u = 'T'
    if value < 10**12 and value > 10**9: u = 'P'

    return u

def flux_of_photons(Particles,angle):
    """
    Calculates the flux of photons for a given list of particles.

    Parameters:
    - Particles (list): A list of particles.

    Returns:
    - flux (list): A list containing the flux values for each photon.
    - Saved_photons (list): A list of saved photon energies.

    The returns are sorted in increasing order.
    """


    Saved_photons=[]

    for i in range(0,len(Particles.particles)):
        if Particles.particles[i]['Type'] == 'Photon':
            Saved_photons.append(Particles.particles[i]['Energy'])


    flux=[]

    for i in range(0,len(Saved_photons)):
        flux.append((int(Saved_photons[i]))**(-2))

    flux.sort()
    flux.reverse()                                                                                      #making flux and energy readble for plot                                                        
    Saved_photons.sort()
    
    i=0
    for j in range(0,len(Saved_photons)):                                                             #find the index of the first photon with energy > Saved_photons_0
        if(Saved_photons[j]>deriv_energy(starting_energy,X_0/np.cos(angle),s)):                                     #and removes the energy<dEx0*s 
            i=j
        break

    return flux[i:],Saved_photons[i:]


def line(x, a, b,c):
    """
    Generates a new list by applying a linear transformation to each element of the input list.

    Parameters:
        x (List): The input list.
        a (float): The slope of the linear transformation.
        b (float): The y-intercept of the linear transformation.

    Returns:
        List: A new list where each element is obtained by multiplying the corresponding element of the input list by 'a' and adding 'b'.
    """
    y=[]
    for i in x:
        y.append(a*(i**(-2))+b*i+c)
    return y

def Energy_and_flux_of_simulation(energy,deep,s,angle):
    """
    Calculates the energy and flux of a new simulation.

    Parameters:
        energy (float): The starting energy for the simulation.
        deep (float): The depth of the simulation.
        s (float): The parameter s for the simulation.
        angle (float): The angle parameter for the simulation.

    Returns:
        tuple: A tuple containing the flux and the number of saved photons already sorted and reversed.
    """
    P = Swarm(energy)               
    simulate(s, deep/np.cos(angle), P)    
    flux, Saved_photons = flux_of_photons(P,angle)

    return flux,Saved_photons

# Example usage with curve_fit:
# xdata and ydata would be your data vectors
# popt, pcov = curve_fit(landau_dist, xdata, ydata, p0=[initial_mpv, initial_eta, initial_A])
#######################################################################################
#
#Class of Particles
#        
#######################################################################################


class photons:
    """
    Class representing a photon with a specific energy.

    Attributes:
       -E (float): The energy of the photon.
    """

    def __init__(self, Energy):
        """
        Initialize a photon instance with the given energy.

        Parameters:
            -Energy (float): The energy to set for the photon.
        """
        self.E = Energy

class electrons:
    """
    Class representing an electron with a specific energy.

    Attributes:
        -E (float): The energy of the electron.
    """

    def __init__(self, Energy):
        """
        Initializes a new instance of the electron class with the specified energy.

        Parameters:
            -Energy (float): The energy of the electron.
        """
        self.E = Energy

class positrons:

    """
    Class representing a positron with a specific energy.

    Attributes:
        -E (float): The energy of the positron.
    """

    def __init__(self, Energy):
        """
        Initializes a new instance of the positron class with the specified energy.

        Parameters:
            -Energy (float): The energy of the positron.
        """
        self.E = Energy


class Swarm:

    """
    
    This class rappresent the swarm of particles in the simulation.
    Variables:
                -E0 (float): The starting energy 
                -particles (list): The list of particles
                -number_particles (int): The number of particles
                -H (float): The initial altitude (took from constants)
    
    """
    def __init__(self, E0):
        self.E0 = E0
        self.H=h_in 
        self.particles = [{'Type': 'Photon', 'Energy': E0, 'High': h_in}]
        self.number_particles = []
    


#######################################################################################
#
#Main Program 
#     
# 
#1-Part: User input to start the simulation
#          
#######################################################################################
        



"""
The program ask to user to input : - starting energy
                                   - step size
"""
try:
    starting_energy = float(input("\nInserisci l'Energy iniziale in MeV(max 100Tev): "))
except:
    raise ValueError("Numero inserito sbagliato, perfavore inserire in numero in fomato e.g 10GeV=10000MeV NO 10**4")
s=float(input("\nInserisci il passo dello step tra 0 e 1:"))



Particles=Swarm(starting_energy)    #First simulation
n_elettroni_totali = []
n_positroni_totali = []
n_fotoni_totali = []
total_particles = []
Altitude_event=[]



        
simulate( s, X_0, Particles)
print("\n---------------------------------\n")
print("Ad ogni step:\n")
print(f"Numero di fotoni totali : {n_fotoni_totali}")
print(f"Numero di positroni totali : {n_positroni_totali}")
print(f"Numero di elettroni totali : {n_elettroni_totali}")
print(f"Numero di particelle totali : {total_particles}")



print("Con energia iniziale {:} eV".format(starting_energy))
Altitude_event=list(set(Altitude_event)) 
Altitude_event.sort()
Altitude_event.reverse()
print("\nAltezze delle particelle:\n ")
print("Evento       Altezza")
for i in range(0,len(Altitude_event)):
    print(i,"         ",round(Altitude_event[i],2))   





#######################################################################################
    

#2 part: Plotting the results and graph them
    

#######################################################################################

"""
Graph plot of the energy of photons nad flux.
Variables:
            -Saved_photons_0: energy of photons
            -flux_0: flux of photons

Formula:
            flux=k*energy**-2       where k is normalized to 1


"""


flux_0,Saved_photons_0=flux_of_photons(Particles,0)                                     # [@]  User flux and energy

plt.plot(Saved_photons_0,flux_0,".",label="Photons")                                    #plot of photons
plt.xlabel("log E(MeV)")
plt.ylabel("log Flux(MeV**-2)")
plt.title("Flux-Energy of photons {:}eV".format(starting_energy))
plt.xscale("log")
plt.yscale("log")
plt.legend(loc="upper right")
plt.show()

"""

Histogram plot of the energy of photons.
Variables:
        -Saved_photons_0: energy of photons

"""

plt.hist(Saved_photons_0,bins=50+int(np.sqrt(len(Saved_photons_0))))                       #Hist of photons 
plt.xlabel("log E(MeV)")
plt.ylabel("N*of samples")
plt.title("Histogram of Energy of photons at {:}eV".format(starting_energy))
plt.xscale("log")
plt.show()


#######################################################################################
    

#3 Part: Simulation of 2 new Swarm with different starting angle and
#        comparison with the preavius Swarn (made in Part 1) 
    

#######################################################################################

b=input("\nVuoi vedere i grafici a diversi angoli ma con la stessa simulazione?\n(Se si vuole utilizzare anche il prossimo passaggio inserire 1)\n")
if int(b)==1:

    """

    Simulation of 2 new Swarm with different starting angle:

        -Particles_1 with 40° or 2*pi/9 angle  [1]
        -Particles_2 with 20° or pi/9 angle    [2]
        

    """

    flux_40g_user,Saved_photons_40g_user=Energy_and_flux_of_simulation(starting_energy,X_0,s,2*np.pi/9)  #first simulation[1]
    flux_20g_user, Saved_photons_20g_user = Energy_and_flux_of_simulation(starting_energy,X_0,s,np.pi/9) #second simulation[2]



    """
    N.B.:
    In this part we take the simulation done in Part 1.


    Sorting the flux and the energy of photons in order to plot the curve.
    To make the curve.fit (from scipy), we need to use the function "line" to fit the curve.
    In the plot there are 2 graph(in log scale): -Fitted curve
                                                 -Flux at 0°

    """
    params_0, params_covariance_0 = optimize.curve_fit(line, Saved_photons_0, flux_0)                     #At 0°
    fitted_curve_0 = line(Saved_photons_0, params_0[0], params_0[1],params_0[2])

    params_1, params_covariance_1 = optimize.curve_fit(line, Saved_photons_40g_user, flux_40g_user)       #At 40°
    fitted_curve_1 = line(Saved_photons_40g_user, params_1[0], params_1[1],params_1[2])


    params_2, params_covariance_2 = optimize.curve_fit(line, Saved_photons_20g_user, flux_20g_user)       #At 20°
    fitted_curve_2 = line(Saved_photons_20g_user, params_2[0], params_2[1],params_2[2])
    
    
    
    
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))                                         # 3 rows, 1 column
    fig.subplots_adjust(hspace=0.5)
    #For Energy=Decided by the user go to [@] 

    #For staring angle 0°
    axs[0].plot(Saved_photons_0, fitted_curve_0,"--" ,label="Fitted Curve", color="orange")  #plot of fitted curve
    axs[0].plot(Saved_photons_0, flux_0, ".", label="Flux with 0°", color="blue")            #plot of data
    axs[0].set_xlabel("log E(MeV)")
    axs[0].set_ylabel("log Flux(MeV**-2)")
    # axs[0].set_title("Flux-Energy of photons for Flux_0",loc="left",fontsize="small")
    axs[0].legend(loc="upper right")
    axs[0].set_xscale("log")
    axs[0].set_yscale("log")

    #For staring angle 40°

    axs[1].plot(Saved_photons_40g_user, fitted_curve_1,"--", label="Fitted Curve", color="indianred")   #plot of fitted curve
    axs[1].plot(Saved_photons_40g_user, flux_40g_user, ".", label="Flux with 40°", color="purple")        #plot of data
    axs[1].set_xlabel("log E(MeV)")
    axs[1].set_ylabel("log Flux(MeV**-2)")
    #axs[1].set_title("Flux-Energy of photons for flux_40g_user",,loc="left",fontsize="small")
    axs[1].legend(loc="upper right")
    axs[1].set_xscale("log")
    axs[1].set_yscale("log")

    #For staring angle 20°
    axs[2].plot(Saved_photons_20g_user, fitted_curve_2, "--",label="Fitted Curve", color="magenta")     #plot of fitted curve
    axs[2].plot(Saved_photons_20g_user, flux_20g_user, ".", label="Flux with 20°", color="red")                #plot of data
    axs[2].set_xlabel("log E(MeV)")
    axs[2].set_ylabel("log Flux(MeV**-2)")
    #axs[2].set_title("Flux-Energy of photons for Flux_2",loc="left",fontsize="small")
    axs[2].legend(loc="upper right")
    axs[2].set_xscale("log")
    axs[2].set_yscale("log")
    plt.suptitle("Flux-Energy of photons with different starting angle",fontsize="xx-large",va="center")
    plt.show()


#######################################################################################
    

#4 Part: Simulation of 4 new Swarm with different starting energy and different angles
#        and plotting the Swarm of Part 1

#######################################################################################



"""
In this part we will do the same as Part 3 but with different starting energy.
We gona take 4 different starting energies and for them we will take 3 different angles:

    1) Energy=Decided by the user
    2) Energy=10 TeV
    3) Energy=50 TeV
    4) Energy=100 TeV

And the 3 different angles are:

    -0°
    -20°
    -40°

N.B: All 4 simulation have the same s choose by the user!
"""

b=input("\nVuoi vedere i grafici a diversi angoli e diverse energie?\n")
if int(b)==1:
    try:
        print("\nAttenzione il programma potrebbe impiegare qualche secondo in più,attendere prego\n")
        #At 0°  

        Saved_photons_0g_user=Saved_photons_0
        flux_0g_user=flux_0                                                                                        #User input    For Energy=Decided by the user go to [@]
        flux_0g_10,Saved_photons_0g_10=Energy_and_flux_of_simulation(10**7,X_0,s,0)                               #10 TeV
        flux_0g_50,Saved_photons_0g_50=Energy_and_flux_of_simulation(5*10**7,X_0,s,0)                             #50 TeV           
        flux_0g_100,Saved_photons_0g_100=Energy_and_flux_of_simulation(10**8,X_0,s,0)                             #100 TeV               

        #At 20° or pi/9
        #flux and Saved_photons at 20° already make in Part 3:                                                     User input    For Energy=Decided by the user go to [@]
        flux_20g_10,Saved_photons_20g_10=Energy_and_flux_of_simulation(10**7,X_0,s,np.pi/9)                       #10 TeV
        flux_20g_50,Saved_photons_20g_50=Energy_and_flux_of_simulation(5*10**7,X_0,s,np.pi/9)                     #50 TeV           
        flux_20g_100,Saved_photons_20g_100=Energy_and_flux_of_simulation(10**8,X_0,s,np.pi/9)                     #100 TeV               

        #At 40° or 2*pi/9
        #flux and Saved_photons at 40° already make in Part 3:                                                     #User input    For Energy=Decided by the user go to [@]
        flux_40g_10,Saved_photons_40g_10=Energy_and_flux_of_simulation(10**7,X_0,s,2*np.pi/9)                     #10 TeV
        flux_40g_50,Saved_photons_40g_50=Energy_and_flux_of_simulation(5*10**7,X_0,s,2*np.pi/9)                   #50 TeV           
        flux_40g_100,Saved_photons_40g_100=Energy_and_flux_of_simulation(10**8,X_0,s,2*np.pi/9)                   #100 TeV               


        """
        
        Plotting the graphs of simulations with different starting energy and different angles.
        The plot is divided in 4 subplots:
                    -1) different angle at user energy
                    -2) different angle at 10 TeV
                    -3) different angle at 50 TeV
                    -4) different angle at 100 TeV

        All the subplots are in log scale to make it more understandble.  
        """


        fig, axs = plt.subplots(2,2, figsize=(10, 15))
        fig.subplots_adjust(hspace=0.5)


        #Plotting at user energy
        axs[0,0].plot(Saved_photons_0g_user, flux_0g_user, ".", label="0°", color="green",alpha=0.2)                      #flux and energy of photons at 0°
        axs[0,0].plot(Saved_photons_20g_user, flux_20g_user, ".", label="20°", color="red",alpha=0.2)                     #flux and energy of photons at 20°
        axs[0,0].plot(Saved_photons_40g_user, flux_40g_user, ".", label="40°", color="blue",alpha=0.2)                    #flux and energy of photons at 40°


        axs[1,0].plot(Saved_photons_0g_10, flux_0g_10, ".", label="0°", color="magenta", alpha=0.4)                       #flux and energy of photons at 0°
        axs[1,0].plot(Saved_photons_20g_10, flux_20g_10, ".", label="20°", color="indianred",alpha=0.2)                   #flux and energy of photons at 20°
        axs[1,0].plot(Saved_photons_40g_10, flux_40g_10, ".", label="40°", color="orange",alpha=0.2)                      #flux and energy of photons at 40°

        axs[0,1].plot(Saved_photons_0g_50, flux_0g_50, ".", label="0°", color="purple",alpha=0.2)                         #flux and energy of photons at 0°
        axs[0,1].plot(Saved_photons_20g_50, flux_20g_50, ".", label="20°", color="rosybrown",alpha=0.2)                   #flux and energy of photons at 20°
        axs[0,1].plot(Saved_photons_40g_50, flux_40g_50, ".", label="40°", color="deepskyblue",alpha=0.4)                 #flux and energy of photons at 40°



        axs[1,1].plot(Saved_photons_0g_100, flux_0g_100, ".", label="0°", color="blue",alpha=0.2)                         #flux and energy of photons at 0°
        axs[1,1].plot(Saved_photons_20g_100, flux_20g_100, ".", label="20°", color="lime",alpha=0.5)                      #flux and energy of photons at 20°
        axs[1,1].plot(Saved_photons_40g_100, flux_40g_100, ".", label="40°", color="red",alpha=0.2)                       #flux and energy of photons at 40°


        axs[0,0].set_xlabel("log E(MeV)")
        axs[0,0].set_ylabel("log Flux(MeV**-2)")
        axs[0,0].set_title("Flux-Energy of photons decided by user",loc="left",fontsize="small")
        axs[0,0].legend(loc="upper right")
        axs[0,0].set_xscale("log")
        axs[0,0].set_yscale("log")


        axs[1,0].set_xlabel("log E(MeV)")
        axs[1,0].set_ylabel("log Flux(MeV**-2)")
        axs[1,0].set_title("Flux-Energy of photons at 10 Tev",loc="left",fontsize="small")
        axs[1,0].legend(loc="upper right")
        axs[1,0].set_xscale("log")
        axs[1,0].set_yscale("log")


        axs[0,1].set_xlabel("log E(MeV)")
        axs[0,1].set_ylabel("log Flux(MeV**-2)")
        axs[0,1].set_title("Flux-Energy of photons at 50 Tev",loc="left",fontsize="small")
        axs[0,1].legend(loc="upper right")
        axs[0,1].set_xscale("log")
        axs[0,1].set_yscale("log")

        axs[1,1].set_xlabel("log E(MeV)")
        axs[1,1].set_ylabel("log Flux(MeV**-2)")
        axs[1,1].set_title("Flux-Energy of photons at 100 Tev",loc="left",fontsize="small")
        axs[1,1].legend(loc="upper right")
        axs[1,1].set_xscale("log")
        axs[1,1].set_yscale("log")

        plt.suptitle("Flux-Energy of photons with different starting angle and different energy",fontsize="xx-large",va="center")
        plt.show()

    except:
        raise ValueError("Non si è eseguito il punto precedente, errore!")