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
    std::vector<Depot*> close_to;
    Swappable_customer(int id);
};

// Genetic Algorithm class
class GA
{
    // Reads the test data and sets up the initial population based on the information in the file
    void generate_initial_population(std::string problem, std::vector<Depot> &depots, std::vector<Customer> &customers, std::vector<Swappable_customer> &swappable_customers, double distance_threshold);

    public:
        // Runs the Genetic Algorithm
        static void run(std::string, double distance_threshold);
};

// Plots the depots and customers
// TODO: implement plotting of routes
void plot(std::vector<Depot> depots, std::vector<Customer> customers);
// Splits the lines of a file by whitespace and returns converted tokens from string to int
std::vector<int> split_line(std::string);
// Calculates the euclidian distance between two points
double calculate_euclidian_distance(int x1, int y1, int x2, int y2);
// Compares distances to depots
bool compare_distances(Distance_to_depot d1, Distance_to_depot d2);

void assign_customer(std::vector<Depot> &depots, Depot depot, Customer customer);

#endif