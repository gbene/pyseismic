
# Imports

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import obspy as obs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector



import seismic_fft as s_fft
import seismic_plot as s_plt


def wd(frame):
	for w in frame.winfo_children():
		w.destroy()



# Interactive fft function
# This functions let's you choose the data region to be analyzed with the FFT algorithm and produces the corresponding frequency plot
def fft():
	def call_fft(eclick,erelease):
		x1, y1 = eclick.xdata, eclick.ydata #first corner
		x2, y2 = erelease.xdata, erelease.ydata #second corner (opposite to the first one)
		matrix_list = np.array(file_import.tr_list) #array with all the traces
		mask_x = np.where((spacing<max(x1,x2))&(spacing>min(x1,x2)))[0] #see which traces are within the x corners
		mask_y = np.where((time<max(y1,y2))&(time>min(y1,y2)))[0] #see what time interval is within the y corners

		sel_x = file_import.tr_list[mask_x.min():mask_x.max()+1] #selected traces 
		sel_y = time[mask_y.min():mask_y.max()] #time interval
		if plt.fignum_exists("Spectral analysis"): #if a spectral plot already exists:
		    call_fft.fig2.clf() #clear the previous one.
		call_fft.fig2, call_fft.ax2 = s_fft.sp_analysis(sel_x,sel_y) #plot data


	if plt.fignum_exists('Raw data'): # if something is plotted (raw data figure) then:

		RS = RectangleSelector(file_import.ax,call_fft,
				           drawtype='box', useblit=True,
				           button=[1],  # don't use middle button
				           minspanx=5, minspany=5,
				           spancoords='pixels',
				           interactive=True,state_modifier_keys={}) #define the selector and function to be run (call_fft)

		file_import.fig.canvas.mpl_connect('key_press_event', RS) #connect the selector to the canvas
		file_import.fig.show()


	else:
		print("No data to analyize")




# FFT tool interface

def tool_fft():

	#wd(tools_frame)
	fft_frame = tk.Frame(master=tools_frame)
	fft_frame.pack()
	fft_frame.rowconfigure(0,minsize=50,weight=1)
	fft_frame.columnconfigure(0,minsize=50,weight=1)
	title = tk.Label(master=fft_frame,text='FFT analysis')
	title.grid(row=0,column=0)
	freq_an = tk.Button(master=fft_frame, text=f"Spectrum \n analysis",command=fft)
	freq_an.grid(row=1,column=0)


# Filter tool interface
# This tool filters the raw seismic data by choosing one of three filters: low pass, high pass, band pass.


def tool_filter():
	def click():
		try:
			file_import.file_path[file_import.i] #if files are not imported print "files are not imported"
		except NameError:
			print('Files not imported')
		else:
			filter_fun(file_import.file_path[file_import.i],tool_filter.low_val.get(),tool_filter.high_val.get()) #filter function that actually plots the result
 

   	
	def gray_out(event):
		if filter_pass.get() == 'Low pass':
			low_value.config(state='normal')
			low_value.delete(0, 'end')
			high_value.delete(0, 'end')
			high_value.insert(0, 1_000_000)
			high_value.config(state='disabled')

		elif filter_pass.get() == 'High pass':
			high_value.config(state='normal')
			high_value.delete(0, 'end')
			low_value.delete(0, 'end')
			low_value.insert(0, 0.1)
			low_value.config(state='disabled')
		else:
			high_value.config(state='normal')
			low_value.config(state='normal')
			high_value.delete(0,'end')
			low_value.delete(0,'end')
	def toggle_auto():# auto filtering toggle (check box)
		tool_filter.auto_ap = toggle_ap.get()
		if tool_filter.auto_ap:
			click() #run one time the filter function  (only when box is checked)
			
		if filter_button["state"] == 'normal':
			filter_button["state"] = 'disabled' #disable the filter button when checked.
		else:
			filter_button["state"] = 'normal'
    	
	tool_filter.low_val=tk.StringVar()
	tool_filter.high_val=tk.StringVar()

	filter_frame = tk.Frame(master=tools_frame)
	filter_frame.pack()
	filter_frame.rowconfigure(0,minsize=50,weight=1)
	filter_frame.columnconfigure([0,1,2],minsize=50,weight=1)

	filter_label = tk.Label(filter_frame, text='Filter type')
	filter_label.grid(row=1,column=0)
	filter_pass = ttk.Combobox(filter_frame,values=['Low pass','High pass','Band pass'])
	filter_pass.grid(row=1,column=1)
	filter_pass.bind("<<ComboboxSelected>>", gray_out)
	low_label = tk.Label(filter_frame, text='Lower limit')
	low_value = tk.Entry(master=filter_frame,textvariable = tool_filter.low_val)
	low_label.grid(row=2,column=0)
	low_value.grid(row=2,column=1)
	high_label = tk.Label(filter_frame, text='Upper limit')
	high_value = tk.Entry(master=filter_frame,textvariable = tool_filter.high_val)
	high_label.grid(row=3,column=0)
	high_value.grid(row=3,column=1)




	filter_button = tk.Button(filter_frame,text='Filter traces',command= click)
	filter_button.grid(row=1,column=2,rowspan=3,sticky=tk.N+tk.S)

	toggle_ap = tk.BooleanVar()
	auto_filter = tk.Checkbutton(filter_frame,text='Automatic apply', var=toggle_ap,command=toggle_auto)
	auto_filter.grid(row=4,column=2)

