# -*- coding: utf-8 -*-

"""
Created on Mon Jun  7 14:12:39 2021

@author: Gabriel Amorosetti
UT3 - L2 Parcours Spécial Physique

Internship at LAPLACE Laboratory, Toulouse 
Supervised by Hubert Caquineau, from 2021-06-07 to 2021-07-09

Python development of a physico-chemical data preprocessing software towards a partial differential equations resolution commercial software
"""

import copy         # Used to deepcopy lists

####################################################################
'''
CLASSES CREATIONS
'''


'''
Species class creation
'''

class Species:   
    
    # Attributes (Species physico-chemical data)
           
    def __init__(self, nameSpecies='0', typeSpecies='0', massSpecies='0', sigmaSpecies='0', epsilon_kSpecies='0', coeff_diffSpecies='0'):
        
        self.nameSpecies = nameSpecies              # Species name
        self.typeSpecies = typeSpecies              # Type (neutral, ion, neutrals to the walls)
        self.massSpecies = massSpecies              # Mass
        self.sigmaSpecies = sigmaSpecies            # Sigma
        self.epsilon_kSpecies = epsilon_kSpecies    # Epsilon_k
        self.coeff_diffSpecies = coeff_diffSpecies  # Diffusion coefficient
        
     # Methods 
     
    def readSpecies(self):                          # Display species attributes
        print(f'\n----------------------- \nSpecies : {self.nameSpecies} \nType : {self.typeSpecies} \nMass = {self.massSpecies} kg/mol \nSigma = {self.sigmaSpecies} angstrom \nEpsilon_k = {self.epsilon_kSpecies} K \nDiffusion coefficient = {self.coeff_diffSpecies} unité \n-----------------------')
               
        

'''
SpeciesList class creation
'''

class SpeciesList:
    
    def __init__(self,species_List=[]):                 # species_List attribute is the list containing all the Species objects
        self.species_List = species_List
        
    def verifSpecies(self):  
        error=0                                         # Function to verify that all Species in SpeciesList are unique
        for i in range (len(self.species_List)):
            for j in range (len(self.species_List)) :
                if i != j :
                    if self.species_List[i].nameSpecies==self.species_List[j].nameSpecies:
                        print (f'\n----------------------- \n Same species is appearing two times in the list : {self.species_List[i].nameSpecies} \n-----------------------')
                        error+=1
        if error==0:
            print('\n----------------------- \nAll species in list are unique \n-----------------------')
            
    def verifNoCoeffSpecies(self):                      # Function to verify that the names of the species begin with a letter and not a number 
        error=0 
        verif_list=['0','1','2','3','4','5','6','7','8','9']
        for i in range (len(self.species_List)):
            for j in range (len(verif_list)):
                if self.species_List[i].nameSpecies[0] == verif_list[j] :
                    print (f'\n----------------------- \n Error : stoichiometric coefficient in front on the name species "{self.species_List[i].nameSpecies}" \n-----------------------')
                    error+=1
        if error==0:
            print ('\n----------------------- \n No coefficient in front of a name species \n-----------------------')
            
    def readSpeciesList(self):                          # Display all species in SpeciesList
        for i in range (len(self.species_List)):
            self.species_List[i].readSpecies()
            
    def writeSpecies(self):
        
        f= open("Species_and_Reactions.java","a")          # Writing the species and their attributes to the Java file according to the format needed

        f.write('\n  public static Model run2(Model model) {')
        
        for i in range (len(self.species_List)):
            
            # Sometimes we can have molecular ions like for example O2.NO+, written in the original file 'NOpO2'. We need to remove the p (or m) and put it at the end in order to have a species name like that : 'NOO2p'
            # If there is 'p' or 'm' in the species name, we remove it and write it at the end (so nothing will change for species like NO2+, written 'NO2p' in the original file)
    
            if ('p') in self.species_List[i].nameSpecies:                                           # 'p' or 'm' in a species name refers to a positive or negative ion
                
                before_change=self.species_List[i].nameSpecies                                      # before_change is the name before we put the 'p' at the end                                             
                
                self.species_List[i].nameSpecies=self.species_List[i].nameSpecies.replace('p','')   
                self.species_List[i].nameSpecies=self.species_List[i].nameSpecies+'p'
                
                ########## Translation of 'p' and 'm' on the species causing error on Comsol
                
                # self.species_List[i].nameSpecies=self.species_List[i].nameSpecies.replace('p','+')  # Tranlating it to '+' or '-' because the java file needs to be written like that)
                
                ##########
                
                after_change=self.species_List[i].nameSpecies                                       # after_change is the name after we put the 'p' at the end
                print(f'Warning : {before_change} changed to {after_change}')                       # print to warn the user. Can be useful if there are species with a 'p' in the middle of the name that is not a positive charge but part of the name
                    
            if ('m') in self.species_List[i].nameSpecies:
                
                before_change=self.species_List[i].nameSpecies                                      # Doing exactly the same for species with 'm' in their name
               
                self.species_List[i].nameSpecies=self.species_List[i].nameSpecies.replace('m','') 
                self.species_List[i].nameSpecies=self.species_List[i].nameSpecies+'m'    
                
                ########## Translation of 'p' and 'm' on the species causing error on Comsol
                
                # self.species_List[i].nameSpecies=self.species_List[i].nameSpecies.replace('m','-') 
                
                ##########
                
                after_change=self.species_List[i].nameSpecies
                print(f'Warning : {before_change} changed to {after_change}')                
            
            self.species_List[i].nameSpecies=self.species_List[i].nameSpecies.replace('*', 'e') # '*' refers to electronically excited species. We need to replace '*' with 'e'
            self.species_List[i].nameSpecies=self.species_List[i].nameSpecies.replace('_', '')  #
            self.species_List[i].nameSpecies=self.species_List[i].nameSpecies.replace('.', '')  #
            
            f.write('\n    model.component("comp1").physics("plas").create("spec1", "Species", 1);')
            f.write(f'\n    model.component("comp1").physics("plas").feature("spec1").set("specName", "{self.species_List[i].nameSpecies}");')
            f.write(f'\n    model.component("comp1").physics("plas").feature("{species[i].nameSpecies}").set("M", "{self.species_List[i].massSpecies}[kg/mol]");')
            f.write(f'\n    model.component("comp1").physics("plas").feature("{species[i].nameSpecies}").set("sigma", "{self.species_List[i].sigmaSpecies}[angstrom]");')
            f.write(f'\n    model.component("comp1").physics("plas").feature("{species[i].nameSpecies}").set("epsilonkb", "{self.species_List[i].epsilon_kSpecies}[K]");')
        
        f.write('\n\n    return model;\n  }\n')
        f.close()     


