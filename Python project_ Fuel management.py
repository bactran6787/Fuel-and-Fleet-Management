"""
Progame: Vehicle Fuel Management

Author: Bac Tran
Last Edit: 21/10/2021
Email: tranbacise@gmail.com

Description: The program helps the fleet company to manage fuel consumption and
travel distance based on the given information about fuel transactions, odometer
reading and initial setting of the fleet. The user can input the vehicle plate
number to check the fuel performance. Also, user can input the threshold value
to classify the suspicious vehicles in term of fuel performance.

To run the program, you need 2 files "transactions" and "configuration" at the 
same directory as the Python program file.

You can open the program using Spyder (Anaconda) or Wing IDE 101. 
If you use Wing IDE101, please clik the "Lady Bug" button to run

"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame

def read_transactions_file(filename):
    """get transaction data from transactions_file"""    
    trans_data = pd.read_csv(filename)
    return trans_data

def config_input(filename):
    """ read configuration csv file and return a vehicles list contains all the
        Object Vehicle"""
    infile = open(filename)
    contents = infile.read()
    infile.close()                 
    lines1 = contents.splitlines()
    lines=lines1[1:]
    vehicle_list = []
    for line in lines:
        plate_num, fuel_quota, odo = line.split(',')
        #Assign class Vehicle for each vehicle in the list:
        vehicle = Vehicle(plate_num, float(fuel_quota), float(odo))
        vehicle_list.append(vehicle)
    return vehicle_list

class Vehicle:
    """Defines a Vehicle class"""
    def __init__(self, plate_num, fuel_quota, odo):
        """Creates a new vehicle with the plate number, fuel quota, initial
        odometer and fuel transaction"""
        self.plate_num = plate_num
        self.fuel_quota = fuel_quota
        self.odo = odo
        self.transactions = [] #list of all transactions for single Vehicle
        
    def __str__(self):
        """Returns a string representation of the Vehicle object"""
        return f"{self.plate_num}"
        
    def add_transactions(self, trans_data):
        """add transactions to Vehicle object: fuel volume, fuel price, odo"""
        self.transactions = trans_data.loc[trans_data['Vehicle plate'] \
                             == self.plate_num,:]

    def fuel_consumption(self):
        """calculate total fuel_consumption"""
        return np.sum(self.transactions['Quantity(L)'].values)
    
    def travel_distance(self):
        """calculate total travel distance in km:
        final odometer reading - initial odometer reading"""
        return (self.transactions['Odometer'].values[-1] - self.odo)
    
    def fuel_performance(self):
        """calculate fuel performance Litres/100km"""
        return 100 * self.fuel_consumption() / self.travel_distance()
    
    def daily_performance(self):
        """"compute and return a dict of total fuel per day for entire vehicle"""
        fuels = np.array(self.transactions['Quantity(L)'].values)
        odo1 = np.array(self.transactions['Odometer'].values)
        odo2 = np.insert(odo1[:-1], 0, self.odo)
        distances = odo1 - odo2
        daily_performance = 100 * fuels / distances
        return (daily_performance)
    
    def date_to_plot(self):
        day_list = []
        date = self.transactions['Date']
        for date in self.transactions['Date']:
            day, month, year = date.split("/")
            day_list.append(day)  
        return day_list
    
    def plot_daily_performance(self):
        """plot fuel consumption daily"""
        xs = self.date_to_plot()
        ys1 = self.daily_performance()
        ys2 = np.full(len(xs), self.fuel_quota)
        axes = plt.axes()
        axes.bar(xs, ys1, color='orange')
        plt.axhline(y= self.fuel_quota, color='r', linestyle='-', label='Quota')
        axes.set_title(f'Fuel Performance of vehicle No. {self.plate_num}')
        axes.set_xlabel('Day')
        axes.set_ylabel('Fuel Performance (L/100km) ') 
        axes.legend()
        axes.grid(False)
        plt.show()    

