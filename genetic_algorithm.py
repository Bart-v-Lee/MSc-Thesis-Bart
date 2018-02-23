#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 13:13:43 2017

@author: Bart van der Lee
@project: MSc thesis 
"""
import pandas as pd
import numpy as np
import crenellation
import sys

class Population:
    """A set of solutions, in GA terms a " Population of individuals". A population has the following attributes:
        
    Attributes:
        N_pop = an integer representing the population size, or number of inidividuals in the population
        Statistics = a collection of statistics describing the population, such a fitess mean, std devation, max fitness, min fitness
    
    """
    
    def __init__(self, N_pop): #object or instance variables 

        self.N_pop = N_pop

    def InitializePopulation(NumberOfContainers, delta_a, W, N_pop, t_dict, SeedSettings, SeedNumber, Constraints): #previous initialize_population
        """
        Initializes a population of individuals of size N_pop, either through random or by pre-determined choice (e.g. a seed design). Depending on the SeedSettings, a number of 
        pre-designed solutions are scaled to the given boundary conditions (delta_x, W) and inserted in the initial population. The remaining individuals are sampled randomly from
        the solution space. 
        """
        
#        pop_size = int(bc.ix["Population size"])
#        array = np.zeros((pop_size,7))
#        index = range(1,pop_size+1)
#        list = {"Original Indi. No","Fitness", "Chromosome", "Cren Design", "Balance", "Lower Bound", "Upper Bound"}
#        population_matrix = pd.DataFrame(data=array, index = index, columns = list, dtype = 'object')
        
        """
        Import empty population dataframe
        """
        import database_connection
        PopulationInitial = database_connection.Database.RetrievePopulationDataframe(N_pop)

        """
        Determine whether to import any seed design into the initial population. If True, then chooses a solution number within the population which will become the seed solution.
        """

        if SeedSettings == True:
            IndividualNumberSeed = np.random.randint(1,N_pop+1)
        else:
            IndividualNumberSeed = None
            
        """
        Fill the initial population with solutions 
        """
            
        import crenellation
        
        for IndividualNumber in range(1,N_pop+1):
        
            if  IndividualNumber == IndividualNumberSeed:
                PopulationInitial.Chromosome[IndividualNumber] = crenellation.CrenellationPattern.ConstructChromosomeSeed(SeedNumber,delta_a,W,t_dict, Constraints)
        
            else:
                PopulationInitial.Chromosome[IndividualNumber] = crenellation.CrenellationPattern.ConstructChromosomeRandom(NumberOfContainers,delta_a, W, t_dict, Constraints)
                
       
        return PopulationInitial
        
        
        def CalculateDiversity():
            """
            Calculates the measure of diversity for a population based on the unique features present in the entire population
            """
            pass
        
        def CalculatePopulationStatistics():
            """
            Calculates the main statistics of the population based on its individuals. These main statistics are:
                
            Main population statistics:
                1. Mean fitness
                2. Standard deviation of fitness
                3. Max fitness
                4. Min fitness
            """
            pass
       


class GeneticAlgorithm:
    """
    A genetic algorithm with the following parameters.
    
    Parameters:
        1. Crossover rate Pc
        2. Mutation rate Pm
        3. Selection rate Rs
    """

    def __init__(self, Pc, Pm, Rs):
        self.Pc = Pc
        self.Pm = Pm
        self.Rs = Rs
        
    """           
    #==============================================================================
    #     Step 2. Evaluate the fitness function
    #==============================================================================
    """         
        
        
    def EvaluateFitnessFunction(Fitness_Function_ID,Chromosome, S_max,a_0, a_max, Delta_a,C,m):
        """
        Main method used for evaluating the objective function, or in GA terms "fitness function".
        Since the objective function can change depending on the experiment, this method chooses the right one
        Furthermore it shows on overview of the equations for each objective function
        """

        import fatigue
        
        if Fitness_Function_ID == "Set 1":
            
            FatigueLife, FatigueCalculations = fatigue.FatigueCalculations.CalculateFatigueLife(Chromosome, S_max, a_0, a_max, Delta_a, C, m)
            
            """
            The Fitness value is the unscaled, fatigue life of the solution in fatigue cycles [N]
            """
            
            FitnessValue = FatigueLife 
            
            
        elif Fitness_Function_ID == "Set 2":
            
            pass
            
            
        elif Fitness_Function_ID == "Set 3":
            
            pass
        
        else:
            pass
        
        
        return FitnessValue
        
        
        
    """           
    #==============================================================================
    #     Step 3. Select the fittest solutions
    #==============================================================================
    """     
        
        
    def SelectSurvivingPopulation(PopulationCurrent, Rs):
        """
        Selects the highest scoring solutions based on fitness. The number of solutions selected is determined by the population size N_pop and the selection rate Rs.
        """

        # Step 1. Rank individuals based on fitness values
        
        PopulationCurrentRanked = PopulationCurrent.sort_values("Fitness",ascending=False, kind='mergesort')
        
        # Step 2. Select the top individuals based on the given selection rate Rs
        
        NumberOfSurvivors = int(len(PopulationCurrentRanked) * Rs)
        PopulationCurrentSelected = PopulationCurrentRanked[:NumberOfSurvivors]
        
        return PopulationCurrentSelected
        
            
    """           
    #==============================================================================
    #     Step 4. Determine probability of reproduction for each solution
    #==============================================================================
    """
    
    def CalculateReproductionProbParents(PopulationCurrentSelected, RankingMethod):
        """
        Choose selection method of parents based on condition provided in the boundary conditions bc
        """
        
        import genetic_algorithm
    
        if RankingMethod == 'Relative Fitness Rank':
            SelectionProbParents = genetic_algorithm.GeneticAlgorithm.RelativeRank(PopulationCurrentSelected)
            
        elif RankingMethod == 'Relative Fitness':
            SelectionProbParents = genetic_algorithm.GeneticAlgorithm.RelativeFitness(PopulationCurrentSelected)

        elif RankingMethod == 'Inverse Rank':
            SelectionProbParents = genetic_algorithm.GeneticAlgorithm.RelativeRankInverse()
            
        elif RankingMethod == 'Tournament': #not developed yet at this point
            SelectionProbParents = genetic_algorithm.GeneticAlgorithm.Tournament()
            
    
        return SelectionProbParents


    def RelativeFitness(PopulationCurrentSelected): 
        """
        Output: Probability Distribution for Selection of a specific Solution as a Parent, based on its relative fitness value amongst other solutions in the population.
        """
        N_pop_selected = len(PopulationCurrentSelected)
            
        PopulationCurrentSelected.index = range(1,N_pop_selected+1)

        PopulationCurrentSelected["Pp"] = (N_pop_selected - PopulationCurrentSelected.index + 1) / (sum(range(1,N_pop_selected+1)))
        PopulationCurrentSelected["Pp Cumulative"] = PopulationCurrentSelected["Pp"].cumsum()

        return PopulationCurrentSelected
        
    def RelativeRank(PopulationCurrentSelected): #previously fitness_ranking_method
        """
        Output: Probability Distribution for Selection of a specific Solution as a Parent, based on its relative fitness rank amongst other solutions in the population.
        """
    
        
#        selection_rate = bc.ix["Selection Rate"]
#        pop_size = int(bc.ix["Population size"])
#        population_ranked = population_eval.sort_values("Fitness",ascending=False, kind='mergesort')
#        cut_off_position = int(selection_rate * pop_size)
#        population_selected = population_ranked[:cut_off_position]
    
        return PopulationParents
    
    def RelativeRankInverse(): #previously inverse_ranking_method
        """
        Output: Probability Distribution for Selection of a specific Solution as a Parent, based on its relative fitness inverse rank amongst other solutions in the population.
        """
        
        selection_rate = bc.ix["Selection Rate"]
        pop_size = int(bc.ix["Population size"])
        population_ranked = population_eval.sort_values("Fitness",ascending=True, kind='mergesort')
        cut_off_position = int(selection_rate * pop_size)
        population_selected = population_ranked[:cut_off_position]
        
        population_selected = population_selected.sort_values("Fitness", ascending=False, kind = 'mergesort')
        
        return population_selected
        
        
    def Tournament():
        pass
   
    """
    #==============================================================================
    #           5. Select the Parents for Recombination
    #==============================================================================
    """  
    
    def SelectParents(PopulationParents): # previously pair_parents
        """
        This method selects (two) parents for the reproduction, based on the probability distribution for the solutions being chosen as a parent
        """
        ParentIndex1 = 0
        ParentIndex2 = 0
        
        while ParentIndex1 == ParentIndex2:
        
            """
            Picks a float value between 0.0 and 1.0
            """
            PairIndex1 = np.random.uniform(0.0,1.0)
            PairIndex2 = np.random.uniform(0.0,1.0)
            """
            Looks up the chosen first individual in the cumulative probability distribution of all parent individuals
            """
            number_of_true = PopulationParents["Pp Cumulative"][PopulationParents["Pp Cumulative"]>= PairIndex1].count()
            ParentIndex1 = (len(PopulationParents) - number_of_true)+1
            """
            Looks up the chosen second individual in the cumulative probability distribution of all parent individuals
            """
            number_of_true = PopulationParents["Pp Cumulative"][PopulationParents["Pp Cumulative"]>= PairIndex2].count()
            ParentIndex2 = (len(PopulationParents) - number_of_true)+1
            
            """
            Returns the index of the chosen parent in the parent population if they are not the same solution
            """
        
    
        return ParentIndex1, ParentIndex2
        
    """
    #==============================================================================
    #           6. Crossover of selected parent solutions
    #==============================================================================
    """  
    def RecombineParents(Parent1, Parent2, PopulationOffspring, Pc, W, CrossoverOperator, Constraints, NumberOfContainers): #previously recombination
        """
        Determine whether the Offspring is created by crossover or that the parents are passed into the OffspringPopulation without any crossover. 
        Crossover happens with a probability of Pc 
        If crossover takes places, the crossover method is chosen based on the boundary condition CrossoverOperator
        """
        
        CrossoverRandomGenerator = np.random.uniform(0.0,1.0)

        if CrossoverRandomGenerator < Pc:
            print("Crossover taking place...")
            # Select how solutions are recombined based on the boundary condition CrossoverOperator
            
            import genetic_algorithm
    
            if CrossoverOperator == "Set 1":
                Child1, Child2 = genetic_algorithm.GeneticAlgorithm.CrossoverSinglePoint(Parent1, Parent2, PopulationOffspring, W, NumberOfContainers, Constraints)
                
            elif CrossoverOperator == "Set 2":
                PopulationOffspring  = genetic_algorithm.uniform_cross_over()
                
            elif CrossoverOperator == "Set 3":
                PopulationOffspring  = genetic_algorithm.initialize_population()
                
            elif CrossoverOperator == "Set 4":
                PopulationOffspring  = genetic_algorithm.redistribution()
                
            else:
                pass
            
            #insert both children into the OffspringPopulation
            
            for i in range(1,len(PopulationOffspring)):
                
                if PopulationOffspring.Chromosome[i] is None: # gives error when first individuals have been place, solve!
                
                    PopulationOffspring.Chromosome[i] = Child1
                    PopulationOffspring.Chromosome[i+1] = Child2
                    break
            

        else:
            #insert both parents into the OffspringPopulation
            for i in range(1,len(PopulationOffspring)):
                
                print(i)
                if PopulationOffspring.Chromosome[i] is None:

                    PopulationOffspring.Chromosome[i] = Parent1
                    PopulationOffspring.Chromosome[i+1] = Parent2
                    break
                    
        return PopulationOffspring
        
    """
    #==============================================================================
    #                        Cross over methods
    #==============================================================================
    """    

    def CrossoverSinglePoint(Parent1, Parent2, PopulationOffspring, W, NumberOfContainers, Constraints): #previously single_point_crossover
        """
        This method recombines the chromosomes of two parent solutions using the principles of single point crossover
        """

        
        if Constraints.Plate_Symmetry[0] == str(True):    #only consider the first half of the containers for the crossover

            """
            Only considers half of the containers for crossover, as the plate has to be symmetric
            """
            # Choose the crossover point randomly
            
            NumberOfCrossoverPoints = NumberOfContainers-1
            CrossoverPoint = int(np.random.choice(NumberOfCrossoverPoints,1))+1
            HalfChromosome = int(0.5*W)
            
            # Translate the crossover point to a point in the array of the chromosome calculating delta_x as the container width
            
            Delta_x = ((0.5*W) / NumberOfContainers) #0.5 because of the symmetry constraint
            
            # Exchange the chromosomes between both parents

            Child1Left = np.append(Parent1.Thickness[:int(CrossoverPoint*Delta_x)], Parent2.Thickness[int(CrossoverPoint*Delta_x):HalfChromosome])                # left side of Parent1 and right side of Parent2
            Child2Left = np.append(Parent2.Thickness[:int(CrossoverPoint*Delta_x)], Parent1.Thickness[int(CrossoverPoint*Delta_x):HalfChromosome])                # left side of Parent2 and right side of Parent1
            
            Child1Chromosome = np.append(Child1Left,np.flipud(Child1Left))
            Child2Chromosome = np.append(Child2Left,np.flipud(Child2Left))
            
            import database_connection
            Child1 = database_connection.Database.RetrieveChromosomeDataframe() #empty chromosome dataframes
            Child2 = database_connection.Database.RetrieveChromosomeDataframe()
            
            # Place Children in Chromsome dataframes
            
            Child1.Thickness = Child1Chromosome
            Child2.Thickness = Child2Chromosome
            Width = np.linspace(1,W, W)
            Child1.Width = Width
            Child2.Width = Width
            
            return Child1, Child2
        
    
    def CrossoverUniform(self):
        pass
    
    def CrossoverAddition(self, bc, population_children, population_parents): #previously addition_crossover
        """
        Currently not in use
        """
        
        t_ref = bc.ix["Reference thickness"]
        pop_size = bc.ix["Population size"]
        output_children_per_couple = 1
        number_of_children = pop_size #- np.count_nonzero(population_children["Chromosome"])
        number_of_couples = int(number_of_children / output_children_per_couple)
        chromosome_half_length = int(len(population_parents["Chromosome"][1])/2)
        
        for i in range(1,number_of_couples+1):
            
            parent_1_index = genetic_algorithm.pair_parents(self, bc,population_parents)
            parent_2_index = genetic_algorithm.pair_parents(self, bc,population_parents)
            
            while parent_1_index == parent_2_index:
                parent_2_index = genetic_algorithm.pair_parents(self, bc,population_parents)
            
            parent_1 = population_parents["Chromosome"][parent_1_index][:]
            parent_2 = population_parents["Chromosome"][parent_2_index][:]
            child_1_chromosome = (parent_1 + parent_2) / 2
            """
            Calculate and apply the rebalancing of the new chromosome
            """
            population_children["Chromosome"][i] = child_1_chromosome
        
        return population_children
        
        
    def cross_over(self, bc, material, population_selected):
        
        elitism_settings = bc.ix["Elitism"]
        
        if elitism_settings == "True":
            population_children, number_of_elites = genetic_algorithm.apply_elites(self,bc,population_selected)
            print("Elitism has been used")
            
        elif elitism_settings == "Inverse":
            population_children = genetic_algorithm.apply_elites_inverse(self,bc,population_selected)
            
        else:
            population_children = genetic_algorithm.children_population(self, bc)
            number_of_elites = 0
        
        cross_over_method = bc.ix["Cross-over Method"]
        population_parents = population_selected
        population_parents = genetic_algorithm.pairing_probability(self, bc, population_children, population_parents)
        
        if cross_over_method == "Single Point":
            population_children = genetic_algorithm.single_point_crossover(self, bc, population_children, population_parents)
        
        elif cross_over_method == "Addition":
            population_children = genetic_algorithm.addition_crossover(self, bc, population_children, population_parents)

        return population_children, number_of_elites


        
    """
    #==============================================================================
    #                      7. Mutation of Offspring population  
    #==============================================================================
    """
    
    def MutatePopulation(Chromosome, MutationOperator, Pm, NumberOfContainers, W, t_dict, Constraints):
        """
        This method outputs a mutated chromosome of a single solution, in GA terms "chromosome", whose chromosome has been mutated. 
        Mutation can be performed in different ways, which is determined by the chosen MutationOperator.
        For each way of mutating, a different method has been made.
        """
        
        import genetic_algorithm
        
        # Apply the given constraints to the mutation operations
        
        if Constraints.Plate_Symmetry[0] == str(True):
            
            # Calculate the number of variable containers and their container width delta_x
            
            NumberOfContainersSymmetry = int(0.5 * NumberOfContainers)
            delta_x = int((0.5*W) / NumberOfContainersSymmetry)
        
            NumberOfContainers =  NumberOfContainersSymmetry
            
        else:
            delta_x = int(W / NumberOfContainers)

        
        if MutationOperator == "Set 1":
            ChromosomeMutated = genetic_algorithm.GeneticAlgorithm.MutateRandom(Chromosome, Pm, NumberOfContainers, W, t_dict, delta_x, Constraints)
            
        elif MutationOperator == "Set 2":
            ChromosomeMutated = genetic_algorithm.GeneticAlgorithm.MutateSwap()
        
        elif MutationOperator == "Set 3":
            ChromosomeMutated = genetic_algorithm.GeneticAlgorithm.mutate_swap_ref_5_10cont_8thick()

        else:
            pass
        
        return ChromosomeMutated
        
            
    def MutateRandom(Chromosome, Pm, NumberOfContainers, W, t_dict, delta_x, Constraints):
        """
        This method mutates provided Chromosome.
        Each container has a probability to mutate to another thickness of Pm.
        """
        # Calculate the number of features (in the case of crenellation, container thicknesses) will be mutated. 
        # This depends on the NumberOfContainers, the population size and the Mutation Rate Pm.

        # Loop through containers in the chromosome
                    
        for ContainerNumber in range(1,NumberOfContainers+1):
            
            # Determine whether mutation of the container thickness will take place 
            
            MutationRandomGenerator = np.random.uniform(0.0,1.0)
            
            if MutationRandomGenerator < Pm:
                print("Mutation took place")
                
                # Retrieve the current container thickness

                CurrentContainerThickness = Chromosome.Thickness[(ContainerNumber*delta_x)]
                
                # Randomly choose another thickness from the thickness dictionary t_dict
                
                MutatedContainerThickness = CurrentContainerThickness 
                
                while MutatedContainerThickness == CurrentContainerThickness:
                    
                    NumberOfThicknesses = np.arange(0,len(t_dict))
                    MutatedContainerThicknessIndex = str(np.random.choice(NumberOfThicknesses))
                    MutatedContainerThickness = float(t_dict[MutatedContainerThicknessIndex])
                    
                # Change the container thickness to the mutated thickness in the chromosome
                
                Chromosome.Thickness[(ContainerNumber-1)*delta_x : ContainerNumber*delta_x] = MutatedContainerThickness
                
                # If the symmetry condition is true, mirror the change to the other symmetrical half of the chromosome
                
                if Constraints.Plate_Symmetry[0] == str(True):
                
                    ChromosomeLeft = Chromosome.Thickness[:(NumberOfContainers*delta_x)]
                    ChromosomeRight = np.flipud(ChromosomeLeft)
                    
                    Chromosome.Thickness[(NumberOfContainers*delta_x):] = ChromosomeRight
                
            else:
                continue
                
        return Chromosome

    def MutateSwap(self, bc, population_children, number_of_elites):
        """
        Mutation through swapping of material for highly refined crenellation patterns. Only review if necessary.
        """
        t_ref = bc.ix["Reference thickness"]
        pop_size = bc.ix["Population size"]
        mutation_rate = bc.ix["Mutation Rate"]
        chromosome_length = int(len(population_children["Chromosome"][1])/2)
        number_of_mutations = int(mutation_rate * pop_size * chromosome_length)  #subtract the elites
        total_locations = int(pop_size * chromosome_length)
        
        mutation_locations = np.random.randint(0,total_locations, number_of_mutations)
        
        #print("Starting mutation of children")
        for i in range(0,number_of_mutations):
            """
            Pick one of the mutation locations and find the respective chromosome
            """
            individual_no = int(np.floor(mutation_locations[i] / chromosome_length))
            individual_location = mutation_locations[i] - int(individual_no * chromosome_length)
            individual_chromosome = population_children["Chromosome"][individual_no+1]
            """
            Swap thickness with another location in the chromosome
            """
            individual_chromosome = crenellation.swap_thickness_mutation(self, individual_chromosome, individual_location, bc)
            """
            """
            individual_chromosome_left_half = individual_chromosome[:chromosome_length]
            individual_chromosome = np.append(individual_chromosome_left_half,np.flipud(individual_chromosome_left_half))
            """
            Insert mutated chromosome back into the population
            """
            population_children["Chromosome"][individual_no+1] = individual_chromosome
            
        return population_children

    def mutate_swap_ref_5_10cont_8thick(self, bc, population_children, number_of_elites):
        """
        Mutate through swapping material between containers for crenellation patterns from reference paper. 
        """
        
        #print(population_children)
        t_ref = bc.ix["Reference thickness"]
        delta_t_min = bc.ix["Layer thickness"]
        mutation_rate = bc.ix["Mutation Rate"]
        number_of_containers = bc.ix["number_of_containers"]
        population_size = bc.ix["Population size"]
        half_width = bc.ix["Width"]/2
        area_ref = t_ref * half_width
        container_width = (half_width /2) / number_of_containers
        number_of_mutations = int(number_of_containers * population_size * mutation_rate)
        thickness_dict = {0: 1.9 ,1: 2.22 , 2: 2.54, 3: 2.86, 4: 3.19, 5: 3.51, 6: 3.83, 7:4.15}

        """
        Choose which containers should be mutated, and mutate them by the minimum thickness level. Direction is chosen randomly uniform.
        """
        for i in range(1, number_of_mutations):
            mutate_location = int(np.random.choice(np.arange(1,population_size*number_of_containers)))
            individual_number = int(np.ceil(mutate_location / number_of_containers))
            area_chromosome_old = np.sum(population_children.Chromosome[individual_number])

            #print("individual no ",individual_number)
            
            mutate_local_loc_1 = mutate_location - ((individual_number-1)*number_of_containers)
            mutate_local_loc_2_options = np.delete(np.arange(1,number_of_containers+1),mutate_local_loc_1-1)
            mutate_local_loc_2 = np.random.choice(mutate_local_loc_2_options)
            container_1_range_chromosome = [int(((mutate_local_loc_1-1) * container_width)),int((mutate_local_loc_1 * container_width))]
            container_2_range_chromosome = [int(((mutate_local_loc_2-1) * container_width)),int((mutate_local_loc_2 * container_width))]
            """
            Chosing maximum transfer of thickness between the two chosen containers
            """
            current_thickness_1 = population_children.Chromosome[individual_number][container_1_range_chromosome[0]] #hier gaat iets fout met current thickness
            #print("current thickness" , current_thickness_1)
            current_thickness_2 = population_children.Chromosome[individual_number][container_2_range_chromosome[0]]
            
            available_thickness_increase = int((thickness_dict[max(thickness_dict)] - current_thickness_1)/ delta_t_min) #calculating how much a container thickness can increase until it reaches the maximum thickness level
            available_thickness_decrease = int((current_thickness_2 - thickness_dict[min(thickness_dict)]) / (delta_t_min)) #give some margin within the rounding, otherwise will give an error
            available_thickness_change = min(available_thickness_increase, available_thickness_decrease) #if decrease is 0 , then something goes wrong
            
            current_thickness_level_1 = int((current_thickness_1 - thickness_dict[min(thickness_dict)] ) / (delta_t_min - 0.01))
            
            if available_thickness_change == 0:
                continue
            else:
                thickness_options_array = np.arange(current_thickness_level_1, current_thickness_level_1 + available_thickness_change +1)
            
            """
            Applying the thickness changes to the respective containers
            """
            new_thickness_no_1 = np.random.choice(thickness_options_array)
            new_thickness_level_1 = thickness_dict[new_thickness_no_1]
            #thickness_difference = new_thickness_level - population_children.Chromosome[individual_number][container_1_range_chromosome[0]]
            thickness_level_difference = new_thickness_no_1 - current_thickness_level_1
            new_thickness_level_2 = current_thickness_2 - (delta_t_min*thickness_level_difference)
            
            population_children.Chromosome[individual_number][container_1_range_chromosome[0]:container_1_range_chromosome[1]] = new_thickness_level_1
            population_children.Chromosome[individual_number][container_2_range_chromosome[0]:container_2_range_chromosome[1]] = new_thickness_level_2

            """
            Mirror mutated chromosome around centre to make it symmetrical again
            """
            population_children.Chromosome[individual_number] = np.append(population_children.Chromosome[individual_number][:(half_width/2)],np.flipud(population_children.Chromosome[individual_number][:(half_width/2)]))
            
            if abs(new_thickness_level_1 - current_thickness_1) > 0.03 and new_thickness_level_2 == current_thickness_2 or new_thickness_level_1 == current_thickness_1 and abs(new_thickness_level_2 - current_thickness_2) > 0.03:
                print("thickness out of bounds for individual", individual_number)
                print("thickness 1 for this individual was ", current_thickness_1," at current thickness level ", current_thickness_level_1," and now it is ", new_thickness_level_1)
                print("the thickness options were ", thickness_options_array)
                print("thickness 2 for this individual was ", current_thickness_2, " and now it is ", new_thickness_level_2)
                print("mutation took place at location ",mutate_local_loc_1, "and mirrored at location ", mutate_local_loc_2)
                sys.exit('GA stopped due to unequal area with reference panel after mutation')
            
        #print(population_children)
        return population_children
        
        
    """
    #==============================================================================
    #                           Elitism methods
    #==============================================================================
    """
            
            
    def apply_elites(self, bc, population_selected):
        
        """
        Take children population and fill in first individuals with elites
        """
        
        pop_size = int(bc.ix["Population size"])
        population_children = genetic_algorithm.children_population(self, bc)
        
        elites_perc = bc.ix["Elites percentage"]
        number_of_elites = int(pop_size * elites_perc)
        
        if pop_size * elites_perc < 0:
            print("No Elites chosen due to wrong elites percentage versus population size settings")
        
        else:
            for k in range(1,number_of_elites+1):
                elite_index = population_selected.index[k]
                population_children.at[k,"Chromosome"] = population_selected["Chromosome"][elite_index]
            
                #print("Population with elites applied",population_children)
        
        return population_children, number_of_elites
        
             
    def apply_elites_inverse(self, bc, population_selected):
        
        """
        Take children population and fill in first individuals with elites
        """
        
        pop_size = int(bc.ix["Population size"])
        population_children = genetic_algorithm.children_population(self, bc)
        population_selected_inverse = population_selected.sort_values("Fitness",ascending=True, kind='mergesort')
        
        elites_perc = bc.ix["Elites percentage"]
        number_of_non_elites = int(pop_size * (1-elites_perc))
        #print(number_of_non_elites)
        
        if pop_size * elites_perc < 0:
            print("No Elites chosen due to wrong elites percentage versus population size settings")
        
        for k in range(0,number_of_non_elites-1):
            elite_index = population_selected_inverse.index[k]
            population_children.at[k,"Chromosome"] = population_selected_inverse["Chromosome"][elite_index]
            
            
        #print("Population with elites applied",population_children)
        
        return population_children
    
    """
    #==============================================================================
    #                    Termination Conditions
    #==============================================================================
    """
        
    def CheckTermination(PopulationCurrent, Generation):
        
        # add in unique termination conditions based on fitness values
        
        TerminationCondition = False
        
        
        return TerminationCondition
        
        
        
        
    """
    #==============================================================================
    #                    Population convergence methods
    #==============================================================================
    """
    """
    Stores key data per generation for analysis
    """

    def population_convergence(self, bc, population_eval,g, convergence_overview):
        population_convergence = convergence_overview
        number_of_generations = int(bc.ix["Number of Generations"])
        array = np.zeros(((number_of_generations),4))
        index = range(1,(number_of_generations)+1)
        ranked_population = population_eval.sort_values("Fitness", ascending=False,kind='mergesort')

        if g == 0:
            list = {"Individual No.", "Crenellation Pattern","Fitness", "Generation No"}
            population_convergence = pd.DataFrame(data=array, index = index, columns = list, dtype = 'object')
        else:
            population_convergence["Fitness"][g] = ranked_population["Fitness"].head(1).values        #change the number for the number of individuals you want to show in the convergence
            population_convergence["Crenellation Pattern"][g] = ranked_population["Chromosome"].head(1).values           
            population_convergence["Individual No."][g] =  ranked_population["Original Indi. No"].head(1).values         
            population_convergence["Generation No"][g] =  g  
            
        return population_convergence
        
        
#==============================================================================
#        Old code not being used 
#==============================================================================
        
#    def children_population(self, bc):
#        """
#        Constructs an empty dataframe as the children population. 
#        """
#        pop_size = int(bc.ix["Population size"])
#        array = np.zeros((pop_size,7))
#        index = range(1,pop_size+1)
#        list = {"Original Indi. No","Fitness", "Chromosome", "Cren Design", "Balance", "Lower Bound","Upper Bound"}
#        population_children = pd.DataFrame(data=array, index = index, columns = list, dtype = 'object')
#                
#        for i in range(1,pop_size+1):
#            population_children["Original Indi. No"][i] = index[i-1]
#        
#        return population_children
#        

    def MutateRandom_OLD(PopulationOffspring, Pm):
        """
        Mutate for highly refined crenellation patterns, not the simple cases. Only review if necessary at this point.
        """
        #print(number_of_elites)
        t_ref = bc.ix["Reference thickness"]
        pop_size_all = bc.ix["Population size"]
        pop_size_non_elites = pop_size_all - number_of_elites
        mutation_rate = bc.ix["Mutation Rate"]
        chromosome_length = int(len(population_children["Chromosome"][1])/2)
        mutation_width = bc.ix["Mutation Width"]
        number_of_mutations = int((mutation_rate * pop_size_non_elites * chromosome_length)/(mutation_width*chromosome_length))  #subtract the elites
        total_locations = int(pop_size_all * chromosome_length)
        
        start_mutation_location =int(number_of_elites * chromosome_length)
        
        mutation_locations = np.random.randint(start_mutation_location,total_locations, number_of_mutations)
        
        print("Starting mutation of children")
        for i in range(0,number_of_mutations):
            """
            Pick one of the mutation locations and find the respective chromosome
            """
            individual_no = int(np.floor(mutation_locations[i] / chromosome_length))
            mutation_location = mutation_locations[i] - int(individual_no * chromosome_length)
            individual_chromosome = population_children["Chromosome"][individual_no+1]
            """
            Expand the number of containers subjected to the mutation operation
            """
            bandwidth_left = int(max(0,mutation_location - mutation_width * chromosome_length))
            bandwidth_right = int(min(chromosome_length,mutation_location + mutation_width * chromosome_length))
            thickness_left = individual_chromosome[bandwidth_left]
            thickness_right = individual_chromosome[bandwidth_right]
            """
            Calculate the A_balance of the existing section of the chromosome
            """
            current_balance = np.sum((individual_chromosome[bandwidth_left:bandwidth_right+1]) - t_ref)
            """
            Re-initialize crenellation pattern for the mutation range
            """
            individual_chromosome, mutated_balance,t = crenellation.rand_thickness_mutation(self, individual_chromosome, bandwidth_left, bandwidth_right, thickness_left, thickness_right, bc)
            """
            Apply balance for the mutation range
            """
            individual_chromosome = crenellation.apply_balance_mutation(self, t, bandwidth_left, bandwidth_right, current_balance, mutated_balance, individual_chromosome, bc)
            """
            Mirror the mutated region of the chromosome to the right part of the chromosome
            """
            individual_chromosome_left_half = individual_chromosome[:chromosome_length]
            individual_chromosome = np.append(individual_chromosome_left_half,np.flipud(individual_chromosome_left_half))
            """
            Insert mutated chromosome back into the population
            """
            population_children["Chromosome"][individual_no+1] = individual_chromosome
            
        return population_children




    """
    Single Point Crossover - OLD - using feasible crossover points as a method to guide search within feasible solution space
    """

    def CrossoverSinglePoint_OLD(ParentSelected1, ParentSelected2, PopulationOffspring, Pc, Constraints): #previously single_point_crossover
        """
        This method recombines the chromosomes of two parent solutions using the principles of single point crossover
        """
