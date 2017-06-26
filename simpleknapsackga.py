from random import choice, randint
import matplotlib.pyplot as plt


# goods = [
#     [5, 7],
#     [8, 8],
#     [3, 4],
#     [2, 10],
#     [7, 4],
#     [9, 6],
#     [5, 7],
#     [10, 8],
#     [3, 7],
#     [2, 10],
#     [7, 9],
#     [9, 16],
#     [4, 2]]
#
# MAX_WEIGHT = 44

# w, v
goods = [
    [7, 5],
    [8, 8],
    [4, 3],
    [10, 2],
    [4, 7],
    [6, 9],
    [4, 4]]

MAX_WEIGHT = 22


def random_chromosome():
    return [randint(0, 1) for i in range(len(goods))]


def calc_fitness(chromo):
    fit = 0
    weight = 0
    for value in goods:
        w, f = value
        key = goods.index(value)
        weight += chromo[key] * w
        fit += chromo[key] * f
    if weight >= MAX_WEIGHT:
        return 0
    else:
        return fit


def mate(chromo1, chromo2):
    point = randint(0, len(goods))
    return chromo1[:point] + chromo2[point:]


def mutate(chromo):
    for i in range(2):
        chromo[randint(0, len(goods))] = randint(0, 1)
    return chromo


def alphas(arrs):
    decorated = [(calc_fitness(chromo), chromo) for chromo in arrs]
    decorated.sort(reverse=True)
    return [chromo[1] for chromo in decorated][:len(goods)]


def run(NUM_OFFSPRING):
    SEEDS = [random_chromosome() for i in range(NUM_OFFSPRING)]
    top10 = alphas(SEEDS)
    top = top10[0]
    i = 0
    top_prev = [0 for i in range(len(goods))]
    top_p_p = [0 for i in range(len(goods))]
    while top[:-1] != top_prev[:-1] and top[:-1] != top_p_p:
        top_p_p = top_prev
        top_prev = top10[0]
        offspring = []
        for j in range(NUM_OFFSPRING):
            offspring.append(mate(choice(top10), choice(top10)))

        top10 = alphas(offspring)
        top = top10[0]
        i += 1
    sum_weight = 0
    sum_fit = 0
    for val in goods:
        w, f = val
        key = goods.index(val)
        if top_prev[key] > 0:
            weight = top_prev[key] * w
            fit = top_prev[key] * f
            print("%d:\tweight %d price %d" % (key, weight, fit))
            sum_weight += weight
            sum_fit += fit
    print("#Sum:\nweight %d price %d" % (sum_weight, sum_fit))
    return str(sum_fit)

def plot_graph(x, y, count):
    plt.figure(count)
    plt.plot(x, y)
    plt.ylabel('Valor')
    plt.xlabel('Geração')
    # plt.ylim([0, 32])
    # plt.show()
    plt.savefig('knapsack_NEW_%s.png' % count)

if __name__ == '__main__':
    for i in range(10):
        x = [x for x in range(1, 1000)]
        y = list()
        for off in x:
            y.append(run(off))
        plot_graph(x,y,i)
        print("Foi %s" % i)

