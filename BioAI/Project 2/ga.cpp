#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

#include "pbPlots.hpp"
#include "supportLib.hpp"
#include "ga.h"
#include "depot.h"

using std::cout;
using std::endl;

// Plots the depots and customers
// TODO: implement plotting of routes
void plot(std::vector<Depot> depots, std::vector<Customer> customers)
{
    RGBABitmapImageReference *imageref = CreateRGBABitmapImageReference();

    std::vector<double> xd, yd;
    for(Depot depot : depots)
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
    for(Customer customer : customers)
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

// Reads the test data and sets up the initial population based on the information in the file
void GA::generate_initial_population(std::string problem)
{
    std::fstream file ("./Testing Data/Data Files/" + problem);
    
    int n_vehicles;
    int n_customers;
    int n_depots;

    std::vector<Depot> depots;
    std::vector<Customer> customers;

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
            depots.push_back(Depot(tokens[0], tokens[1]));
        }
        else if (i > n_depots && i <= n_customers+n_depots)
        {
            customers.push_back(Customer(tokens[0], tokens[1], tokens[2], tokens[3], tokens[4]));
        }
        else
        {
            depots[i-(n_customers+n_depots)-1].coord_x = tokens[1];
            depots[i-(n_customers+n_depots)-1].coord_y = tokens[2];
        }

        i++;
    }

    // TODO: assign all customers to depots and find swappable customers based on distance

    // TODO: make depots make routes
    plot(depots, customers);
}

void GA::run(std::string problem)
{
    GA ga;
    ga.generate_initial_population(problem);
}