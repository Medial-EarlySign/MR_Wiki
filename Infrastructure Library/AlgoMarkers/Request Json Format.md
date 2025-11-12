## AlgoMarker Request Format

For complete details, see the [AlgoMarker Spec](../../SharePoint_Documents/General/AlgoMarker/RDG-04-11-33%20AM%20Library%20SW%20Version%201.1%20Software%20Design%20Document%20-%20Rev%20D.docx).

### Required Fields

A valid request to AlgoMarker should include the following fields:

- **type**: Set to `"request"`.
- **request_id**: A unique string identifier for the request.
- **export**: Specifies the desired output. For standard predictions, use `"prediction": "pred_0"` to request the model prediction and store it in the `"prediction"` field of the response. You can also specify request to recieve explainabiltiy output if applicable for example by specifiying `"explainability_output_field_name_for_your_control": "json_attr Tree_iterative_covariance"`.
- **load**: Set to `1` to indicate that patient data is included in the request.
- **flag_threshold** (optional): If your model supports configurable thresholds, specify the threshold name here.
- **requests**: An array of patient requests, each containing:
    - **patient_id**: An integer patient identifier.
    - **time**: The calculation date in `YYYYMMDD` format. Any data after this date will be ignored from score calculation.
    - **data**: Patient data, including:
        - **signals**: An array of signal objects, each with:
            - **code**: The signal name.
            - **data**: An array of data points, each with:
                - **timestamp**: An array of timestamps (e.g., `[20250806]`). Can be empty for static values.
                - **value**: An array of values (e.g., `["14.5"]` or `[82]`). You can pass string/float, both OK.
            - **unit** (optional): The unit for the signal (e.g., `"fL"`).

#### Example Signal Entry
```json title="Example Signal Entry"
{
    "type": "request",
    "request_id": "999ef0f4-1099-4178-8c86-ecbfac6578e2",
    "export": {
        "prediction": "pred_0"
    },
    "flag_threshold": "USPSTF_50-80$PR_03.000",
    "load": 1,
    "requests": [
        {
            "time": "20250806",
            "patient_id": "1",
            "data": {
                "signals": [
                    {
                        "code": "Hemoglobin",
                        "data": [
                            {
                                "value": [
                                    "14.5"
                                ],
                                "timestamp": [
                                    20250806
                                ]
                            }
                        ],
                        "unit": "fL"
                    },
                    {
                        "code": "Hematocrit",
                        "data": [
                            {
                                "value": [
                                    "32"
                                ],
                                "timestamp": [
                                    20250806
                                ]
                            }
                        ],
                        "unit": "fL"
                    },
                    {
                        "code": "RBC",
                        "data": [
                            {
                                "value": [
                                    "40000.5"
                                ],
                                "timestamp": [
                                    20230806
                                ]
                            },
                            {
                                "value": [
                                    "4.5"
                                ],
                                "timestamp": [
                                    20250806
                                ]
                            }
                        ],
                        "unit": "fL"
                    },
                    {
                        "code": "MCV",
                        "data": [
                            {
                                "value": [
                                    82
                                ],
                                "timestamp": [
                                    20250806
                                ]
                            }
                        ],
                        "unit": "fL"
                    },
                    {
                        "code": "GENDER",
                        "data": [
                            {
                                "value": [
                                    "Male"
                                ],
                                "timestamp": []
                            }
                        ]
                    },
                    {
                        "code": "BDATE",
                        "data": [
                            {
                                "value": [
                                    19780101
                                ],
                                "timestamp": []
                            }
                        ]
                    }
                ]
            }
        }
    ]
}
```