# Filter function
# Actual function that filters and plots the result
def filter_fun(file_in,low_val,high_val):
	if plt.fignum_exists('Filtered data'):#if a filter plot already exists:
		filter_fun.fig3.clf() #clear previous plot
	in_data=obs.read(file_in) #read input trace/s
	filt_data = in_data.filter('bandpass',freqmin=float(low_val),freqmax=float(high_val)) #the filter is always a band pass. If high or low pass is selected then one of the limit values is very high or very low. This way is more efficient.
	filter_fun.fig3, _, _ =s_plt.plot(filt_data,spacing,time,"Filtered data")   #plot filtered data data



# Dromochrome tool
# This tool can be used to create a dromochrome plot by first break picking on traces (raw or filtered).
def tool_dromo():
	current_fig=plt.gcf()
	points=[]
	points_dromo=[]
	fig3,ax = plt.subplots(1,num='Dromochrome')
	ax.set_ylim(0,1500)
	ax.set_xlim(0,960)
	ax.set_xlabel('Space (m)')
	ax.set_ylabel('Time (s)')
	def pick(event):
		
		xdata = round(event.xdata,-1) #x mouse position is rounded to the "nearest" trace by rounding the units. This is NOT the best solution because I can still Dx!= 10. For now it will do.
		ydata = event.ydata #y mouse position
		if event.key == 'w': # if the w key was pressed (selected):
			point = plt.plot(xdata,ydata,'_r',markersize=7) #plot point
			points.append(point) #append point graph to the points list. Not the value but the point matplotlib object
			current_fig.canvas.draw()
			current_fig.canvas.flush_events()
			
			point_dromo=ax.plot(xdata,ydata,'or',markersize=3)# plot the same point on the dromochrome plot
			points_dromo.append(point_dromo)#append point graph to the dromochrome points list
			fig3.canvas.draw()
			fig3.canvas.flush_events()
		elif event.key == 'd': # if the d key was pressed (delete):
			for i,p in enumerate(points): #take the point list
				xp=p[0].get_xdata()[0] #take the current position
				yp=p[0].get_ydata()[0]
			#print(xdata,xp)
				if abs(xp-xdata) <=5 and abs(yp-ydata)<=5 : # if the |distance| between the point and the mouse position is less than 5: 
					p[0].remove() #remove the point object from the graph (p[0] because p is a list even if is only one point. I don't know why) 
					points_dromo[i][0].remove() #remove the same point from the dromochrome graph
					current_fig.canvas.draw() #refresh everything
					current_fig.canvas.flush_events()
					fig3.canvas.draw()
					fig3.canvas.flush_events()
		
	current_fig.canvas.mpl_connect('key_press_event',pick) #when a key is pressed the mouse position is registered
	fig3.show()




# file navigator
# This functions creates an interface that can be used to scroll files if more than one file is imported.