#        pop_size = bc.ix["Population size"]
#        t_ref = bc.ix["Reference thickness"]
#        number_of_containers = bc.ix["number_of_containers"] #fill this in into GA boundary conditions
#        half_width = bc.ix["Width"]/2
        OutputChildren = 2
#        number_of_elites = int(pop_size -  population_children["Chromosome"].count())
#        number_of_children = int(pop_size - number_of_elites) #- np.count_nonzero(population_children["Chromosome"])
#        number_of_couples = int(number_of_children / output_children_per_couple)
#        chromosome_half_length = int(len(population_parents["Chromosome"][1])/2)
#        container_width = chromosome_half_length / number_of_containers
        
        """
        Pair two parents and calculate the array of feasible crossover points
        """
        

        feasible_crossover_points = []

        while feasible_crossover_points == []:
            parent_1_index = genetic_algorithm.pair_parents(self, bc,population_parents) #chooses parent 1
            parent_2_index = genetic_algorithm.pair_parents(self, bc,population_parents) #chooses parent 2
            
            while parent_1_index == parent_2_index:
                parent_2_index = genetic_algorithm.pair_parents(self, bc,population_parents) #ensures that the parents are not the same
                            
            for crossover_point in range(1,chromosome_half_length-1):

                area_parent_1 = np.sum(population_parents["Chromosome"][parent_1_index][:crossover_point])
                area_parent_2 = np.sum(population_parents["Chromosome"][parent_2_index][:crossover_point])
                
                """
                Check whether the area of both parents' chromosomes until the crossover point is within narrow range of each other.
                If so, the crossover point is feasible as it will yield children of equal area compared to its parents.
                """
                
                if area_parent_1 - 0.0001 < area_parent_2 < area_parent_1 +0.0001: 
                    
                    container_edges = np.arange(1,number_of_containers)*container_width
                    
                    """
                    If the crossover point is at an edge of the container, add it to the array of feasible crossover points.
                    Not most computationally efficient, yet not a bottleneck.
                    """
                    
                    if crossover_point in container_edges:
                        feasible_crossover_points = np.append(feasible_crossover_points,int(crossover_point))
                        print("possible crossover points",feasible_crossover_points)
