import numpy as np 
from scipy import optimize
import matplotlib.pyplot as plt
import numpy.random as random


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
#Hit or miss
#        
#######################################################################################

 
fotoni_energie=random.uniform(low=1000000,high=100000000,size=50000)         #we generate 50000 photons
y=fotoni_energie**(-2)
value=random.uniform(low=0,high=max(y),size=50000)
mask=y>value

fotoni_energie=fotoni_energie[mask]     #starting energy photons




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
    Simulates a particle system based on given parameters.

    Args:
        s (float): The step size for the simulation.
        d (float): The distance factor for the altitude calculation.
        Particles (object): An object containing information about the particles.

    Returns:
        None
    """

    
    particle_Energy = Particles.particles[0]['Energy']
    step = 0
    new_particles= Particles.particles
    pippolo=deriv_energy(starting_energy, X_0, s)
    while particle_Energy > 0:
        
        
        Particles.particles = new_particles   
        step +=1
        new_particles = []
        N_electrons = 0 
        N_photons = 0 
        N_positrons = 0 
        ciao=[]

        

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
                            #Altitude_event.append(altitude)           #Uncomment when you test
                            ciao.append(Energy_after_process/2)
                            
                        else:
                            altitude=h_in-step*(h_in-h_det)
                            new_particles.append({'Type': 'Electron', 'Energy': Energy_after_process, 'High': altitude})
                            ciao.append(Energy_after_process)   

            
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
                        #Altitude_event.append(altitude)           #Uncomment when you test
                        ciao.append(particle_Energy/2)
                        
                    else:
                        new_particles.append({'Type': 'Photon', 'Energy': particle_Energy, 'High': altitude}) 
                        ciao.append(particle_Energy)              

            else:                                                                                                   #Type_particella == 'Positron':
                if particle_Energy > deriv_energy(starting_energy, X_0, s) and altitude>h_det: 
                    Energy_after_process = particle_Energy - deriv_energy(starting_energy, X_0, s)
                    
                    if Energy_after_process > Critical_energy_p:
                        N_positrons += 1 
                        probabilità = 1-np.exp(-s)
                        if (np.random.uniform() < probabilità):

                    
                            new_particles.append({'Type': 'Photon', 'Energy': Energy_after_process/2, 'High': altitude}) 
                            new_particles.append({'Type': 'Positron', 'Energy': Energy_after_process/2, 'High': altitude}) 
                            N_photons +=1 
                            # Altitude_event.append(altitude)           #Uncomment when you test
                            ciao.append(Energy_after_process/2)
                            
                        else:
                
                            new_particles.append({'Type': 'Positron', 'Energy': Energy_after_process, 'High': altitude})
                            ciao.append(Energy_after_process)
                            

        total_n_electrons.append(N_electrons)
        total_n_photons.append(N_photons)
        total_n_positrons.append(N_positrons)
        total_particles.append(N_electrons+N_photons+N_positrons)
        
        ciaone=np.array(ciao)
        mask =  ciaone > pippolo
        ciaone=ciaone[mask]
        if(len(ciaone)==0):
            totale=total_particles[-2]
            break


def flux_of_photons(Particles):
    """
    Calculate the flux of photons and energy of photons from a given list of particles.

    Parameters:
    - Particles: A Particle List object containing the list of particles.

    Returns:
    - flux: A list of the calculated flux values for each photon.
    - Saved_photons: A list of the energies of the saved photons.
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
    
    return flux,Saved_photons  



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
The program ask to user to input : 
    - starting energy
    - step size
"""
try:
    starting_energy = float(input("\nInserisci l'Energy iniziale in MeV(max 100Tev): \n "))
except:
    raise ValueError("Numero inserito sbagliato, perfavore inserire in numero in fomato e.g 10GeV=10000MeV NO 10**4")
s=float(input("\nInserisci il passo dello step tra 0 e 1:(si consiglia uno step alto. e.g. 0.7) \n"))



Particles=Swarm(starting_energy)                                       #First simulation and generation of particles
total_n_electrons = []                                                 #|
total_n_positrons = []                                                 #|Saving number of particles for 
total_n_photons = []                                                   #|each type
total_particles = []                                                   #|
step=0

# Altitude_event=[]                                                    #Uncomment to test the program

        
simulate( s, X_0, Particles)
print("\n---------------------------------\n")
print("Ad ogni step:\n")
print(f"Numero di fotoni totali : {total_n_photons[:-1]}")
print(f"Numero di positroni totali : {total_n_positrons[:-1]}")       #Description of what happening
print(f"Numero di elettroni totali : {total_n_electrons[:-1]}")
print(f"Numero di particelle totali : {total_particles[:-1]}")

print(f"\nAlla fine sono arrivati al rivelatore ", total_particles[-2], " particelle\n")

print("Con energia iniziale {:} MeV".format(starting_energy))
print("Derivata x step:",round(deriv_energy(starting_energy, X_0, s),2)," MeV")
print("\n---------------------------------\n")



lenoo=np.linspace(0,len(total_particles),len(total_particles))
plt.plot(lenoo[:-1],total_particles[:-1])                            #plotting the number of particles for each step
plt.title("Numero di particelle per ogni step")
plt.ylabel("Numero di particelle")
plt.xlabel("Numero di step")
plt.show()


#######################################################################################
    

#2 part: Plotting the results and graph them
    

#######################################################################################

"""
Graph plot , in log-log scale, of the energy of photons and flux.
Variables:
            -Saved_photons_0: energy of photons
            -flux_0: flux of photons

