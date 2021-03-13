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

// Reads the test data and sets up the initial population based on the information in the file
void GA::generate_initial_population(std::string problem, std::vector<Depot *> &depots, std::vector<Customer> &customers, std::vector<Swappable_customer> &swappable_customers, double distance_threshold)
{
    std::fstream file ("./Testing Data/Data Files/" + problem);
    
    int n_vehicles, n_customers, n_depots;

    int i = 0;
    std::string line;
    while (getline(file, line))
    {
        std::vector<int> tokens = split_line(line);
        if (i == 0)
        {
            n_vehicles = tokens[0];
            n_customers = tokens[1];
            n_depots = tokens[2];
        }
        else if (i <= n_depots)
        {
            Depot depot = Depot(tokens[0], tokens[1]);
            depots.push_back(&depot);
        }
        else if (i > n_depots && i <= n_customers+n_depots)
        {
            customers.push_back(Customer(tokens[0], tokens[1], tokens[2], tokens[3], tokens[4]));
        }
        else
        {
            depots[i-(n_customers+n_depots)-1]->set_coords(tokens[1], tokens[2]);
        }

        i++;
    }

    // TODO: assign all customers to depots and find swappable customers based on distance
    for(Customer customer : customers)
    {
        std::vector<Distance_to_depot> distances;
        for (Depot * depot : depots) 
        {
            distances.push_back({depot, calculate_euclidian_distance(customer.coord_x, customer.coord_y, depot->coord_x, depot->coord_y)});
        }

        std::sort(distances.begin(), distances.end(), compare_distances);
        
        for (Depot * depot : depots)
        {
            if (depot->coord_x == distances[0].depot->coord_x && depot->coord_y == distances[0].depot->coord_y)
            {
                cout << "Customer " << customer.id << " assigned to depot at [" << depot->coord_x << ", " << depot->coord_y << "]" << endl;
                depot->assign_customer(customer.id);
            }
        }
        /*
        if (distance_threshold != 0)
        {
            Swappable_customer swappable_customer;
            swappable_customer.id = customer.id;
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
        */
    }

}

void GA::run(std::string problem, double distance_threshold)
{
    GA ga;
    std::vector<Depot *> depots;
    std::vector<Customer> customers;
    std::vector<Swappable_customer> swappable_customers;

    ga.generate_initial_population(problem, depots, customers, swappable_customers, distance_threshold);

    for (Depot * depot : depots)
    {
        cout << "Customers assigned to depot at [" << depot->coord_x << ", " << depot->coord_y << "]:" << endl << "{";
        for (int customer: depot->customers)
        {
            cout << customer << ", ";
        }
        cout << "}" << endl;
    }

    plot(depots, customers);
}

// Plots the depots and customers
// TODO: implement plotting of routes
void plot(std::vector<Depot *> depots, std::vector<Customer> customers)
{
    RGBABitmapImageReference *imageref = CreateRGBABitmapImageReference();

    std::vector<double> xd, yd;
    for (Depot * depot : depots)
    {
        xd.push_back(1.0*depot->coord_x);
        yd.push_back(1.0*depot->coord_y);
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

// Splits the lines of a file by whitespace and returns converted tokens from string to int
std::vector<int> split_line(std::string line)
{
    int buf;
    std::stringstream ss(line);
    std::vector<int> tokens;

    while (ss >> buf)
        tokens.push_back(buf);
    
    return tokens;
}

// Calculates the euclidian distance between two points
double calculate_euclidian_distance(int x1, int y1, int x2, int y2)
{
    return sqrt(pow(x2-x1, 2)+pow(y2-y1, 2));
}

// Compares distances to depots
bool compare_distances(Distance_to_depot d1, Distance_to_depot d2)
{
    return d1.distance < d2.distance;
}
