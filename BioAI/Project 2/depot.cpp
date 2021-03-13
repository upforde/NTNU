#include <vector>
#include <algorithm>

#include "depot.h"

Depot::Depot(){}

Depot::Depot(int max_route_len, int max_vehicle_load)
{
    this->max_route_len = max_route_len;
    this->max_vehicle_load = max_vehicle_load;
}

Customer::Customer(int id, int coord_x, int coord_y, int service_duration, int demand)
{
    this->id = id;
    this->coord_x = coord_x;
    this->coord_y = coord_y;
    this->service_duration = service_duration;
    this->demand = demand;
}

void Depot::set_coords(int x, int y)
{
    this->coord_x = x;
    this->coord_y = y;
}

void Depot::assign_customer(int customer)
{
    this->customers.push_back(customer);
}

void Depot::unassign_customer(int customer)
{
    this->customers.erase(std::find(this->customers.begin(), this->customers.end(), customer));
}

// TODO: make depots make routes
void Depot::assign_route(std::vector<Customer> order)
{
    return;
}
