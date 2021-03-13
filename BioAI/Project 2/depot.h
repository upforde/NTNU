#ifndef DEPOT_H
#define DEPOT_H

#include <vector>

struct Customer;

// Depot class
class Depot
{
    public:
        int coord_x;
        int coord_y;
        int max_route_len;
        int max_vehicle_load;
        std::vector<Customer> customers;

        // Default constructor
        Depot();
        // Constructor
        Depot(int max_route_len, int max_vehicle_load);
        // Sets the coordinates
        void set_coords(int x, int y);
        // Assigns routes based on max amount of deployable vehicles and their capacity
        void assign_route(std::vector<Customer> customers);
};

// Customer struct
struct Customer 
{
    int id;
    int coord_x;
    int coord_y;
    int service_duration;
    int demand;
    // Default constructor
    Customer(int id, int coord_x, int coord_y, int service_duration, int demand);
};

#endif