#                        print("area parent 1",area_parent_1)
#                        print("area parent 2", area_parent_2)
        
#            print("total feasible crossover points",feasible_crossover_points)

        """
        From array of feasible crossover points, choose one crossover point following a uniform random distribution
        """
        cross_over_point = np.random.choice(feasible_crossover_points)
#            print("crossover point chosen", cross_over_point)

        """
        Perform the crossover by combining different parts of both parents.
        """
        parent_1_left = population_parents["Chromosome"][parent_1_index][:cross_over_point]
        parent_2_left = population_parents["Chromosome"][parent_2_index][:cross_over_point]
        parent_1_right = population_parents["Chromosome"][parent_1_index][cross_over_point:chromosome_half_length]
        parent_2_right = population_parents["Chromosome"][parent_2_index][cross_over_point:chromosome_half_length]
        child_1_chromosome_left_half = np.append(parent_1_left, parent_2_right)
        child_2_chromosome_left_half = np.append(parent_2_left, parent_1_right)
        child_1_chromosome = np.append(child_1_chromosome_left_half,np.flipud(child_1_chromosome_left_half))
        child_2_chromosome = np.append(child_2_chromosome_left_half,np.flipud(child_2_chromosome_left_half))
        """
        Calculate and apply the rebalancing of the new chromosome
        """
