# RepBasicOutlierCleaner
### [RepBasicOutlierCleaner ](http://node-04/Libs/html/classRepBasicOutlierCleaner)is a point-wise cleaner of outliers
Each value of a given signal is considered with respect to two ranges. First, the values is compared to the 'Remove' range, and if outside, it is deleted. Otherwise, it is compare to the 'Trim' range and clipped if outside (i.e. - assigned the upper limit if larger, and the lower limit if smaller). The 'Remove' and 'Trim' ranges are learnt from data, using the methods of [MedValueCleaner](../MedValueCleaner).
### Include file is - H:/MR/Libs/Internal/MedUtils/MedProcessTools/RepProcess.h
 
### OutlierSampleFilter initialization: see [**MedValueCleaner**](./MedValueCleaner).
