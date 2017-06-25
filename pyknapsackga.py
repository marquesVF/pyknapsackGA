from random import randint, uniform
from log import Log, INFO, DEBUG, IMPORTANT, FINAL

CHROMOSOME = 0
CHROMOSOME_VALUE = 1
CHROMOSOME_WEIGHT = 2
CHROMOSOME_PROBABILITY_SELECTION = 3
ITEM_VALUE = 0
ITEM_WEIGHT = 1

MAX = 999999999999999999999999

log = Log(debug=False)


class KnapsackGA:
    def __init__(self, values=list(),
                 weights=list(),
                 knapsack_weight=0,
                 population_quantity=0,
                 generation_limit=1,
                 mutation_prob = 10): # Percent
        assert len(values) == len(weights)
        assert population_quantity > 0

        """
        'self.population' is an array of chromosomes.
        Each chromosome is a list containing  4 elements:
            #1 is an array of 1s and 0s (it determines if an item is included or not)
            #2 is the total_value
            #3 is the total_weight
            #4 is the probability for reproduction selection
        """
        self.population = list()
        self.total_items = len(values)
        self.population_quantity = population_quantity
        self.knapsack_weight = knapsack_weight
        self.generation = 0
        self.generation_limit = generation_limit
        self.mutation_prob = mutation_prob
        self.items = [(values[i], weights[i]) for i in range(self.total_items)]
        log.log(INFO, "Itens -> "+str(self.items))

    def loop(self):
        log.log(INFO, "Generating population of " + str(self.population_quantity))
        self._init_population()
        self._fitness()
        for i in range(self.generation_limit):
            self.generation += 1
            log.log(DEBUG, ("Generation #%s" % self.generation))
            mates = self._selection()
            self._crossover(mates)
            self._fitness()
        log.log(DEBUG, "The final population is -> " + str(self.population))

    def get_solution(self):
        max = 0
        chromosome = None
        weight = 0
        for pop_unit in self.population:
            value = pop_unit[CHROMOSOME_VALUE]
            if value > max:
                max = value
                weight = pop_unit[CHROMOSOME_WEIGHT]
                chromosome = pop_unit[CHROMOSOME]
        return (chromosome, max, weight)

    def _init_population(self):
        self.population = [[
                               [(randint(0, 1)) for i in range(self.total_items)],
                               0,
                               0,
                               0
                           ]
                           for times in range(self.population_quantity)]

    def _fitness(self):
        for pop_unit in self.population:
            chromosome = pop_unit[CHROMOSOME]
            total_weight = MAX
            while total_weight > self.knapsack_weight:
                total_value = 0
                total_weight = 0
                for i in range(len(chromosome)):
                    if chromosome[i] == 1:
                        total_value += self.items[i][ITEM_VALUE]
                        total_weight += self.items[i][ITEM_WEIGHT]
                # log(DEBUG, "Total Weight: "+str(total_weight))
                pop_unit[CHROMOSOME_VALUE] = total_value
                pop_unit[CHROMOSOME_WEIGHT] = total_weight
                # Remove one item (set it to 0) if the total_weight is bigger then the knapsack capacity
                if total_weight > self.knapsack_weight:
                    for item in range(len(chromosome)):
                        if chromosome[item] == 1:
                            chromosome[item] = 0
                            break

    def _roulette_wheel(self):
        pop_max_value = 0
        for pop_unit in self.population:
            pop_max_value += pop_unit[CHROMOSOME_VALUE]
        log.log(INFO, "Total population value: "+str(pop_max_value))

        for pop_unit in self.population:
            pop_unit[CHROMOSOME_PROBABILITY_SELECTION] = pop_unit[CHROMOSOME_VALUE]/pop_max_value

        r = uniform(0, 1)
        sum = 0
        for i in range(0, self.population_quantity):
            pop_unit = self.population[i]
            sum += pop_unit[CHROMOSOME_PROBABILITY_SELECTION]
            if r < sum:
                return self.population[i]
        return self.population[0]

    def _selection(self):
        mates = list()
        for i in range(self.population_quantity//2):
            mate = self._roulette_wheel()
            mates.append(mate)
        # log(DEBUG, "Mates -> " + str(mates))
        return mates

    def _mutation(self, individual):
        lucky = randint(0, 100)
        if lucky <= self.mutation_prob:
            mutation_gene = randint(0, len(individual)-1)
            if individual[mutation_gene] == 1:
                individual[mutation_gene] = 0
            else:
                individual[mutation_gene] = 1
            log.log(IMPORTANT, "A mutation is going on")
        return individual

    def _crossover(self, mates):
        log.log(DEBUG, " -> Mates.. " + str(mates))
        crossover_point = self.total_items // 2
        mates_middle = len(mates)//2
        j = mates_middle
        log.log(INFO, "Quantity of mates: " + str(len(mates)))
        new_population = list()
        for i in range(0, mates_middle):
            parent1 = mates[i][CHROMOSOME]
            parent2 = mates[j][CHROMOSOME]
            log.log(DEBUG, "Parent1: " + str(parent1))
            log.log(DEBUG, "Parent2: " + str(parent2))

            child = self._mutation(parent1[:crossover_point] + parent2[crossover_point:])
            log.log(DEBUG, "Child1: "+str(child))
            new_population.append([child, 0, 0, 0])

            child2 = self._mutation(parent2[:crossover_point] + parent1[crossover_point:])
            log.log(DEBUG, "Child2: " + str(child2))
            new_population.append([child2, 0, 0, 0])

        if len(new_population) != len(mates):
            log.log(DEBUG, "Generating on more child from random parents")

            index = randint(0, len(mates)-1)
            parent1 = mates[index][CHROMOSOME]
            index = randint(0, len(mates)-1)
            parent2 = mates[index][CHROMOSOME]
            child = self._mutation(parent1[:crossover_point] + parent2[crossover_point:])
            new_population.append([child, 0, 0, 0])
        self.population = new_population + mates
        log.log(INFO, "New population -> " + str(self.population))
        log.log(INFO, "The population size is -> " + str(len(self.population)))