class Company:
    """Defines a Company class for entire vehicles"""
    def __init__(self, trans_data, vehicle_list):
        self.data = trans_data #all the transactions data of the Company
        self.vehicles = vehicle_list 
        self.total_fuel = sum(trans_data['Quantity(L)'])
        self.total_amount = sum(trans_data['Quantity(L)'] \
                            * trans_data['Price (VND)'])
        self.num_vehicle = len(vehicle_list)
        
    def __str__(self):
        """Returns a string represent general information of the Company object"""
        return f"Number of vehicles: {self.num_vehicle}.\n\
        Total fuel consumption: {self.total_fuel:.1f} Litres. \n\
        Total Fuel Amount: {int(self.total_amount)} VND.\n\
        Total Travel Distance: {int(self.total_travel())} km. \n\
        Average Fuel Performance: {self.average_performance():.1f} Litres/100km.\n\
        Best 5 vehicles in fuel: {self.best5_performance()}. \n\
        Best 5 vehicles in travel: {self.best5_travel()}."
        
    def vehicles_no(self):
        """return a list contain all vehicle no."""
        vehicles_no = set(self.data['Vehicle plate'])
        return vehicles_no
        
    def total_travel(self):
        """return total travel distance km"""
        total_travel = 0
        for vehicle in self.vehicles:
            total_travel += vehicle.travel_distance()   
        return total_travel
    
    def average_performance(self):
        """return mean of all vehicle fuel performance (Litres/100km)"""
        performance_list = []
        for vehicle in self.vehicles:
            performance_list.append(vehicle.fuel_performance())
        return np.mean(performance_list)
    
    def daily_fuel(self):
        """"compute and return a dictionary of total fuel per day for entire vehicle"""
        fuel_dict = {}
        for date in self.data['Date']:
            day, month, year = date.split("/")
            fuel_dict[int(day)] = sum((self.data.loc[self.data['Date'] \
                                        == date])['Quantity(L)'])
        return fuel_dict
    
    def best5_performance(self):
        """return a string contains 5 vehicles with highest fuel performance"""
        ranking = []
        best5_fuel = []
        for vehicle in self.vehicles:
            ranking.append((vehicle.plate_num, vehicle.fuel_performance()))
        ranking.sort(key = lambda x: x[1],reverse= True)
        list5 = ranking[-5:]
        for i in range(len(list5)):
            plate, fuel = list5[i]
            best5_fuel.append(plate)
        str_vehicle = ', '.join(best5_fuel)
        return str_vehicle 
    
    def best5_travel(self):
        """return a string contains 5 vehicles with highest travel distance"""
        ranking = []
        best5_travel = []
        for vehicle in self.vehicles:
            ranking.append((vehicle.plate_num, vehicle.travel_distance()))
        ranking.sort(key = lambda x: x[1])
        list5 = ranking[-5:]
        for i in range(len(list5)):
            plate, travel = list5[i]
            best5_travel.append(plate)
        str_vehicle = ', '.join(best5_travel)
        return str_vehicle        
    
    def plot_fuel_per_day(self):
        """plot fuel consumption daily"""
        fuel_dict = self.daily_fuel()
        xs = list(fuel_dict.keys())
        ys = list(fuel_dict.values())
        axes = plt.axes()
        axes.plot(xs, ys, 'ro-')
        axes.set_title(f'Company Fuel Consumption\n{self.num_vehicle} vehicles')
        axes.set_xlabel('Day')
        axes.set_ylabel('Fuel consumption per day')
        axes.grid(True)
        plt.show()
        
    def suspicious_vehicle(self, threshold):
        """get vehicles with fuel performance above or below 
        (threshold * 100%) * fuel quota"""
        sus_vehicles = []
        for vehicle in self.vehicles:
            if vehicle.fuel_performance() >= (1 + threshold) * vehicle.fuel_quota\
               or vehicle.fuel_performance() <= (1 - threshold) * vehicle.fuel_quota:
                sus_vehicles.append(vehicle)
        return sus_vehicles
    
    def sus_dataframe(self, threshold):
        """ return data frame for exporting all the suspicious vehicles 
        transaction to csv file"""
        sus_vehicles = self.suspicious_vehicle(threshold)
        sus_dict = {}
        for vehicle in sus_vehicles:
            sus_dict[vehicle.plate_num] = vehicle.transactions 
        sus_data = pd.DataFrame(sus_dict)
        return sus_data   
    
    def plot_suspicious_vehicle(self, threshold):
        """plot fuel performance for suspicious vehicles"""
        performance_data = []
        plate_data = []
        quota_data = []
        for vehicle in self.suspicious_vehicle(threshold):
            performance_data.append(vehicle.fuel_performance())
            plate_data.append(vehicle.plate_num)
            quota_data.append(vehicle.fuel_quota)
        ys1 = performance_data
        ys2 = np.array(quota_data)
        xs = plate_data
        axes = plt.axes()
        axes.bar(xs, ys1, label='Actual', color='orange')
        axes.plot(xs, ys2, 'ro-',label='Quota')
        axes.set_title(f'Fuel Performance Report \nSuspicious Vehicles by THRESHOLD {threshold:.2f}')
        axes.set_xlabel('Plate Number')
        axes.set_ylabel('Fuel Performance (L/100km)')
        axes.set_xticks(xs)
        axes.set_xticklabels(xs, rotation = 90)
        plt.tight_layout()    
        axes.legend(loc='best')
        plt.show()

