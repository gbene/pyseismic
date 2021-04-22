import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack






def sp_analysis(sel_x,sel_y):#spectral analysis function (I do not remember how it works)
	#print(tr_list)
	fig2, ax2 = plt.subplots(1,num="Spectral analysis")

	s_r = 1000 #max frequency

	for i in sel_x:
		i_filt = [n-np.mean(i) for n in i]
		sel_x_fft = scipy.fftpack.rfft(np.transpose(i_filt))
		freq = np.linspace(0,s_r,len(i))
		ax2.plot(freq,np.abs(sel_x_fft)*(2/1500),'-')#dx =2, dt=1500?
		ax2.set_xlabel('Frequency')
		ax2.set_ylabel('Magnitude')
	fig2.show()
	return fig2,ax2
    