'''
Reaction class creation
'''

class Reaction:
    
    # Attributes (data about the chemical reaction)
    
    def __init__(self, eq_reaction=[], reagents=[], products=[],k=0):
        self.eq_reaction=eq_reaction                                    # eq_reaction is a list containing the chemical reaction equation
        self.reagents=reagents                                          # reagents is a list containing the reagents of the chemical reaction
        self.products=products                                          # products is a list containing the products of the chemical reaction
        self.k=k                                                        # k is the value of the k, a constant associated to the chemical reaction
        
    def readReaction(self):                                             # Display reaction attributes
        print(f'\n----------------------- \nReaction : \n{self.eq_reaction} \n \nReagents : {self.reagents} \nProducts : {self.products} \nk = {self.k} unité \n-----------------------')
        
        
'''
ReactionList class creation
'''        
            
class ReactionsList:
    
    def __init__(self,reactions_List=[]):                 # reactions_List attribute is the list containing all the Reaction objects
        self.reactions_List = reactions_List
        
    def verifEqReaction(self): 
        error=0                                            # Function to verify that all Reactions in SpeciesList are unique
        for i in range (len(self.reactions_List)):
            for j in range (len(self.reactions_List)) :
                if j != i :
                    if self.reactions_List[i].eq_reaction==self.reactions_List[j].eq_reaction:
                        print (f'\n----------------------- \n Same reaction is appearing two times in the list : {self.reactions_List[i].eq_reaction}')
                        error+=1
        if error==0:
            print('\n----------------------- \nAll reactions in list are unique \n-----------------------')
            
    def readReactionsList(self):                          # Display all species in SpeciesList
        for i in range (len(self.reactions_List)):
            self.reactions_List[i].readReaction()
            
    def writeReactions(self):                             # Writing the reactions and their attributes to the Java file according to the format needed

        eir_counter=0                                     # eir_counter count the electron impact reactions                 
        rxn_counter=0                                     # rxn_counter count the classic reactions (non eir reactions)
        
        
        # Java does not support a single run() method containing too much information
        # We need to cut the information written on the Java file in severals run()
        
        reactions_in_run=0  # Count the reactions written in a run() method of Java
        run_number=2        # Count the number of run() in the Java file. It starts at 2 because there are already 2 run() before writing the reactions : 1 for the base of file, 1 for the species
        
        
        for i in range (len(self.reactions_List)):        # iterations on the reactions
                                
          #################################################
          
          # If a species is appearing more than one times in the reagents or products list, we need to keep only one occurence of the species in the list, with a coefficient in front of the name species (the stoichiometric coefficient = to the number of times the species is appearing in the list)
          
            # Reagents                                           
            
            r_same=[]                                            # r_same is almost the same list as the reagents list, but contains only one occurence of each species
            r_coeff=[]                                           # r_coeff[i] is the stoichiometric coefficient of the r_same[i] species
            
            for y in range(len(self.reactions_List[i].reagents)):
                if self.reactions_List[i].reagents[y] not in r_same:        # We add a species to the r_same list, and if the species is already in the list, we add 1 to the stoichiometric coefficient
                    r_same.append(self.reactions_List[i].reagents[y])           
                    r_coeff.append(1)
                    for z in range(y+1, len(self.reactions_List[i].reagents)):
                        if self.reactions_List[i].reagents[y]==self.reactions_List[i].reagents[z]:
                            r_coeff[-1]+=1
            
            for y in range(len(r_coeff)):       # If the stoichiometric coefficient is 1, we remove it because it's a convention to not put a stoichiometric coefficient when it is equal to 1
                if r_coeff[y]==1:
                    r_coeff[y]=''
                    
            new_reagents=[]
            for y in range(len(r_same)):
                new_reagents.append(f'{r_coeff[y]}{r_same[y]}')     # Creating the new reagents list with the stoichiometrics coefficients
                
            self.reactions_List[i].reagents=new_reagents            # Replacing the regeants list attribute with the new reagents list
               
            # Products

            p_same=[]                                           # p_same is almost the same list as the products list, but contains only one occurence of each species
            p_coeff=[]                                          # p_coeff[i] is the stoichiometric coefficient of the p_same[i] species
            
            for y in range(len(self.reactions_List[i].products)):
                if self.reactions_List[i].products[y] not in p_same:        # We add a species to the p_same list, and if the species is already in the list, we add 1 to the stoichiometric coefficient
                    p_same.append(self.reactions_List[i].products[y])
                    p_coeff.append(1)
                    for z in range(y+1, len(self.reactions_List[i].products)):
                        if self.reactions_List[i].products[y]==self.reactions_List[i].products[z]:
                            p_coeff[-1]+=1
            
            for y in range(len(p_coeff)):     # If the stoichiometric coefficient is 1, we remove it because it's a convention to not put a stoichiometric coefficient when it is equal to 1
                if p_coeff[y]==1:
                    p_coeff[y]=''
                    
            new_products=[]
            for y in range(len(p_same)):
                new_products.append(f'{p_coeff[y]}{p_same[y]}')    # Creating the new products list with the stoichiometrics coefficients
                
            self.reactions_List[i].products=new_products           # Replacing the products list attribute with the new products list
            
            #################################################
    
            # Sometimes we can have molecular ions like for example O2.NO+, written in the original file 'NOpO2'. We need to remove the p (or m) and put it at the end in order to have a species name like that : 'NOO2p'
            # If there is 'p' or 'm' in the species name, we remove it and write it at the end (so nothing will change for species like NO2+, written 'NO2p' in the original file)
            
            # Here we don't warn the user of the changes. We did it in the writeSpecies function in the SpeciesList class. If there is a problem on a spcies name, we detected it with the writeSpecies function.
            
            # Reagents
            for y in range(len(self.reactions_List[i].reagents)):
                
                if ('p') in self.reactions_List[i].reagents[y]:
                                        
                    self.reactions_List[i].reagents[y]=self.reactions_List[i].reagents[y].replace('p','') 
                    self.reactions_List[i].reagents[y]=self.reactions_List[i].reagents[y]+'p'
                    
                    
                if ('m') in self.reactions_List[i].reagents[y]:
                                        
                    self.reactions_List[i].reagents[y]=self.reactions_List[i].reagents[y].replace('m','') 
                    self.reactions_List[i].reagents[y]=self.reactions_List[i].reagents[y]+'m'
                               
            
            # We do the same for the species of the products list 
           
            eir_ionization=False # eir_ionization will be useful to know if the reaction is an ionization or not 
                                 # If there is an ion in the products, the reaction is an ionization, so eir_ionization will be set to True
            
            # Products                     
            for y in range(len(self.reactions_List[i].products)):
                
                if ('p') in self.reactions_List[i].products[y]:
                    eir_ionization=True 
                    self.reactions_List[i].products[y]=self.reactions_List[i].products[y].replace('p','') 
                    self.reactions_List[i].products[y]=self.reactions_List[i].products[y]+'p'
                    
                if ('m') in self.reactions_List[i].products[y]:
                    eir_ionization=True                    
                    self.reactions_List[i].products[y]=self.reactions_List[i].products[y].replace('m','') 
                    self.reactions_List[i].products[y]=self.reactions_List[i].products[y]+'m'
            
            ############
            
            # To respect the file format needed for Comsol, we need to put the positives ions at the end of the reagents and products lists
            
            # Reagents
            
            r_l=[]                  # r_l is the list where the neutrals species will be added
            r_l_p=[]                # r_l_p is the list where positives ions (with 'p') will be added (like N+ / Np in the original file)

            for y in range(len(self.reactions_List[i].reagents)):          # Iterations on the reagents list
                if not ('p') in self.reactions_List[i].reagents[y]:        # If it is a neutral species, we add it to r_l
                    r_l.append(self.reactions_List[i].reagents[y])
                if ('p') in self.reactions_List[i].reagents[y]:            # If it is a positive ion
                    r_l_p.append(self.reactions_List[i].reagents[y])       # We add it to the r_l_p list
                
            
            r_l.extend(r_l_p)
            # We create a list with, in order, the neutral species, then the positives ions with p in the names species
            
            self.reactions_List[i].reagents=r_l     # Replacing the reagents list with the new list r_l
            
            # Products
            
            p_l=[]                  # p_l is the list where the neutral species will be added
            p_l_p=[]                # p_l_p is the list where positives ions (with 'p')  will be added (like N+ / Np in the original file)

            for y in range(len(self.reactions_List[i].products)):           # Iterations on the products list
                if not ('p') in self.reactions_List[i].products[y]:         # If it is a neutral species, we add it to p_l
                    p_l.append(self.reactions_List[i].products[y])
                if ('p') in self.reactions_List[i].products[y]:             # If it is a positive ion
                    p_l_p.append(self.reactions_List[i].products[y])        # # We add it to the p_l_p list
           
            p_l.extend(p_l_p)
            # We create a list with, in order, the neutral species, then the positives ions with p in the names species
            
            self.reactions_List[i].products=p_l   # Replacing the reagents list with the new list p_l            
                       
            #############
            
            regeants_string=self.reactions_List[i].reagents[0]                      # regeants_string is used with products_string to create eq_reaction_string
            for j in range(1, len(self.reactions_List[i].reagents)):
                    regeants_string += f' + {self.reactions_List[i].reagents[j]}'
                                     
                    
            products_string=self.reactions_List[i].products[0]
            for j in range(1, len(self.reactions_List[i].products)):
                    products_string += f' + {self.reactions_List[i].products[j]}'
                    
                    
            eq_reaction_string = regeants_string + ' => ' + products_string        # eq_reaction_string is a string of characters of the chemical reaction formula
                                                                                   # We need to do this to add for exemples the spaces and '+' to respect the Java file format needed for Comsol
            
            k_string=self.reactions_List[i].k                                      # k_string is a string of character containing the k value expression
            
            eq_reaction_string=eq_reaction_string.replace("p","+")                 # 'p' or 'm' in a species name refers to a positive or negative ion 
            eq_reaction_string=eq_reaction_string.replace("m","-")                 # Tranlating it to '+' or '-' because the java file needs to be written like thatNo documentation 
            eq_reaction_string=eq_reaction_string.replace("*","e")                 # '*' refers to electronically excited species. We need to replace '*' with 'e'
            
            eq_reaction_string=eq_reaction_string.replace("_","")                  # Removing character causing error on Comsol 
            eq_reaction_string=eq_reaction_string.replace(".","")                  # Removing character causing error on Comsol
            k_string=k_string.replace("_", "")                                     # Removing character causing error on Comsol
            
            
            k_string=k_string.replace('Teff', '123xxx')                            # Translating the temparature variables, first to a random string to not replace 'Te' in 'Teff' for example
            k_string=k_string.replace('Te', '456yyy')                               
            k_string=k_string.replace('T', '789zzz')

            k_string=k_string.replace('123xxx', 'Teff')                                 # Need to correct with the right translation of Teff on Comsol  
            k_string=k_string.replace('456yyy', 'elTemp')                               # 'Te' is the temperature of the electrons. For Comsol this needs to be translated to 'elTemp'
            k_string=k_string.replace('789zzz', 'plas.T')                               # 'T' is the temperature of the gaz (or neutral species). For Comsol this needs to be translated to 'plas.T'
            k_string=k_string.strip('\n')
            


            if reactions_in_run==0:  # Corresponding to the last run() full, so we create a new run() where we will add reactions, or just the first run() with reactions
                run_number+=1        # Creation of a new run() on the Java file
                
                f= open("Species_and_Reactions.java","a")
                f.write(f'\n  public static Model run{run_number}(Model model) {{') # Writing the corresping Java syntax for the beginning of a run()
                f.close()
            
            # Then writing the reactions    
            
            if ('e') in regeants_string:   # If 'e' (electron) is in the reagents, the reaction is an electron impact reaction
                eir_counter+=1
                
                if eir_ionization==True:   # More precisely, if there is an ion in the products, the reaction is an ionization
                
                    f= open("Species_and_Reactions.java","a")                                 # Writing on the file
            
                    f.write(f'\n    model.component("comp1").physics("plas").create("eir{eir_counter}", "ElectronImpactReaction", 1);')
                    f.write(f'\n    model.component("comp1").physics("plas").feature("eir{eir_counter}").set("type", "Ionization");')
                    f.write(f'\n    model.component("comp1").physics("plas").feature("eir{eir_counter}").set("formula", "{eq_reaction_string}");')
            
                    f.close()
                    
                else:                     # If there it is an electron impact reaction but without ion in the products, the reaction is an excitation
                    
                    f= open("Species_and_Reactions.java","a")                                 # Writing on the file
            
                    f.write(f'\n    model.component("comp1").physics("plas").create("eir{eir_counter}", "ElectronImpactReaction", 1);')
                    f.write(f'\n    model.component("comp1").physics("plas").feature("eir{eir_counter}").set("type", "Excitation");')
                    f.write(f'\n    model.component("comp1").physics("plas").feature("eir{eir_counter}").set("formula", "{eq_reaction_string}");')
            
                    f.close()
                                                           
            else:                         # If 'e' (electron) is not in the reagents, the reaction is a classic reaction
                rxn_counter+=1

                f= open("Species_and_Reactions.java","a")                                 # Writing on the file
            
                f.write(f'\n    model.component("comp1").physics("plas").create("rxn{rxn_counter}", "Reaction", 1);')
                f.write(f'\n    model.component("comp1").physics("plas").feature("rxn{rxn_counter}").set("rType", "irrev");')
                f.write(f'\n    model.component("comp1").physics("plas").feature("rxn{rxn_counter}").set("formula", "{eq_reaction_string}");')
                f.write(f'\n    model.component("comp1").physics("plas").feature("rxn{rxn_counter}").set("kf", "{k_string}");')
                f.close()
                
                
         
            reactions_in_run+=1     # We wrote one more reaction in the current run()
            
            limit=80 # limit is the maximum number of reactions we want in a run. We can adapt it depending on Comsol compiling the file without error or not
            
            if reactions_in_run==limit or i==len(self.reactions_List)-1: # If there are enought reactions in the run() or we just added all the reactions and the last run() if not full (less than limit number reactions)
                
                f= open("Species_and_Reactions.java","a")                # Writing the corresping Java syntax for the end of a run()
                f.write('\n\n    return model;\n  }\n')                             
                f.close()
                
                reactions_in_run=0 # Setting reactions_in_run to 0 to begin a new run after this one
        
        f= open("Species_and_Reactions.java","a")                   # Writing the corresping Java syntax for the end of the file with multiples run()
        f.write('\n  public static void main(String[] args) {')
        f.write('\n    Model model = run();')
        f.write('\n    model = run2(model);')
        f.close()
        
        for w in range(3, run_number):
            f= open("Species_and_Reactions.java","a")
            f.write(f'\n    model = run{w}(model);')
            f.close()
        
        f= open("Species_and_Reactions.java","a")
        f.write(f'\n    run{run_number}(model);')
        f.write('\n  }')
        f.write('\n ')
        f.write('\n}')
        f.close()
        
        

                        
            
