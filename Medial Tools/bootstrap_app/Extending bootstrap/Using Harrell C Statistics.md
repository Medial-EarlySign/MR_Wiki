# Using Harrell C Statistics
 
activate:
```bash
bootstrap_app --measurement_type "calc_harrell_c_statistic"
```
Encoding samples for harrell's c Statistics:

* Case/Control => effect outcome/y sign. positive is case, negative controls. Can't handle event in time zero.
* Time to event => abs value of outcome/y
* Score => the prediction