#            individual_no = i
#            individual_no_2 = i + number_of_couples
        
#            child_1_chromosome = crenellation.apply_balance_crossover(self, child_1_chromosome, bc, individual_no)
#            child_2_chromosome = crenellation.apply_balance_crossover(self, child_2_chromosome, bc, individual_no_2)
        """
        Assign new children to the children population
        """
        population_children["Chromosome"][i] = child_1_chromosome
        population_children["Chromosome"][i+number_of_couples] = child_2_chromosome
        
#            """
#            Check whether the area of the children is equal to the parents
#            """
#            area_child_1 = int(np.sum(child_1_chromosome))
#            area_child_2 = int(np.sum(child_2_chromosome))
#            area_parent_1 = np.sum(population_parents["Chromosome"][parent_1_index])
#            area_parent_2 = np.sum(population_parents["Chromosome"][parent_2_index])
#            area_ref = int(t_ref * half_width)
        
#            if area_child_1 not in range(int(area_ref - 10), int(area_ref +10)) or area_child_2 not in range(int(area_ref - 10), int(area_ref +10)):
#                print("area out of bounds after crossover for children individual ", i," or ",i+number_of_couples)
#                print("the area for child 1 was ",area_child_1," and child 2 was ",area_child_2)
#                print("the area for parent 1 was ",area_parent_1," and parent 2 was ",area_parent_2)
#                print("Population parents was ",population_parents)
#                print("parent 1 was number ",parent_1_index," and parent 2 was number ",parent_2_index)
#                print("Population children became ", population_children)
#                sys.exit('GA stopped due to unequal area with reference panel after crossover')
#            
        return population_children
        