####################################################################
'''
FILE READING AND DATA COLLECTION
'''

data='Species_and_reactions.txt' # Original file containing species and reactions data

with open(data) as d:            # Opening the file
    lines_d=d.readlines()        # Creation of lines, a list containing the lines of the file text
d.close()

n= open("new_file.txt","w")      # Creation of new_file.txt
n.write('')

for i in range(len(lines_d)):    # As the commented lines with '%' on the original file don't have to be considered
    if lines_d[i][0]!='%':       # We write only the lines without '%' on new_file.txt
        n.write(lines_d[i])
n.close()

new_data='new_file.txt'          # new_file.txt is the new file we will use to read and collect data 

with open(new_data) as fi:       # Opening the file

    lines=fi.readlines()         # Creation of lines, a list containing the lines of the file text 
       
    
    species=[]                   # List where all the temporary species objects will be added     
    reactions=[]                 # List where all the temporary reaction objects will be added
    
# The program may contain more .strip('\n') than necessary but it's not an issue, it's better to avoid errors 
   
    for i in range(len(lines)):     # Iteration on the lines of the file
        
        index=i                 # index of the line i (in the lines list) (will be used where 'SPECIES:' or 'REACTION:' is appearing)
                                # Useful because the wanted data is contained on the following lines
    
        lines[index].strip(',')
        lines[index].strip(';')             # Removal of characters that can lead to error when reading data on the line 
        lines[index].strip('\n')
        lines[index].replace(' ', '')
                
    
        if ('SPECIES:') in lines[index]:
            
            temp=Species()          # Instantiation of a temporary species to collect data from the file at each iteration
                                    # No data for an attribute : the value 0 will be assigned as it was set in the Species class constructor
      
            l_s=lines[index].split(':') # l_s, l_t, l_m, l_sig, l_ep, l_c are lists composed of a splited line, used to collect only the data wanted on this line
            
            l_s[1]=l_s[1].strip('\n')
            
            if 'e'==l_s[1]:                              # Particular case for the electron species. As it appears only one time, we manually add the corresponding data to the lists
                temp.nameSpecies='e'.strip('\n')           # We remove '\n' again because it is appearing when splitting lines[index]
                temp.massSpecies='9.1e-31'.strip('\n')
                # No data for all the others attributes
               
            if 'e'!=l_s[1]:                                # For all the others species
                temp.nameSpecies=l_s[1].strip('\n')              # Adding the name species, type species and mass species to the lists
            
                l_t=lines[index+1].split(':')
                temp.typeSpecies=l_t[1].strip('\n')
            
                l_m=lines[index+2].split(':')
                temp.massSpecies=l_m[1].strip('\n')
            
                if 'NEUTRAL' in l_t[1] :                        # For the neutral type species
                                                                # Adding sigma, epsilon_k and coeff_diff to the lists
                    l_sig=lines[index+3].split(':')
                    temp.sigmaSpecies=l_sig[1].strip('\n')
                
                    l_ep=lines[index+4].split(':')
                    temp.epsilon_kSpecies=l_ep[1].strip('\n')
                
                    l_c=lines[index+5].split(':')
                    temp.coeff_diffSpecies=l_c[1].strip('\n')
              
            if temp.nameSpecies=='ANY_NEUTRAL':                 # Translation of 'ANY_NEUTRAL' name to 'M' (just a convention)
                temp.nameSpecies='M'
                     
                
                # Others than neutral type species don't have sigma, epsilon_k and coeff_diff attributes

            species.append(temp)   # Adding the temporary species object created with its attributes to the list 
                    
        if ('REACTION:') in lines[index]:
                                                   
            l_reaction=lines[index].split(':')            # l_reaction is a list composed of a splited line, used to collect the chemical reaction equation
            l_reaction[1]=l_reaction[1].strip('\n')
            
            l_reaction[1]=l_reaction[1].replace('ANY_NEUTRAL', 'M')   # Translation of 'ANY_NEUTRAL' name to 'M' (just a convention)
                       
                    
            if ('@') in lines[index]:                     # if there is '@' in the reaction equation (corresponding to one of the possibles formats for the file)
                
                               
                c=0
                while lines[index+2+c][0] !='@':                
                    c+=1                            # This is used to have c, with index+2+c the first line of @ data (The order should normally be @A, @B, etc.., @K)
               
                at_counter_reaction=0               # at_counter_reaction is the number of different @ in the reaction equation
                x=0                                 # here, it counts the differents @ given after the reaction line, but if there is @K we need to subtract 1 to at_counter_reaction
                while lines[index+2+c+x][0] == '@':         
                    at_counter_reaction+=1
                    x+=1                            # If the files are always formatted the same way, the while loops in the program should not be infinite
                if ('@') in lines[index+1]:
                    at_counter_reaction-=1
                    
                    
                multi_number=(len( ((lines[index+2+c].split('= '))[1]).split(" ")) )
                # multi_number is the number of possibility for @
                                                          
                l_eq_reaction=l_reaction[1].split('=')    # l_eq_reaction is a list composed of a splited line, used to collect the left part (reagents) and the right part (products) of the chemical reaction
    
                l_reagents=l_eq_reaction[0].split('+')    # l_reagents is a list composed of a splited line, containing the reagents of the reaction
    
                l_products=l_eq_reaction[1].split('+')    # l_products is a list composed of a splited line, containing the products of the reaction
                l_products[-1]=l_products[-1].strip('\n') # Removing '\n' to the last item of l_products, because as it is at the end of a line in the data file, it is followed by an invisible '\n' 

                l_k=lines[index+1].split(':')             # l_k is a list composed of a splited line, used to collect the k constant
                                                          # Then k=l_k[1]  
                    
                for p in range(len(l_reagents)):
                    l_reagents[p]=l_reagents[p].strip('\n')         # Removing the '\n' that could appear int the strings for the reagents, products and k
                        
                for p in range(len(l_products)):
                    l_products[p]=l_products[p].strip('\n')
                    
                l_k[1]=l_k[1].strip('\n')
                
                ###############################################
                
                # If there is a stoichiometric coefficient in front of a species in the regeants or products like '2N2', '12O2' (we assume it can be > 10)
                # We need to create a new list for the products or reagents without stoichiometric coefficient, where the species with stoichiometric coefficient are appearing multiple times

                # Reagents

                new_l_reagents=[]                                      # List where the species will be added, without stoichiometric coefficient            
                
                for s in range(len(l_reagents)):                       # Iterations on the species of the reagents list 
                
                # string[:f] is giving a string with only the characters from 0 to f-1 included
                # string[f:] is giving a string with only the characters from f (included) to the last character included
                
                    if l_reagents[s][0].isdigit()==True:               # If the first character of the name species is a number
                    
                        f=1                                            # f is the first character that is not a number on the string character of the name species, so the stoichiometric coefficient will be in the characters from 0 to f-1
                                                                       # So if the first character (index 0) of the name species is a number, we have to initialize f to 1
      
                        while l_reagents[s][f].isdigit==True:          # We know that the charachter f-1 is a number, so while the character f is a number, we add 1 to f                  
                            f+=1                                       # the While loop will stop when the character f is not a number
                            
                        c=int(l_reagents[s][:f])                       # l_reagents[s][:f] is a string containing only the stoichiometric coefficient (a number). Doing c=int() allow us to convert the string into a number, that can be used as a variable 

                        for i in range(c):                             # Now that we have c, the stoichiometric coefficient, we append c times the species (l_reagents[s][f:], so without the stoichiometric coefficient) to the new list
                            new_l_reagents.append(l_reagents[s][f:])
                                
                    else:                                             # If there is not a number at the beginning of the name species  
                        new_l_reagents.append(l_reagents[s])          # We add the species to the new list  
        
                l_reagents=copy.deepcopy(new_l_reagents)              # Reagents list is the new reagents list


                # Products                

                new_l_products=[]                                       # We do exactly the same for the species in the products list
                
                for s in range(len(l_products)):
                    f=1
                    if l_products[s][0].isdigit()==True:
                        while l_products[s][f].isdigit==True:
                            f+=1
                        c=int(l_products[s][:f])
                        for i in range(c):
                            new_l_products.append(l_products[s][f:])
                                
                    else:
                        new_l_products.append(l_products[s])
        
                l_products=copy.deepcopy(new_l_products)
                
                ###############################################
                                
                for d in range(multi_number):       # Loop on the number of possibility for @
                                                    # At each iteration, we will instance a new reaction
                    
                    l_temp_r=copy.deepcopy(l_reagents)         # We use deepcopy instead of a simple "=", because "=" will just create a link between the two lists, and if we modify one list, the other will be also modified
                    l_temp_p=copy.deepcopy(l_products)         # If we don't do this way, the @ of the products and reagents lists will be remplaced during the first iteration, and during the other iteration the program will not detect @ in the reaction equation (so it will create d times the same reaction)
                    l_temp_k=copy.deepcopy(l_k[1])    

                                                    
                    # Reagents
                    
                    for h in range(len(l_reagents)):           # Replacing '@' in the reagents part of the reaction with the corresponding species in the @ line
                        if ('@') in l_reagents[h]:
                            g=0
                            while l_reagents[h] != lines[index+2+c+g].split('= ')[0]: # if '@x' in the reagents, Searching the line beginning by '@x' to then find the species
                                g+=1
                            l_temp_r[h]=(((lines[index+2+c+g].split('= '))[1]).split(" "))[d].strip('\n')
                            
                    f=0
                    while f < len(l_temp_r):                # Sometimes in the species possibilities for an @, there are things like 'N2+N2'
                        if ('+') in l_temp_r[f]:            # But in the reagents list we need to have one species by character string
                            a=l_temp_r[f].split('+')        # So here we are replacing 'N2+N2' by 'N2', 'N2'
                            l_temp_r.remove(l_temp_r[f])        
                            b=0
                            for e in range(len(a)):
                                l_temp_r.insert(f+b,a[e])
                                b+=1
                        f+=1
                                                 
                    # Products
                    
                    for h in range(len(l_products)):           # Replacing '@' in the products part of the reaction with the corresponding species in the @ line
                        if ('@') in l_products[h]:
                            g=0
                            while l_products[h] != lines[index+2+c+g].split('= ')[0]: # if '@x' in the products, Searching the line beginning by '@x' to then find the species
                                g+=1                           
                            l_temp_p[h]=(((lines[index+2+c+g].split('= '))[1]).split(" "))[d].strip('\n')

                    f=0
                    while f < len(l_temp_p):                # Sometimes in the species possibilities for an @, there are things like 'N2+N2'
                        if ('+') in l_temp_p[f]:            # But in the products list we need to have one species by character string
                            a=l_temp_p[f].split('+')        # So here we are replacing 'N2+N2' by 'N2', 'N2'
                            l_temp_p.remove(l_temp_p[f])        
                            b=0
                            for e in range(len(a)):
                                l_temp_p.insert(f+b,a[e])
                                b+=1
                        f+=1
                    
                                     
                    
                    if ('@K') in l_k[1]:                            # Replacing @K with the corresponding value given on the line beginning by '@K'
                        l_k_at=lines[index+2+c+at_counter_reaction].split("= ")[1].split(" ")
                        l_temp_k=l_k[1].replace("@K", l_k_at[d].strip('\n'))                        
                    
                    for p in range(len(l_temp_r)):                  # Removing the '\n' that could appear int the strings for the reagents, products and k
                        l_temp_r[p]=l_temp_r[p].strip('\n')
                        
                    for p in range(len(l_temp_p)):
                        l_temp_p[p]=l_temp_p[p].strip('\n')
                    
                    l_temp_k=l_temp_k.strip('\n')
                    

                    temp_r_string=''                              # To instance a reaction class we need the reaction equation (not used after to write on the java file, just used as an attribute, so a little different from the formula written on the java file)
                    temp_r_string+=l_temp_r[0]                    # As we replaced the @ by the corresponding species, we need to write again the reaction equation without @
                   
                    for v in range(1, len(l_temp_r)):             # Here we are doing the reagents part
                        temp_r_string+=f'+{l_temp_r[v]}'
                                                            
                    temp_p_string=''                              # Here we are doing the products part
                    temp_p_string+=l_temp_p[0]
                    for v in range(1, len(l_temp_p)):
                        temp_p_string+=f'+{l_temp_p[v]}'
                        
                    l_reaction[1]=f'{temp_r_string}={temp_p_string}'  # The new equation reaction 
                    
                    
                    if ('M') in l_reaction[1]:     # If 'M' is in the reaction , corresponding to 'ANY_NEUTRAL' species, we need to create two reactions with N2 and O2 replacing 'M'
                        
                        # Replacing 'M' with 'N2'
                    
                        l_temp_r_M=copy.deepcopy(l_temp_r)      # We use deepcopy instead of a simple "=", because "=" will just create a link between the two lists, and if we modify one list, the other will be also modified
                        l_temp_p_M=copy.deepcopy(l_temp_p)      # If we don't do this way, we will replace 'M' with 'N2' and then, when searching to replace 'M' with 'O2', we will not find 'M'
                        
                        
                        l_reaction_M=l_reaction[1].replace('M', 'N2')    # Creation of new lists for the reaction equation, the reagents and products lists
                        for m in range(len(l_temp_r)):                   # Replacing 'M' with 'N2' for each of them   
                            l_temp_r_M[m]=l_temp_r[m].replace('M', 'N2')
                        for m in range(len(l_temp_p)):
                            l_temp_p_M[m]=l_temp_p[m].replace('M', 'N2')
                        
                        # Instantiation of a temporary reaction object with theses lists
                        temp=Reaction(l_reaction_M.strip('\n'), l_temp_r_M, l_temp_p_M, l_temp_k.strip('\n'))
                        reactions.append(temp)
                        # Adding the temporary reaction object created  to the list
                        
                        # Replacing 'M' with 'O2'

                        l_temp_r_M=copy.deepcopy(l_temp_r)      # Doing exactly the same as we did just before, but with O2 instead of N2
                        l_temp_p_M=copy.deepcopy(l_temp_p)

                        l_reaction_M=l_reaction[1].replace('M', 'O2')
                        for m in range(len(l_temp_r)):
                            l_temp_r_M[m]=l_temp_r[m].replace('M', 'O2')
                        for m in range(len(l_temp_p)):
                            l_temp_p_M[m]=l_temp_p[m].replace('M', 'O2')
                        
                        temp=Reaction(l_reaction_M.strip('\n'), l_temp_r_M, l_temp_p_M, l_temp_k.strip('\n'))
                        reactions.append(temp)                    

                    else:  # If there is not 'M' in the reaction, we juste creation a new temporary reaction object with the data collected
                        
                        temp=Reaction(l_reaction[1].strip('\n'), l_temp_r, l_temp_p, l_temp_k.strip('\n')) 
                        
                        # Instantiation of a temporary reaction object to collect data from the file at each iteration
                        # .strip('\n') is used as before to remove the invisible '\n' from the original data file
                        
                        reactions.append(temp)    # Adding the temporary reaction object created with its attributes to the list
                                                                                                                         
                
            else : # if there is'nt '@' in the reaction equation (corresponding to one of the possibles formats for the file)
                
                l_eq_reaction=l_reaction[1].split('=')    # l_eq_reaction is a list composed of a splited line, used to collect the left part (reagents) and the right part (products) of the chemical reaction
        
                l_reagents=l_eq_reaction[0].split('+')    # l_reagents is a list composed of a splited line, containing the reagents of the reaction
        
                l_products=l_eq_reaction[1].split('+')    # l_products is a list composed of a splited line, containing the products of the reaction
                l_products[-1]=l_products[-1].strip('\n') # Removing '\n' to the last item of l_products, because as it is at the end of a line in the data file, it is followed by an invisible '\n' 
                        
                l_k=lines[index+1].split(':')                 # l_k is a list composed of a splited line, used to collect the k constant

                l_k[1].strip('\n')                            # Then k=l_k[1]                                             

               
                if ('M') in l_reaction[1]:                  # If 'M' is in the reaction , corresponding to 'ANY_NEUTRAL' species, we need to create two reactions with N2 and O2 replacing 'M'
                    
                    # Replacing 'M' with 'N2'
                
                    l_temp_r_M=copy.deepcopy(l_reagents)    # We use deepcopy instead of a simple "=", because "=" will just create a link between the two lists, and if we modify one list, the other will be also modified
                    l_temp_p_M=copy.deepcopy(l_products)    # If we don't do this way, we will replace 'M' with 'N2' and then, when searching to replace 'M' with 'O2', we will not find 'M'
                    
                    l_reaction_M=l_reaction[1].replace('M', 'N2')           # Creation of new lists for the reaction equation, the reagents and products lists
                    for m in range(len(l_reagents)):                        # Replacing 'M' with 'N2' for each of them
                        l_temp_r_M[m]=l_reagents[m].replace('M', 'N2')
                    for m in range(len(l_products)):
                        l_temp_p_M[m]=l_products[m].replace('M', 'N2')
                    
                    # Instantiation of a temporary reaction object with theses lists
                    temp=Reaction(l_reaction_M.strip('\n'), l_temp_r_M, l_temp_p_M, l_temp_k.strip('\n'))
                    reactions.append(temp)
                    # Adding the temporary reaction object created  to the list
                    
                    # Replacing 'M' with 'O2'
                    
                    l_temp_r_M=copy.deepcopy(l_reagents)    # Doing exactly the same as we did just before, but with O2 instead of N2
                    l_temp_p_M=copy.deepcopy(l_products)

                    l_reaction_M=l_reaction[1].replace('M', 'O2')
                    for m in range(len(l_reagents)):
                        l_temp_r_M[m]=l_reagents[m].replace('M', 'O2')
                    for m in range(len(l_products)):
                        l_temp_p_M[m]=l_products[m].replace('M', 'O2')
                    
                    temp=Reaction(l_reaction_M.strip('\n'), l_temp_r_M, l_temp_p_M, l_temp_k.strip('\n'))
                    reactions.append(temp)                
                
                
                else:   # If there is not 'M' in the reaction, we juste creation a new temporary reaction object with the data collected
                    
                    temp=Reaction(l_reaction[1].strip('\n'), l_reagents, l_products, l_k[1]) 
                    # Instantiation of a temporary reaction object to collect data from the file at each iteration
                    # .strip('\n') is used as before to remove the invisible '\n' from the original data file
                    
                    reactions.append(temp)                    # Adding the temporary reaction object created with its attributes to the list
    
    