class FuelGui:
    """define FuelGui class"""
    def __init__(self, window, vehicle_list, my_company):
        """Setup GUI on given window and get the necessary data"""
        self.vehicle_list = vehicle_list
        self.my_company = my_company
        
        #Create 2 Frame: header Frame and main Frame
        self.header_frame = Frame(window, bg='red', width=690, height=70)
        self.header_frame.grid(row=0, column=0, columnspan=2)
            
        self.main_frame = Frame(window, bg='white', highlightbackground="white",\
                                highlightthickness=20, width=690, height=600)
        self.main_frame.grid(row=1, column=0, rowspan=2)
        
        #Setup header frame
        self.header_frame.grid_propagate(0)
        self.header_frame.grid_rowconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=1)
        self.label_header_text_2 = tk.Label(self.header_frame,\
                                            text='VEHICLE FUEL MANAGEMENT',\
                                            bg='red', fg='white', \
                                            font=("Arial", 30))
        self.label_header_text_2.grid(row=0, column=1)
        
        # Setup main frame
        self.main_frame.grid_propagate(0)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        
        #Create 2 sub frames inside the main frame: top and bottom main frame
        #top main frame
        self.top_main_frame = Frame(self.main_frame, bg='white',\
                                    highlightbackground="#5f9cad",\
                                    highlightthickness=2, width=660, height=170)
        self.top_main_frame.grid(row=0)
        self.top_main_frame.grid_propagate(0)
        self.top_main_frame.grid_rowconfigure(10, weight=1)
        self.top_main_frame.grid_columnconfigure(8, weight=1)
        
        #bottom main frame
        self.bottom_main_frame = Frame(self.main_frame, bg='white',\
                                       width=660, height=480)    
        self.bottom_main_frame.grid(row=5, sticky='n')
        self.bottom_main_frame.grid_propagate(0)
        self.bottom_main_frame.grid_rowconfigure(8, weight=1)
        self.bottom_main_frame.grid_columnconfigure(8, weight=1)
        
        #Setup the widgets for the top main_frame
        #Summary and Plot
        self.btn_general = tk.Button(self.top_main_frame,\
                                     text='Summary and Plot',\
                                     command=self.general_report)
        self.btn_general.grid(row=0, column=8)
        self.label_general_report = tk.Label(self.top_main_frame, text="", bg='white')
        self.label_general_report.grid(row=1, column=8, rowspan = 8,\
                                       sticky = W )
        #Single Vehicle Plot
        single_notice = "Please input vehicle number"
        self.label_single = tk.Label(self.top_main_frame, text=single_notice, bg='white')
        self.label_single.grid(row=0, column=0, pady=5)        
        self.btn_single = tk.Button(self.top_main_frame, text='Plot Single Vehicle',\
                                    command=self.single_report)
        self.btn_single.grid(row=1, column=0)
        self.entry_vehicle = tk.Entry(self.top_main_frame, width=20)
        self.entry_vehicle.grid(row=2, column=0)
        self.label_message1 = tk.Label(self.top_main_frame, text= '',\
                                       bg='white', anchor=W)
        self.label_message1.grid(row=3, column=0)        
        
        #Setup the widgets for the bottom_main_frame
        #Threshold widget
        text1 = "Please input THRESHOLD for fuel limit (0< THRESHOLD <1)"
        text2 = "Suspicious vehicle will be classified by:"
        text3 = "fuel performance <(1 - THRESHOLD)fuel quota  OR  (1 + THRESHOLD)fuel quota < fuel performance"
        threshold_notice = f'   {text1}\n   {text2}\n      {text3}'
        self.label_threshold_note = tk.Label(self.bottom_main_frame, \
                                             text=threshold_notice , bg='white', anchor=W)
        self.label_threshold_note.grid(row=0, column=0, pady=6)
        self.label_threshold = tk.Label(self.bottom_main_frame, \
                                        text= 'THRESHOLD', bg='white')
        self.label_threshold.grid(row=1, column=0, pady=6)
        self.entry_threshold = tk.Entry(self.bottom_main_frame, width=20)
        self.entry_threshold.grid(row=2, column=0)    
        
        #Classify suspicious vehicles wiget
        self.btn_Classify = tk.Button(self.bottom_main_frame, \
                                      text='Classify Suspicious Vehicles',\
                                      command=self.suspicious_vehicles)
        self.btn_Classify.grid(row=3, column=0, pady=5)
        
        #Display the classification result wiget
        self.label_result = tk.Label(self.bottom_main_frame, \
                                     text= 'Suspicious Vehicles:', bg='white')
        self.label_result.grid(row=4, column=0, pady=5)
        self.label_message2 = tk.Label(self.bottom_main_frame, text= '', \
                                       bg='white', wraplength=500)
        self.label_message2.grid(row=5, column=0 )
        
        #Plot the classification result button
        self.btn_plot = tk.Button(self.bottom_main_frame, text='Plot Result', \
                                  command=self.plot_result)
        self.btn_plot.grid(row=6, column=0)        
        
        #Save the classification result button
        self.btn_savefile = tk.Button(self.bottom_main_frame, \
                                 text='Export Result', command=self.export_file)
        self.btn_savefile.grid(row=7, column=0 )        
        
    def general_report(self):
        """Display summary report for entire vehicles and plot the company fuel 
        consumption"""
        self.label_general_report.configure(text = self.my_company)
        (self.my_company).plot_fuel_per_day()
        
    def single_report(self):
        """plot the daily fuel performance based on vehicle No. input"""
        vehicle_no = self.entry_vehicle.get()
        if vehicle_no not in self.my_company.vehicles_no():
            self.label_message1.configure(\
                text = 'You must enter a valid vehicle plate number.\nPlease try again',\
                fg='red')
        else:
            for vehicle in self.vehicle_list: # get the Object from vehicle_list to plot
                if vehicle.plate_num == vehicle_no:
                    vehicle.plot_daily_performance()
            
    def suspicious_vehicles(self):
        """return suspicious vehicles with the threshold input"""
        try:
            threshold = float(self.entry_threshold.get())
        except ValueError:
            self.label_message2.configure(\
                text = 'You must enter a valid threshold \nPlease try again', fg='red')
        else:
            if float(self.entry_threshold.get()) <= 0 or \
               float(self.entry_threshold.get()) >= 1:
                self.label_message2.configure(\
                    text = 'You must enter a threshold value between 0 and 1 \nPlease try again',\
                    fg='red')
            else:
                sus_vehicles = self.my_company.suspicious_vehicle(threshold)
                self.label_message2.configure(text = sus_vehicles, fg='red')
                return sus_vehicles    
    
    def plot_result(self):
        """Plot fuel performance for suspicious vehicles"""
        try:
            threshold = float(self.entry_threshold.get())
        except ValueError:
            self.label_message2.configure(\
                text = 'You must enter a valid threshold \nPlease try again',\
                fg='red')
        else:
            if float(self.entry_threshold.get()) <= 0 or \
               float(self.entry_threshold.get()) >= 1:
                self.label_message2.configure(\
                    text = 'You must enter a threshold value between 0 and 1 \nPlease try again',\
                    fg='red')
            else:        
                threshold = float(self.entry_threshold.get())
                self.my_company.plot_suspicious_vehicle(threshold)
        
    def export_file(self):
        """Export the result data for transactions of all suspicious vehicle
        to a csv file"""
        sus_vehicles = self.suspicious_vehicles()
        sus_list = []
        for vehicle in sus_vehicles:
            sus_list.append(vehicle.transactions)
        sus_data = pd.concat(sus_list, ignore_index=True)
        export_csv = sus_data.to_csv("export_data.csv")    
                         
def main():
    """Main function"""
    vehicle_list = config_input('configuration.csv')
    trans_data = read_transactions_file('transactions.csv')
    my_company = Company(trans_data, vehicle_list)#Create a Object Company
    for vehicle in vehicle_list:
        vehicle.add_transactions(trans_data)#add transactions to each Object Vehicle    
    window = tk.Tk()
    fuel_gui = FuelGui(window, vehicle_list, my_company)
    window.mainloop()

main()







        
    
    