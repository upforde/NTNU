#ifndef GA_H
#define GA_H

#include <vector>
#include <string>

#include "depot.h"

// Struct for comparing distances between depots
struct Distance_to_depot 
{
    Depot * depot;
    double distance;
};

// Struct for ceeping track of swappable customers
struct Swappable_customer
{
    int id;
    std::vector<Depot> close_to;
};

// Genetic Algorithm class
class GA
{
    void generate_initial_population(std::string problem, std::vector<Depot *> &depots, std::vector<Customer> &customers, std::vector<Swappable_customer> &swappable_customer, double distance_threshold);

    public:
        static void run(std::string, double distance_threshold);
};

void plot(std::vector<Depot *> depots, std::vector<Customer> customers);
std::vector<int> split_line(std::string);
double calculate_euclidian_distance(int x1, int y1, int x2, int y2);
bool compare_distances(Distance_to_depot d1, Distance_to_depot d2);
void assign_customer(std::vector<Depot> &depots, Depot depot, Customer customer);

#endif