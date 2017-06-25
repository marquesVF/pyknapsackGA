import matplotlib.pyplot as plt
from pyknapsackga import KnapsackGA
from log import Log, INFO, NEWLINE, FINAL, DEBUG

# Test matters
log = Log(debug=True)
maxWeight = 22
values = [5, 8, 3, 2, 7, 9, 4]
weights = [7, 8, 4, 10, 4, 6, 4]


def plot_graph(x, y, label='', count=1):
    plt.figure(count)
    plt.plot(x, y)
    plt.ylabel('Valor')
    plt.xlabel('População')
    plt.ylim([0, 32])
    plt.savefig('knapsack_%s.png' % label)


def test_close_to_optimum():
    optimum = 28
    generation_limit = [3, 6, 12, 24]
    mutation_prob = 10
    # population_quantity = [10, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000]
    population_quantity = [x for x in range(10, 501)]

    count = 1
    for generation in generation_limit:
        y = list()
        for quantity in population_quantity:
            kga = KnapsackGA(values, weights,
                             knapsack_weight=maxWeight,
                             population_quantity=quantity,
                             generation_limit=generation,
                             mutation_prob=mutation_prob)
            kga.loop()
            result = kga.get_solution()
            log.log(FINAL, "FINAL RESULTS: ", NEWLINE)
            log.log(FINAL, "")
            log.log(FINAL, "Population Quantity: %s" % quantity)
            log.log(FINAL, "Generation Limit: %s" % generation)
            log.log(FINAL, "Mutation Probability: %s" % mutation_prob)
            log.log(FINAL, "The chosen chromosome is %s. The total value is %s. The total weight is %s" % result)
            y.append(result[1])
        x = population_quantity
        plot_graph(x, y,
                   "Limite Geração %s_Mutação a %s_PopulaçãoMáxima %s" % (generation, mutation_prob, population_quantity[len(population_quantity)-1]),
                   count)
        count += 1


if __name__ == '__main__':
    log.log(INFO, 'Starting Iterations', NEWLINE)
    log.log(DEBUG, 'Values ~> ' + str(values))
    log.log(DEBUG, 'Weights ~> ' + str(weights))
    log.log(DEBUG, 'Knapsack Maximum Weight ~> ' + str(maxWeight))

    test_close_to_optimum()

    # population_quantity = 10
    # generation_limit = 3
    # mutation_prob = 10
    # kga = KnapsackGA(values, weights,
    #                  knapsack_weight=maxWeight,
    #                  population_quantity=population_quantity,
    #                  generation_limit=generation_limit,
    #                  mutation_prob=mutation_prob)
    # kga.loop()
    # result = kga.get_solution()
    # log.log(FINAL, "FINAL RESULTS: ", NEWLINE)
    # log.log(FINAL, "")
    # log.log(FINAL, "Population Quantity: %s" % population_quantity)
    # log.log(FINAL, "Generation Limit: %s" % generation_limit)
    # log.log(FINAL, "Mutation Probability: %s" % mutation_prob)
    # log.log(FINAL, "The chosen chromosome is %s. The total value is %s. The total weight is %s" % result)