def file_import():
	file_import.tr_list = [] #list of displayed traces
	file_import.i=0 #counter for the navigator
	file_import.fig,file_import.ax=[],[]
	
	def call_disp(): #display button
		data = obs.read(file_import.file_path[file_import.i])
		#print(data)
		file_import.fig,file_import.ax,file_import.tr_list=s_plt.plot(data,spacing,time,"Raw data") #plot seismic data


	def next_file(): #next file
	
		file_import.i += 1
		
		if file_import.i > len(file_import.file_path)-1: #if the counter is higher than the number of imported files
			file_import.i = 0

		wd(name_frame) #clear the name frame (see below)
		file_name = os.path.basename(file_import.file_path[file_import.i])
		label_file = tk.Label(master=name_frame,text=f"analysing: {file_name}")
		label_file.pack()
		
		if plt.fignum_exists('Raw data'): #if raw data plot exists
			file_import.fig.clf() #clear it
			call_disp() #call the function
		if tool_filter.auto_ap: #if auto filtering is turned on then 
			filter_fun(file_import.file_path[file_import.i], tool_filter.low_val.get(), tool_filter.high_val.get()) #filter traces
	
	def previous_file():
		file_import.i-=1
		if file_import.i < 0: # if the index is less than 0
			file_import.i = len(file_import.file_path)-1 #set it to the highest index values (last file)	

		wd(name_frame)#clear the name frame (see below)
		file_name = os.path.basename(file_import.file_path[file_import.i])
		label_file = tk.Label(master=name_frame,text=f"analysing: {file_name}")
		label_file.pack()
		
		if plt.fignum_exists('Raw data'):#if raw data plot exists
			file_import.fig.clf()#clear it
			call_disp()#call the function
		if tool_filter.auto_ap:#if auto filtering is turned on then 
			filter_fun(file_import.file_path[file_import.i], tool_filter.low_val.get(), tool_filter.high_val.get())#filter traces
			
	tool_filter.auto_ap=False
	#clear everything
	wd(main_frame) 
	wd(tools_frame)
	#set the name frame (where the file name is displayed)
	name_frame = tk.Frame(master=main_frame)
	name_frame.pack(fill=tk.BOTH,expand=True)
	scroll_tool = tk.Frame(master=main_frame)
	scroll_tool.pack(fill=tk.BOTH,expand=True)
	
	#File import
	file_import.file_path=tk.filedialog.askopenfilenames()
	file_name = os.path.basename(file_import.file_path[file_import.i])#list of imported files paths

	#write the file name that's being analyzed 
	label_file = tk.Label(master=name_frame,text=f"analysing: {file_name}")
	label_file.pack()
	display_file = tk.Button(master=scroll_tool, text="Display data",command=call_disp)
	display_file.pack()
	
	#File scroll toolframe

	expl = tk.Frame(master=scroll_tool)
	expl.rowconfigure(0,minsize=50,weight=1)
	expl.columnconfigure([0,1,2],minsize=50,weight=1)
	prev_btn = tk.Button(master=expl,text='<< Previous',command=previous_file)
	prev_btn.grid(row=0, column=0)
	next_btn = tk.Button(master=expl,text='Next >>',command=next_file)
	next_btn.grid(row=0, column=2)
	expl.pack(fill=tk.BOTH,expand=True)


def file_export():
	print("export")
def file_exit():
	if messagebox.askokcancel("Exit","Do you want to exit?"):
		plt.close('all')
		window.destroy()




if __name__ == "__main__":
	
	# Menu entry
	
	file_dict = {

	"Import": file_import,
	"Export": file_export,
	"Exit": file_exit,
	}

	tools_dict = {

	"fft": tool_fft,
	"filter": tool_filter,
	"dromo": tool_dromo,
	}

	menu = [["File",file_dict],["Tools",tools_dict]]

	window = tk.Tk()
	window.geometry("400x500")

	menubar = tk.Menu(window)
	
	# cascading menu
	for entry in menu:
		menu_entry = tk.Menu(menubar,tearoff=0)
		for name,function in entry[1].items():
			menu_entry.add_command(label=name,command=function)
		menubar.add_cascade(label=entry[0],menu=menu_entry)

	window.config(menu=menubar)


	# define a main frame to which a secondary frame (tool frame) is attached. On the tool frame all of the tools can be attached
	main_frame = tk.Frame(master=window)
	main_frame.pack(fill=tk.BOTH,expand=True)
	tools_frame = tk.Frame(master=window)
	tools_frame.pack(fill=tk.BOTH,expand=True)	
    
	spacing = np.arange(0,960,10) # traces spacing, for now is fixed, IT SHOULD'NT BE.
	time = np.arange(1500) #fixed time spacing, potato potato
	window.protocol("WM_DELETE_WINDOW",file_exit) #when closed propt the exit warning
	window.mainloop()
