mdvrp: main.o ga.o depot.o
	g++ main.o ga.o depot.o pbPlots.o supportLib.o -o mdvrp

main.o: main.cpp
	g++ -c main.cpp -std=c++11

ga.o: ga.cpp
	g++ -c ga.cpp pbPlots.cpp supportLib.cpp -std=c++11

depot.o: depot.cpp 
	g++ -c depot.cpp -std=c++11


clean:
	rm *.o