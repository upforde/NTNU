#ifndef GA_H
#define GA_H

#include <vector>
#include <string>

#include "depot.h"

class GA
{
    std::vector<Depot> swappable_customers;
    void generate_initial_population(std::string);

    friend std::vector<int> split_line(std::string);
    friend float calc_euclidian_distance(int x1, int y1, int x2, int y2);
    friend void plot(std::vector<Depot> depots, std::vector<Customer> customers);

    public:
        static void run(std::string);
};
#endif