#ifndef DEPOT_H
#define DEPOT_H

#include <vector>

struct Customer;

class Depot
{
    public:
        int coord_x;
        int coord_y;
        int max_route_len;
        int max_vehicle_load;
        std::vector<int> customers;

        Depot();
        Depot(int max_route_len, int max_vehicle_load);
        void set_coords(int x, int y);
        void assign_customer(int customer);
        void unassign_customer(int customer);
        std::vector<int> get_customers();
        void assign_route(std::vector<Customer> customers);
};

struct Customer 
{
    int id;
    int coord_x;
    int coord_y;
    int service_duration;
    int demand;
    Customer(int id, int coord_x, int coord_y, int service_duration, int demand);
};

#endif