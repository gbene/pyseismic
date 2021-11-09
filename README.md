# pyseismic


Pyseismic is a simple python interface created to visualize and process seismic traces based on the Obspy package (https://docs.obspy.org/). The aim of this project is to create a simple alternative to the more complex and _costly_ Visual SUNT (http://www.wgeosoft.ch/PDF/Visual_SUNT_Pro_Data.html) that can be used to do basic taks without the need to buy professional softwares. Since is entirely written in pyhon it can be run on every platform (Visual SUNT is only on Windows D:).

## Functions
The available functions are:

+ Raw data visualizer
+ FFT analyzer and trace filtering
+ Frist break picking and dromochrome plotting

## Dipendencies

+ Obspy:

```
pip install obspy
```

+ Numpy:

```
pip install numpy
```

+ Scipy:

```
pip install scipy
```

## Todolist

1. Automatic first break
2. Trace muting
3. More precise import options (as for now it relies on the autodetect features of Obspy) 
4. Simple stratigraphic model reconstruction (from dromochrome elaboration)
5. Delaytime and GRM applications
6. SRCS
7. Focal mechanism reconstruction
