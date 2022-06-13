# Fuel-and-Fleet-Management
Description: The program helps the fleet company to manage fuel consumption and travel distance based on the given information about fuel transactions, odometer reading and initial setting of the fleet. The user can input the vehicle plate number to check the fuel performance. Also, user can input the threshold value to classify the suspicious vehicles in term of fuel performance.
It’s necessary to install Pandas library (https://pandas.pydata.org/) and Spyder (Anaconda) or Wing IDE 101 to run the program.
You can open the program using Spyder (Anaconda) or Wing IDE 101. If you use Wing IDE 101, please click the “Lady Bug” button to run. The GUI Tkinter window will be displayed with the widgets:
	1.‘Summary and Fuel Plot’ Button: plot the daily total fuel consumption of the entire vehicles and provide general information such as:
		•Number of vehicles: the count of total vehicles had fuel purchase.
		•Total Fuel Consumption (Liters): 
		•Total Fuel Amount (VND)
		•Total Travel Distance (km)
		•Average Fuel Performance (Liters/100km)
		•Best 5 vehicles in fuel
		•Best 5 vehicles in travel
	2.Vehicle number entry: input the vehicle plate number to plot its daily fuel consumption. The vehicle No. must be valid. If not, a message will be display.
	3.Plot single vehicle: provide the graph of daily fuel consumption for the given vehicle number entry
	4.Threshold entry: input the threshold for fuel limit to detect the suspicious vehicles. The threshold must be a valid float number and has value between 0 and 1. If not, a message will be display. The program will detect vehicles with fuel performance above (1 + threshold) * (fuel quota) or below (1 - threshold) * (fuel quota).
	5.‘Classify suspicious vehicles’ Button: display plate numbers of suspicious vehicles which has the outliner fuel performance.
	6.‘Plot Result’ Button: plot the fuel performance for all suspicious vehicles.
	7.‘Export Result’ Button: export all the transactions information of all suspicious vehicles to the csv file “export_file.csv”
