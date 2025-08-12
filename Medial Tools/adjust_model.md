# adjust_model
Template for adding pre processors json:

## **adding rep_processors json template**
```json
{ "pre_processors" : [
  {
    "action_type":"rp_set",
    "members":[
       // Add your blocks in here
    ]
  }
] }
```
**Caution**:
When adding "pre_processros" with "rp_set" - all the rep processors are added in the END of the existing model rep proceossors. 
When using single "rep_processor" in action type, the single rep_processor is added in the begining.
 
Template for adding post processors json:
## **Json for adding post_processors**
```json
{ "post_processors": [
         // Add your blocks in here
] }
```
 
change_model_info examples can be shown in [change_model](change_model)
