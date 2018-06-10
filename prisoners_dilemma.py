#!usr/bin/python2

####################################################
#
# Author: Paul Scurek
# Date: 05/06/2014
#
# Copyright 2014 Paul Scurek. All rights reserved.
#
####################################################

import random
import math

memory_key = ['CCCCCC', 'CCCCCD', 'CCCCDC', 'CCCCDD', 'CCCDCC', 'CCCDCD',
              'CCCDDC', 'CCCDDD', 'CCDCCC', 'CCDCCD', 'CCDCDC', 'CCDCDD',
              'CCDDCC', 'CCDDCD', 'CCDDDC', 'CCDDDD', 'CDCCCC', 'CDCCCD',
              'CDCCDC', 'CDCCDD', 'CDCDCC', 'CDCDCD', 'CDCDDC', 'CDCDDD',
              'CDDCCC', 'CDDCCD', 'CDDCDC', 'CDDCDD', 'CDDDCC', 'CDDDCD',
              'CDDDDC', 'CDDDDD', 'DCCCCC', 'DCCCCD', 'DCCCDC', 'DCCCDD',
              'DCCDCC', 'DCCDCD', 'DCCDDC', 'DCCDDD', 'DCDCCC', 'DCDCCD',
              'DCDCDC', 'DCDCDD', 'DCDDCC', 'DCDDCD', 'DCDDDC', 'DCDDDD',
              'DDCCCC', 'DDCCCD', 'DDCCDC', 'DDCCDD', 'DDCDCC', 'DDCDCD',
              'DDCDDC', 'DDCDDD', 'DDDCCC', 'DDDCCD', 'DDDCDC', 'DDDCDD',
              'DDDDCC', 'DDDDCD', 'DDDDDC', 'DDDDDD']

points_key = {'CC':(3, 3), 'CD':(0, 5), 'DC':(5, 0), 'DD':(1, 1)}

# n is the size of the population 
# l is the length of each chromosome in the population
def generate_population(n, l):

    population = []
    chromosome = ''
    genes = ['C', 'D']

    for x in range(n):
        for y in range(l):
            chromosome += random.choice(genes)
        population.append(chromosome)
        chromosome = ''

    return population

def prisoners_dilemma(pop_size, num_generations, num_runs, crossover_rate, mutation_rate):

    fittest_by_gen = []
    fittest_by_run = []
    fittest_current_gen = ''
    fittest_current_run = ''
    points = [0]*pop_size
    fitness = [0]*pop_size
    population = []
    offspring = []
    memory = []
    runs = []
    generations = []

    for r in range(num_runs):
        # do everything for first random generation
        population = generate_population(pop_size, 67)
        points = play_tournament(population, pop_size)
        fitness = get_fitness(points, pop_size)
        generations.append(zip(population, fitness))
        generations[0].append(fitness[-1])

        for g in range(1, num_generations):
            population = get_new_population(population, fitness, crossover_rate, mutation_rate)
            points = play_tournament(population, pop_size)
            fitness = get_fitness(points, pop_size)
            generations.append(zip(population, fitness))
            generations[g].append(fitness[-1])

        runs.append(generations)
        generations = []

    return runs

def play_tournament(population, pop_size):

    points = [0]*pop_size
    memory = []

    for s in range(pop_size):
        for t in range(s, pop_size):
            memory_s = population[s][64] + population[t][64] + population[s][65] + population[t][65] + population[s][66] + population[t][66]
            memory_t = population[t][64] + population[s][64] + population[t][65] + population[s][65] + population[t][66] + population[s][66]
            for i in range(100):
                memory_index_s = memory_key.index(memory_s)
                memory_index_t = memory_key.index(memory_t)
                move_s = population[s][memory_index_s]
                move_t = population[t][memory_index_t]
                outcome = points_key[move_s + move_t]
                points[s] += outcome[0]
                points[t] += outcome[1]
                memory_s = memory_s[2:] + move_s + move_t
                memory_t = memory_t[2:] + move_t + move_s
    return points

def get_fitness(points, pop_size):

    fitness = [0]*pop_size
    average_fitness = 0

    for x in range(pop_size):
        fitness[x] = (points[x] / (100.0 * pop_size))**2
        average_fitness += fitness[x]

    average_fitness = average_fitness / pop_size
    fitness.append(average_fitness)

    return fitness

def get_new_population(population, fitness, crossover_rate, mutation_rate):

    fitness_range = [0]*(len(population) + 1)
    new_population = []
    parent_1 = ''
    parent_2 = ''
    offspring_1 = ''
    offspring_2 = ''
    mutated_1 = ''
    mutated_2 = ''

    for x in range(len(population)):
        fitness_range[x + 1] = fitness_range[x] + fitness[x]

    for y in range(int(math.ceil(float(len(population))/2))):

        spin_1 = random.uniform(0, fitness_range[len(population)])
        for z in range(len(population)):
            if fitness_range[z] <= spin_1 <= fitness_range[z + 1]:
                parent_1, parent_2 = population[z], population[z]
                break

        while parent_1 == parent_2:
            spin_2 = random.uniform(0, fitness_range[len(population)])
            for z in range(len(population)):
                if fitness_range[z] <= spin_2 <= fitness_range[z + 1]:
                    parent_2 = population[z]
                    break

        # determine if crossover takes place
        if random.uniform(0, 1) < crossover_rate:
            crossover_position = random.randrange(67)
            offspring_1 = parent_1[:crossover_position] + parent_2[crossover_position:]
            offspring_2 = parent_2[:crossover_position] + parent_1[crossover_position:]
        else:
            offspring_1 = parent_1
            offspring_2 = parent_2

        # determine if mutation takes place at each allele of each offspring
        for x, y in zip(offspring_1, offspring_2):

            if random.uniform(0, 1) < mutation_rate:
                if x == 'C':
                    mutated_1 += 'D'
                else:
                    mutated_1 += 'C'
            else:
                mutated_1 += x

            if random.uniform(0, 1) < mutation_rate:
                if y == 'C':
                    mutated_2 += 'D'
                else:
                    mutated_2 += 'C'
            else:
                mutated_2 += y

        new_population.append(mutated_1)
        new_population.append(mutated_2)

        parent_1, parent_2 = '', ''
        mutated_1, mutated_2 = '', ''

    if len(population) % 2 != 0:
        junk = new_population.pop(random.randrange(len(new_population)))

    return new_population

A = prisoners_dilemma(40, 50, 10, 0.7, 0.001)

for x in range(41):
    print A[8][49][x]

print

population = generate_population(20, 67)

for x in range(20):
    print population[x]

print

points = play_tournament(population, 20)

points

fitness = get_fitness(points, 20)

fitness

get_new_population(population, fitness, .7, .001)

fitness_range = [0]*21
for x in range(20):
        fitness_range[x + 1] = fitness_range[x] + fitness[x]

fitness_range

random.uniform(0, fitness_range[20])
