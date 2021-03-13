#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <cmath>
#include <limits>
#include <algorithm>

#include "pbPlots.hpp"
#include "supportLib.hpp"
#include "ga.h"
#include "depot.h"

using std::cout;
using std::endl;

Swappable_customer::Swappable_customer(int id)
{
    this->id = id;
}

void GA::generate_initial_population(std::string problem, std::vector<Depot> &depots, std::vector<Customer> &customers, std::vector<Swappable_customer> &swappable_customers,  double distance_threshold)
{
    std::fstream file ("./Testing Data/Data Files/" + problem);
    
    int n_vehicles, n_customers, n_depots;

    int i = 0;
    std::string line;
    // Reading through the file
    while (getline(file, line))
    {
        std::vector<int> tokens = split_line(line);
        // If at first line, assign the number of vehicles, number of customers and number of depots
        if (i == 0)
        {
            n_vehicles = tokens[0];
            n_customers = tokens[1];
            n_depots = tokens[2];
        }
        // The lines after the first are related to depots
        // Creates depots with relavant info about max vehicles and longest route allowed
        else if (i <= n_depots)
        {
            depots.push_back(Depot(tokens[0], tokens[1]));
        }
        // The lines after depot info are related to customers
        // Creates the customers with relevant info about their coordinates, service duration and demands
        else if (i > n_depots && i <= n_customers+n_depots)
        {
            customers.push_back(Customer(tokens[0], tokens[1], tokens[2], tokens[3], tokens[4]));
        }
        // The last lines store the coordinates of the depots, which are assigned to the depots
        else
        {
            depots[i-(n_customers+n_depots)-1].set_coords(tokens[1], tokens[2]);
        }

        i++;
    }

    // Assigning the customers to depots
    for(Customer customer : customers)
    {
        // Measuring the distance to each depot from the customer
        std::vector<Distance_to_depot> distances;
        for (int i = 0; i < depots.size(); i++)
        {
            distances.push_back({&depots[i], calculate_euclidian_distance(customer.coord_x, customer.coord_y, depots[i].coord_x, depots[i].coord_y)});
        }

        // Sorting the distances in ascending order
        std::sort(distances.begin(), distances.end(), compare_distances);
        
        distances[0].depot->customers.push_back(customer);
        
        if (distance_threshold != 0)
        {
            Swappable_customer swappable_customer(customer.id);
            for (Distance_to_depot distance_to_depot : distances)
            {
                if (distance_to_depot.distance - distances[0].distance > distance_threshold)
                {
                    swappable_customer.close_to.push_back(distance_to_depot.depot);
                }
            }
            if (swappable_customer.close_to.size() > 1) 
            {
                swappable_customers.push_back(swappable_customer);
            }
        }
    }

}

void GA::run(std::string problem, double distance_threshold)
{
    GA ga;

    std::vector<Depot> depots;
    std::vector<Customer> customers;
    std::vector<Swappable_customer> swappable_customers;

    ga.generate_initial_population(problem, depots, customers, swappable_customers, distance_threshold);

    for (Depot depot : depots)
    {
        cout << "Customers assigned to depot at [" << depot.coord_x << ", " << depot.coord_y << "]:" << endl << "{";
        for (Customer customer : depot.customers) 
        {
            cout << customer.id << ", ";
        }
        cout << "}" << endl;
    }

    for (Swappable_customer customer : swappable_customers)
    {
        cout << "Customer " << customer.id << " can be swapped between:\n";
        for (Depot* depot : customer.close_to)
        {
            cout << "[" << depot->coord_x << ", " << depot->coord_y << "] ";
        }
        cout << endl;
    }

    plot(depots, customers);
}


void plot(std::vector<Depot> depots, std::vector<Customer> customers)
{
    RGBABitmapImageReference *imageref = CreateRGBABitmapImageReference();

    std::vector<double> xd, yd;
    for (Depot depot : depots)
    {
        xd.push_back(1.0*depot.coord_x);
        yd.push_back(1.0*depot.coord_y);
    }

    ScatterPlotSeries *series = GetDefaultScatterPlotSeriesSettings();
	series->xs = &xd;
	series->ys = &yd;
    series->linearInterpolation=false;
    series->pointType = toVector(L"dots");

    std::vector<double> xc, yc;
    for (Customer customer : customers)
    {
        xc.push_back(1.0*customer.coord_x);
        yc.push_back(1.0*customer.coord_y);
    }

    ScatterPlotSeries *series2 = GetDefaultScatterPlotSeriesSettings();
	series2->xs = &xc;
	series2->ys = &yc;
    series2->linearInterpolation=false;
    series2->pointType = toVector(L"circles");

	ScatterPlotSettings *settings = GetDefaultScatterPlotSettings();
	settings->width = 600;
	settings->height = 400;
    settings->autoPadding = true;
    settings->showGrid = false;
    settings->xAxisBottom = true;
    settings->yAxisLeft = true;
	settings->scatterPlotSeries->push_back(series);
	settings->scatterPlotSeries->push_back(series2);

    DrawScatterPlotFromSettings(imageref, settings);

    std::vector<double> *pngdata = ConvertToPNG(imageref->image);
    WriteToFile(pngdata, "plot.png");
    DeleteImage(imageref->image);
}

std::vector<int> split_line(std::string line)
{
    int buf;
    std::stringstream ss(line);
    std::vector<int> tokens;

    while (ss >> buf)
        tokens.push_back(buf);
    
    return tokens;
}

double calculate_euclidian_distance(int x1, int y1, int x2, int y2)
{
    return sqrt(pow(x2-x1, 2)+pow(y2-y1, 2));
}

bool compare_distances(Distance_to_depot d1, Distance_to_depot d2)
{
    return d1.distance < d2.distance;
}