fi.close()    # .close() used to close the file to be able to modify it outside of python



####################################################################
'''
CLASSES INSTANTIATION AND METHODS TESTS
'''

'''                        
Species class methods test
'''        

# species[0].readSpecies()    # Reading test
# species[42].readSpecies()
# species[79].readSpecies()


'''
SpeciesList class instantiation and methods test
'''

sL=SpeciesList(species)   # Instantiation

# sL.readSpeciesList()
# sL.verifSpecies()       # Test SpeciesList class
# sL.verifNoCoeffSpecies()



'''                        
Reactions class methods test
'''        

# reactions[0].readReaction()    # Reading test
# reactions[42].readReaction()
# reactions[651].readReaction()


'''
ReactionsList class instantiation and methods test
'''

rL=ReactionsList(reactions)  # Instantiation

# rL.readReactionsList()
# rL.verifEqReaction()       # Test SpeciesList class
                

####################################################################
'''
CREATION OF THE JAVA FILE FOR COMSOL
'''

# Writing the base of the file and adding species and their attributes to the file, according to the file format accepted by Comsol
# before_v2.txt file is needed

with open("before_v2.txt") as f_b:              # Open before_v2.txt
    lines_b=f_b.readlines()                     # Creation of lines_b, a list containing the lines of before_v2.txt
f_b.close()

f= open("species_and_reactions.java","w")         # Creation of species_for_comsol.java
f.write('')                                       # w opens a file for writing only. Overwrites the file if the file exists. If the file does not exist, creates a new file for writing.
# Writing '' to be sure to have an empty file
f.close()
# .close() are important, forgetting them can cause unwanted things when writing on files

for i in range (len((lines_b))):
    f= open("species_and_reactions.java","a")      # a opens a file for appending
    f.write(lines_b[i])                            # Writing before_v2.txt to the Java file
    f.close()


sL.writeSpecies()   # Writing the species and their attributes to the Java file according to the format needed    

rL.writeReactions() # Writing the reactions and their attributes to the Java file according to the format needed

   

f.close()                               

####################################################################

            
                
                

                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
            
        