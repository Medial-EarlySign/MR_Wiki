# Data json file format
```
{
	"patient_id": 1,
	"signals": [
		{ SIGNAL_CODE_BLOCK },
		{ SIGNAL_CODE_BLOCK },
		...
	]
}
```
 
```
SIGNAL_CODE_BLOCK structure:
```
```
{
    "code": "SINGAL_NAME",
    "data": [
     {
      "timestamp": [ 20120902, ADDITIONAL_TIME_CHANNELES if has ],
      "value": [ "51", ADDITIONAL_VALUE_CHANNELES if has ]
     },
	... ADDIOTNAL data points if has
    ]
}
```
 
Can also be encapsulated my "multiple" attribute for array of patients like
```
{ 
"multiple": [
	{PATIENT BLOCK}
]
}
```