Formula:
            -flux=k*energy**-2       where k is normalized to 1


"""


flux_0,Saved_photons_0=flux_of_photons(Particles)                                     # [@]  User flux and energy

plt.plot(Saved_photons_0,flux_0,".",label="Photons")                                    #plot of photons
plt.xlabel("log E(MeV)")
plt.ylabel("log Flux(MeV**-2)")
plt.title("Flux-Energy of photons {:}MeV".format(starting_energy))
plt.xscale("log")
plt.yscale("log")
plt.legend(loc="upper right")
plt.show()

"""

Histogram plot of the energy of photons.
Variables:
        -Saved_photons_0: energy of photons (in log scale)

For the number of bins we use the poissonian distribution:

- n_of_bins=sqrt(frequency)

N.B. It works better if the number of bins is at least 25 for the poissonian distribution

"""

plt.hist(Saved_photons_0,bins=int(np.sqrt(len(Saved_photons_0))))                       #Hist of photons 
plt.xlabel("log E(MeV)")                                                                #number of bins follows the poissonian distribution
plt.ylabel("N*of samples")
plt.title("Histogram of Energy of photons at {:}MeV".format(starting_energy))
plt.xscale("log")
plt.show()


#######################################################################################
    

#3 Part: Simulation of 2 new Swarm with different starting angle and
#        comparison. Using Hit or miss method to create a simulation of 
#        50000 photons in range 1-100TeV
    

#######################################################################################

b=input("\nVuoi vedere i grafici a diversi angoli ma con la stessa simulazione?\n(Inserire 1 se si, 0 altrimenti)\n")
if int(b)==1:

    """
    Plotting hist of hit or miss method.
    Variables:
                -fotoni_energie: energy of photons
    
    
    For the number of bins we use the poissonian distribution:

    - n_of_bins=sqrt(frequency)

    N.B. It works better if the number of bins is at least 25 for the poissonian distribution

    
    """
    print("\nAttendere prego\n")
    plt.hist(fotoni_energie,bins=int(np.sqrt(len(fotoni_energie))))
    plt.title(r"Hit or miss method to generate a flux of photons in range 1-100TeV  Spectrum: $P(E)=kE^{-2}$")
    plt.xlabel("E(MeV)")
    plt.ylabel("N* of photons")
    plt.show()

    """
    Calculate the number of particles in the detector for a given list of photon energies.
    This calcule must be done for each starting angle.

    """  


    n_finale_0=[]

    for i in fotoni_energie:                                            #0*        
        total_particles = []
        Particles=Swarm(i)                                
        simulate(s, X_0, Particles)
        n_finale_0.append(total_particles[-2])

    n_finale_1=[]                                                       #20*

    for i in fotoni_energie:                                
        total_particles = []
        Particles=Swarm(i)                                
        simulate(s, X_0*np.cos(np.pi/9), Particles)
        n_finale_1.append(total_particles[-2])


    n_finale_2=[]                                                       #40*

    for i in fotoni_energie:                                
        total_particles = []
        Particles=Swarm(i)                                
        simulate(s, X_0*np.cos(2*np.pi/9), Particles)
        n_finale_2.append(total_particles[-2])

 
    """

    Plotting the results of the simulation.

    """
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))                    # 3 rows, 1 column
    fig.subplots_adjust(hspace=0.5)


    #For Energy=Decided by the user go to [@] 

    axs[0].plot(fotoni_energie, n_finale_0, ".", label="Flux with 0°", color="blue")
    axs[0].set_xlabel("E(MeV)")
    axs[0].set_ylabel("N* of particles")
    axs[0].legend(loc="upper right")

    #For staring angle 20°

    axs[1].plot(fotoni_energie, n_finale_1, ".", label="Flux with 20°", color="red")
    axs[1].set_xlabel("E(MeV)")
    axs[1].set_ylabel("N* of particles")
    axs[1].legend(loc="upper right")

    #For staring angle 40°

    axs[2].plot(fotoni_energie, n_finale_2, ".", label="Flux with 40°", color="purple")
    axs[2].set_xlabel(" E(MeV)")
    axs[2].set_ylabel(" N* of particles")
    axs[2].legend(loc="upper right")

    plt.suptitle("N* of particles reveald-Energy of photons with different starting angle",fontsize="xx-large",va="center")
    plt.show()

    print("\n---------------------------------------\n")
    print("In media sono state rilevate:\n")
    print("A 0* gradi: ",round(np.mean(n_finale_0))," particelle\n")
    print("A 20* gradi: ",round(np.mean(n_finale_1))," particelle\n")
    print("A 40* gradi: ",round(np.mean(n_finale_2))," particelle\n")
    print("Con un numero di : ",50000, " particelle\n")
    print("\n---------------------------------------\n")







#######################################################################################
    

#Testing the program codes:
    

#######################################################################################



# Altitude_event=list(set(Altitude_event)) 
# Altitude_event.sort()
# Altitude_event.reverse()
# # print("\nAltezze delle particelle:\n ")                         #to see the altitude of the particles for each step.
# # print("Evento       Altezza")
# # for i in range(0,len(Altitude_event)):
# #     print(i,"         ",round(Altitude_event[i],2))   



