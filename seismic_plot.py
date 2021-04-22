
#Function used to properly plot seismic traces 

#Imports
import numpy as np
import matplotlib.pyplot as plt


ax = []

def plot(data,spacing,time,name):
	#global ax,tr_list

	fig, ax = plt.subplots(1,num=name) #make plot with name as input

	tr_list=[]


	for i,tr in enumerate(data):
		tr_data = tr.data 
		tr_final= spacing[i]+((tr_data)/(np.max(tr_data)*0.2)) #signal amplifier (without it further traces are less visibile).
		tr_list.append(tr_final) #list that can be used elsewhere (e.g. fft)
		ax.plot(tr_final,time,'k-') #plot traces as lines
		ax.fill_betweenx(time, spacing[i], tr_final, where=(tr_final>=spacing[i]),facecolor='k',interpolate=True)#black fill "positive" peaks.

	ax.set_ylim(1500,0)
	ax.set_xlabel('Space (m)')
	ax.set_ylabel('Time (s)')
	fig.show()
	return fig,ax,tr_list
    
    
