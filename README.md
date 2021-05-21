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

+ Picking data exporter
+ Gain traces control
+ Other stuff
