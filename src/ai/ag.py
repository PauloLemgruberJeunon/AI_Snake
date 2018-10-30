import numpy as np
import heapq
import snake


class Population:
    def __init__(self, factory, pop_size, individuals=None):
        self.pop_size = pop_size
        self.pop_factory = factory

        if individuals is None:
            self.population = np.empty(pop_size, dtype=object)
            self.create_population(factory)
        else:
            self.population = np.array(individuals, ndarray=object)

    def sort_population(self):
        fit_a = np.array([indv.fit for indv in self.population])
        fit_a = heapq.nlargest(self.pop_size, range(self.pop_size), fit_a.take)
        self.population = np.array([self.population[fit_a[i]] for i in range(len(fit_a))])

    def create_population(self, factory):
        for i in range(self.pop_size):
            self.population[i] = Individual(factory)

    def adapt_population(self):
        for p in range(1, self.pop_size - 4):
            self.make_crossover(self.population[p].indv,
                                self.population[0].indv, self.population[p].indv)

            self.mutate(self.population[p].indv)

        for p in range(self.pop_size - 4, self.pop_size):
            self.population[p] = Individual(self.pop_factory, self.pop_factory_args)

    def make_crossover(self, indv_a, indv_b, indv_c):
        for l in range(len(indv_a.layers)):
            indv_a.layers[l].weight_mtr = np.divide(np.add(indv_b.layers[l].weight_mtr,
                                                           indv_c.layers[l].weight_mtr), 2)

    def mutate(self, indv):
        for l in indv.layers:
            mtr = l.weight_mtr
            for i in range(mtr.shape[0]):
                for j in range(mtr.shape[1]):
                    if np.random.uniform(0, 1) < 0.2:
                        abs_val = np.abs(mtr[i][j])
                        mtr[i][j] = np.random.uniform(-abs_val, abs_val) * \
                            np.random.uniform(1.1, 2)

    def test_pop(self, input_array, y_array):
        while True:
            for indv in self.population:
                indv.clear_fit()
                for x, y in zip(input_array, y_array):
                    indv.evaluate(x, y)
                indv.fit = indv.fit / 150

            self.sort_population()
            print(self.population[0].fit)
            # if self.population[0].fit > 0.8:
            #     break
            self.adapt_population()


class Individual:
    def __init__(self, factory):
        self.fit = 0
        self.rank = 0
        self.indv = factory.create()

    def get_mov(self, input_array):
        y = self.indv.predict(input_array)
        print('Y =', y)
        y = np.argmax(y)
        if y == 0:
            return None
        elif y == 1:
            return snake.Direction.right
        else:
            return snake.Direction.left

    def clear_fit(self):
        self.fit = 0
