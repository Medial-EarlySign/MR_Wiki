# Howto Use AlgoMarker

## How to Deploy AlgoMarker

This guide explains how to set up AlgoMarker to run and expose a predictive model API.

### 1. **Obtain the Model**
- For public models, simply download the directory containing the model and its configuration files. [Full List of Models](../../Models)
- For your own model, you’ll need to create a configuration file.  
  See: [Setup a new AlgoMarker](Setup%20a%20new%20AlgoMarker.md)

### 2. **Build the AlgoMarker Library**
- Follow the [AlgoMarker Library Setup](../../Installation/index.md#1-algomarker-library) to build the `libdyn_AlgoMarker.so` library, or use a pre-built version if available.

### 3. **Build AlgoMarker_Server**
- Follow the [AlgoMarker_Server Setup](../../Installation/index.md#2-algomarker-wrapper) to build `AlgoMarker_Server`, or use an existing compiled binary.

### 4. **Run the Server**
You can run the server either locally or using Docker/Podman.

#### Local Server
Run the following command, adjusting the port as needed:
```bash
AlgoMarker_Server --algomarker_path $PATH_TO_AM_CONFIG_FILE --port 1234
# If the AlgoMarker library (`libdyn_AlgoMarker.so`) is not in a "lib" directory next to the config file,
# specify its location with the "--library_path" argument.
```
Alternatively, you can use the Python wrapper with FastAPI to expose the AlgoMarker model.  
**Note:** The Python wrapper is slower, requires a larger setup, and depends on Python and its libraries. In contrast, `AlgoMarker_Server` only needs glibc and can run in a minimal (distroless) image. However, the Python wrapper allows for easier code modifications and supports legacy ColonFlag models.

To use the Python wrapper, run [`run_server.sh`](https://github.com/Medial-EarlySign/MR_Tools/blob/main/AlgoMarker_python_API/run_server.sh) after setting `AM_CONFIG` and `AM_LIB` in the script. Clone the repository containing `run_server.sh` if needed.
More details can be found [here](../../Medial%20Tools/Python/Python%20AlgoMarker%20API%20Wrapper.md)

#### Using Docker

1. **Create a Base Image**  
   - The recommended base is the chiselled Ubuntu image (~10MB, minimal attack surface).
   - Alternatively, use a full Ubuntu image and add the following to your Dockerfile:
     ```bash
     apt-get update && apt-get install libgomp1 -y
     ```
   - To build the chiselled Ubuntu image, run `create.sh` in [Docker/chiselled-ubuntu](https://github.com/Medial-EarlySign/MR_Scripts/tree/main/Docker/chiselled-ubuntu).

2. **Prepare the Application Directory**  
   - Copy the AlgoMarker directory into the `data/app` folder next to your Dockerfile. Ensure `libdyn_AlgoMarker.so` is in a `lib` directory next to the `.amconfig` file.
   - Copy the `AlgoMarker_Server` binary into `data/app`.

3. **Build the Docker Image**  
   Use the following Dockerfile template:
   ```Dockerfile
   FROM chiselled-ubuntu:latest

   COPY data /

   ENTRYPOINT [ "/app/AlgoMarker_Server", "--algomarker_path", "/app/PATH_TO_AM_CONFIG_FILE", "--port", "1234", "--no_print", "1" ]
   ```
   Adjust `PATH_TO_AM_CONFIG_FILE` and the port as needed. You can also specify the path to `libdyn_AlgoMarker.so` using the `--library_path` argument.

   Build the image with:
   ```bash
   podman build -t algomarker_X --no-cache .
   ```
   You can also use `create_image.sh` [helper script](https://github.com/Medial-EarlySign/MR_Scripts/tree/main/Docker/AlgoMarker_Server) to generate the AlgoMarker

4. **Run a Container**
   execute this command `podman run -id algomarker_X --name algomarker_container_X -p 1234:1234` and expose port 1234 to 1234 in your local machine.

> [!NOTE] You can replace all the `podman` commands with `docker`, it is fully compatible.

---
## How to Use the Deployed AlgoMarker

Once the server is running, it exposes two main API endpoints:

1. **GET `/discovery`**  
   - No parameters required.
   - Returns a JSON specification describing the AlgoMarker (name, inputs, etc.).

2. **POST `/calculate`**  
   - Accepts a JSON request with either a single patient or a batch of patients.
   - Request format details: [Request json format](Request%20Json%20Format.md)

**Example Response:**
```json title="Example Response"
{
  "type": "response",
  "request_id": "999ef0f4-1099-4178-8c86-ecbfac6578e2",
  "responses": [
    {
      "patient_id": "1",
      "time": "20250806",
      "prediction": "0.004082",
      "flag_threshold": "USPSTF_50-80$PR_03.000",
      "flag_result": 0,
      "messages": [
        "(320)An outlier was found and ignored in signal: RBC"
      ]
    }
  ]
}
```


<details>
<summary>Response with Explainability</summary>

```json
{
	"type": "response",
	"request_id": "999ef0f4-1099-4178-8c86-ecbfac6578e2",
	"responses": [
		{
			"patient_id": "1",
			"time": "20230611",
			"messages": [
				"(320)An outlier was found and ignored in signal: RBC",
			],
			"prediction": "0.004082",
			"explainability_output_field_name_for_your_control": {
				"static_info": [
					{
						"signal": "Age",
						"unit": "Year",
						"value": "45"
					},
					{
						"signal": "GENDER",
						"unit": "",
						"value": "1.000000"
					},
					{
						"signal": "Hemoglobin",
						"unit": "g/dL",
						"value": "14.500000"
					}
				],
				"explainer_output": [
					{
						"contributor_name": "Age",
						"contributor_value": -1.257716417312622,
						"contributor_percentage": 42.327555760464165,
						"contributor_elements": [
							{
								"feature_name": "Age",
								"feature_value": 45.0
							}
						],
						"contributor_description": "",
						"contributor_level": 2,
						"contributor_level_max": 4,
						"contributor_records": [
							{
								"signal": "Age",
								"unit": [
									"Year"
								],
								"timestamp": [],
								"value": [
									"45.000000"
								]
							}
						]
					},
					{
						"contributor_name": "MCH_Values",
						"contributor_value": -0.2684820294380188,
						"contributor_percentage": 9.035572693121699,
						"contributor_elements": [
							{
								"feature_name": "FTR_000008.MCH.last.win_0_10000",
								"feature_value": 32.21999740600586
							},
							{
								"feature_name": "FTR_000019.MCH.last.win_0_1000",
								"feature_value": 32.21999740600586
							},
							{
								"feature_name": "FTR_000030.MCH.last.win_0_730",
								"feature_value": 32.21999740600586
							},
							{
								"feature_name": "FTR_000041.MCH.last.win_0_360",
								"feature_value": 32.21999740600586
							},
							{
								"feature_name": "FTR_000052.MCH.last.win_0_180",
								"feature_value": 32.21999740600586
							},
							{
								"feature_name": "FTR_000118.MCH.first.win_0_10000",
								"feature_value": 32.21999740600586
							},
							{
								"feature_name": "FTR_000129.MCH.first.win_0_1000",
								"feature_value": 32.21999740600586
							},
							{
								"feature_name": "FTR_000140.MCH.first.win_0_730",
								"feature_value": 32.21999740600586
							},
							{
								"feature_name": "FTR_000151.MCH.first.win_0_360",
								"feature_value": 32.21999740600586
							},
							{
								"feature_name": "FTR_000162.MCH.first.win_0_180",
								"feature_value": 32.21999740600586
							},
							{
								"feature_name": "FTR_000173.MCH.last2.win_0_10000",
								"feature_value": 29.091323852539063
							},
							{
								"feature_name": "FTR_000184.MCH.last2.win_0_1000",
								"feature_value": 29.041757583618164
							},
							{
								"feature_name": "FTR_000195.MCH.last2.win_0_730",
								"feature_value": 29.01051139831543
							},
							{
								"feature_name": "FTR_000206.MCH.last2.win_0_360",
								"feature_value": 28.922163009643555
							},
							{
								"feature_name": "FTR_000217.MCH.last2.win_0_180",
								"feature_value": 28.734722137451172
							},
							{
								"feature_name": "FTR_000228.MCH.avg.win_0_10000",
								"feature_value": 32.21999740600586
							},
							{
								"feature_name": "FTR_000239.MCH.avg.win_0_1000",
								"feature_value": 32.21999740600586
							},
							{
								"feature_name": "FTR_000250.MCH.avg.win_0_730",
								"feature_value": 32.21999740600586
							},
							{
								"feature_name": "FTR_000261.MCH.avg.win_0_360",
								"feature_value": 32.21999740600586
							},
							{
								"feature_name": "FTR_000272.MCH.avg.win_0_180",
								"feature_value": 32.21999740600586
							},
							{
								"feature_name": "FTR_000283.MCH.min.win_0_10000",
								"feature_value": 32.21999740600586
							},
							{
								"feature_name": "FTR_000294.MCH.min.win_0_1000",
								"feature_value": 32.21999740600586
							},
							{
								"feature_name": "FTR_000305.MCH.min.win_0_730",
								"feature_value": 32.21999740600586
							},
							{
								"feature_name": "FTR_000316.MCH.min.win_0_360",
								"feature_value": 32.21999740600586
							},
							{
								"feature_name": "FTR_000327.MCH.min.win_0_180",
								"feature_value": 32.21999740600586
							},
							{
								"feature_name": "FTR_000338.MCH.max.win_0_10000",
								"feature_value": 32.21999740600586
							},
							{
								"feature_name": "FTR_000349.MCH.max.win_0_1000",
								"feature_value": 32.21999740600586
							},
							{
								"feature_name": "FTR_000360.MCH.max.win_0_730",
								"feature_value": 32.21999740600586
							},
							{
								"feature_name": "FTR_000371.MCH.max.win_0_360",
								"feature_value": 32.21999740600586
							},
							{
								"feature_name": "FTR_000382.MCH.max.win_0_180",
								"feature_value": 32.21999740600586
							},
							{
								"feature_name": "FTR_000503.MCH.last2_time.win_0_10000",
								"feature_value": 449.85882568359375
							},
							{
								"feature_name": "FTR_000514.MCH.last2_time.win_0_1000",
								"feature_value": 315.7171325683594
							},
							{
								"feature_name": "FTR_000525.MCH.last2_time.win_0_730",
								"feature_value": 268.54010009765625
							},
							{
								"feature_name": "FTR_000536.MCH.last2_time.win_0_360",
								"feature_value": 161.85084533691406
							},
							{
								"feature_name": "FTR_000547.MCH.last2_time.win_0_180",
								"feature_value": 85.85099792480469
							},
							{
								"feature_name": "FTR_001148.MCH.last.win_730_10000",
								"feature_value": 29.159976959228516
							},
							{
								"feature_name": "FTR_001159.MCH.min.win_730_10000",
								"feature_value": 28.687816619873047
							},
							{
								"feature_name": "FTR_001170.MCH.max.win_730_10000",
								"feature_value": 29.749162673950195
							},
							{
								"feature_name": "FTR_001208.MCH.Estimate.180",
								"feature_value": 28.93360137939453
							},
							{
								"feature_name": "FTR_001208.MCH.Estimate.360",
								"feature_value": 28.951967239379883
							},
							{
								"feature_name": "FTR_001208.MCH.Estimate.730",
								"feature_value": 28.965957641601563
							}
						],
						"contributor_description": "",
						"contributor_level": 1,
						"contributor_level_max": 4,
						"contributor_records": [],
						"contributor_records_info": {
							"contributor_max_time": 1825,
							"contributor_max_time_unit": "Days",
							"contributor_max_count": 3
						}
					},
					{
						"contributor_name": "MCV_Values",
						"contributor_value": -0.1519976258277893,
						"contributor_percentage": 5.11537231036717,
						"contributor_elements": [
							{
								"feature_name": "FTR_000007.MCV.last.win_0_10000",
								"feature_value": 82.0
							},
							{
								"feature_name": "FTR_000018.MCV.last.win_0_1000",
								"feature_value": 82.0
							},
							{
								"feature_name": "FTR_000029.MCV.last.win_0_730",
								"feature_value": 82.0
							},
							{
								"feature_name": "FTR_000040.MCV.last.win_0_360",
								"feature_value": 82.0
							},
							{
								"feature_name": "FTR_000051.MCV.last.win_0_180",
								"feature_value": 82.0
							},
							{
								"feature_name": "FTR_000117.MCV.first.win_0_10000",
								"feature_value": 82.0
							},
							{
								"feature_name": "FTR_000128.MCV.first.win_0_1000",
								"feature_value": 82.0
							},
							{
								"feature_name": "FTR_000139.MCV.first.win_0_730",
								"feature_value": 82.0
							},
							{
								"feature_name": "FTR_000150.MCV.first.win_0_360",
								"feature_value": 82.0
							},
							{
								"feature_name": "FTR_000161.MCV.first.win_0_180",
								"feature_value": 82.0
							},
							{
								"feature_name": "FTR_000172.MCV.last2.win_0_10000",
								"feature_value": 87.35523986816406
							},
							{
								"feature_name": "FTR_000183.MCV.last2.win_0_1000",
								"feature_value": 87.30293273925781
							},
							{
								"feature_name": "FTR_000194.MCV.last2.win_0_730",
								"feature_value": 87.2611312866211
							},
							{
								"feature_name": "FTR_000205.MCV.last2.win_0_360",
								"feature_value": 87.1921615600586
							},
							{
								"feature_name": "FTR_000216.MCV.last2.win_0_180",
								"feature_value": 86.85134887695313
							},
							{
								"feature_name": "FTR_000227.MCV.avg.win_0_10000",
								"feature_value": 82.0
							},
							{
								"feature_name": "FTR_000238.MCV.avg.win_0_1000",
								"feature_value": 82.0
							},
							{
								"feature_name": "FTR_000249.MCV.avg.win_0_730",
								"feature_value": 82.0
							},
							{
								"feature_name": "FTR_000260.MCV.avg.win_0_360",
								"feature_value": 82.0
							},
							{
								"feature_name": "FTR_000271.MCV.avg.win_0_180",
								"feature_value": 82.0
							},
							{
								"feature_name": "FTR_000282.MCV.min.win_0_10000",
								"feature_value": 82.0
							},
							{
								"feature_name": "FTR_000293.MCV.min.win_0_1000",
								"feature_value": 82.0
							},
							{
								"feature_name": "FTR_000304.MCV.min.win_0_730",
								"feature_value": 82.0
							},
							{
								"feature_name": "FTR_000315.MCV.min.win_0_360",
								"feature_value": 82.0
							},
							{
								"feature_name": "FTR_000326.MCV.min.win_0_180",
								"feature_value": 82.0
							},
							{
								"feature_name": "FTR_000337.MCV.max.win_0_10000",
								"feature_value": 82.0
							},
							{
								"feature_name": "FTR_000348.MCV.max.win_0_1000",
								"feature_value": 82.0
							},
							{
								"feature_name": "FTR_000359.MCV.max.win_0_730",
								"feature_value": 82.0
							},
							{
								"feature_name": "FTR_000370.MCV.max.win_0_360",
								"feature_value": 82.0
							},
							{
								"feature_name": "FTR_000381.MCV.max.win_0_180",
								"feature_value": 82.0
							},
							{
								"feature_name": "FTR_000502.MCV.last2_time.win_0_10000",
								"feature_value": 449.8634948730469
							},
							{
								"feature_name": "FTR_000513.MCV.last2_time.win_0_1000",
								"feature_value": 315.7387390136719
							},
							{
								"feature_name": "FTR_000524.MCV.last2_time.win_0_730",
								"feature_value": 268.5698547363281
							},
							{
								"feature_name": "FTR_000535.MCV.last2_time.win_0_360",
								"feature_value": 161.91400146484375
							},
							{
								"feature_name": "FTR_000546.MCV.last2_time.win_0_180",
								"feature_value": 85.87918853759766
							},
							{
								"feature_name": "FTR_001147.MCV.last.win_730_10000",
								"feature_value": 87.29901123046875
							},
							{
								"feature_name": "FTR_001158.MCV.min.win_730_10000",
								"feature_value": 85.86404418945313
							},
							{
								"feature_name": "FTR_001169.MCV.max.win_730_10000",
								"feature_value": 88.5106430053711
							},
							{
								"feature_name": "FTR_001207.MCV.Estimate.180",
								"feature_value": 87.37998962402344
							},
							{
								"feature_name": "FTR_001207.MCV.Estimate.360",
								"feature_value": 87.38853454589844
							},
							{
								"feature_name": "FTR_001207.MCV.Estimate.730",
								"feature_value": 87.39167022705078
							}
						],
						"contributor_description": "",
						"contributor_level": 1,
						"contributor_level_max": 4,
						"contributor_records": [
							{
								"signal": "MCV",
								"unit": [
									"fL"
								],
								"timestamp": [
									20230611
								],
								"value": [
									"82.000000"
								]
							}
						],
						"contributor_records_info": {
							"contributor_max_time": 1825,
							"contributor_max_time_unit": "Days",
							"contributor_max_count": 3
						}
					},
					{
						"contributor_name": "MCH_Trends",
						"contributor_value": -0.14473219215869904,
						"contributor_percentage": 4.8708592685138346,
						"contributor_elements": [
							{
								"feature_name": "FTR_000063.MCH.slope.win_0_10000",
								"feature_value": -0.09105083346366882
							},
							{
								"feature_name": "FTR_000074.MCH.slope.win_0_1000",
								"feature_value": -0.03978761285543442
							},
							{
								"feature_name": "FTR_000085.MCH.slope.win_0_730",
								"feature_value": -0.008064992725849152
							},
							{
								"feature_name": "FTR_000096.MCH.slope.win_0_360",
								"feature_value": 0.014474527910351753
							},
							{
								"feature_name": "FTR_000107.MCH.slope.win_0_180",
								"feature_value": -0.00038833924918435514
							},
							{
								"feature_name": "FTR_000393.MCH.std.win_0_10000",
								"feature_value": 0.5682898759841919
							},
							{
								"feature_name": "FTR_000404.MCH.std.win_0_1000",
								"feature_value": 0.4634387791156769
							},
							{
								"feature_name": "FTR_000415.MCH.std.win_0_730",
								"feature_value": 0.436860591173172
							},
							{
								"feature_name": "FTR_000426.MCH.std.win_0_360",
								"feature_value": 0.3896379768848419
							},
							{
								"feature_name": "FTR_000437.MCH.std.win_0_180",
								"feature_value": 0.35533618927001953
							},
							{
								"feature_name": "FTR_000558.MCH.last_delta.win_0_10000",
								"feature_value": -0.06643807888031006
							},
							{
								"feature_name": "FTR_000569.MCH.last_delta.win_0_1000",
								"feature_value": -0.03644682839512825
							},
							{
								"feature_name": "FTR_000580.MCH.last_delta.win_0_730",
								"feature_value": -0.024617791175842285
							},
							{
								"feature_name": "FTR_000591.MCH.last_delta.win_0_360",
								"feature_value": 0.008983400650322437
							},
							{
								"feature_name": "FTR_000602.MCH.last_delta.win_0_180",
								"feature_value": 0.0546439066529274
							},
							{
								"feature_name": "FTR_001108.MCH.win_delta.win_0_180_360_10000",
								"feature_value": -0.12988980114459991
							},
							{
								"feature_name": "FTR_001128.MCH.win_delta.win_0_180_730_10000",
								"feature_value": -0.1698904186487198
							}
						],
						"contributor_description": "",
						"contributor_level": 1,
						"contributor_level_max": 4,
						"contributor_records": [],
						"contributor_records_info": {
							"contributor_max_time": 1825,
							"contributor_max_time_unit": "Days",
							"contributor_max_count": 3
						}
					},
					{
						"contributor_name": "MCHC-M_Values",
						"contributor_value": -0.13522081077098846,
						"contributor_percentage": 4.550760668340038,
						"contributor_elements": [
							{
								"feature_name": "FTR_000009.MCHC-M.last.win_0_10000",
								"feature_value": 45.30999755859375
							},
							{
								"feature_name": "FTR_000020.MCHC-M.last.win_0_1000",
								"feature_value": 45.30999755859375
							},
							{
								"feature_name": "FTR_000031.MCHC-M.last.win_0_730",
								"feature_value": 45.30999755859375
							},
							{
								"feature_name": "FTR_000042.MCHC-M.last.win_0_360",
								"feature_value": 45.30999755859375
							},
							{
								"feature_name": "FTR_000053.MCHC-M.last.win_0_180",
								"feature_value": 45.30999755859375
							},
							{
								"feature_name": "FTR_000119.MCHC-M.first.win_0_10000",
								"feature_value": 45.30999755859375
							},
							{
								"feature_name": "FTR_000130.MCHC-M.first.win_0_1000",
								"feature_value": 45.30999755859375
							},
							{
								"feature_name": "FTR_000141.MCHC-M.first.win_0_730",
								"feature_value": 45.30999755859375
							},
							{
								"feature_name": "FTR_000152.MCHC-M.first.win_0_360",
								"feature_value": 45.30999755859375
							},
							{
								"feature_name": "FTR_000163.MCHC-M.first.win_0_180",
								"feature_value": 45.30999755859375
							},
							{
								"feature_name": "FTR_000174.MCHC-M.last2.win_0_10000",
								"feature_value": 33.27936935424805
							},
							{
								"feature_name": "FTR_000185.MCHC-M.last2.win_0_1000",
								"feature_value": 33.24119186401367
							},
							{
								"feature_name": "FTR_000196.MCHC-M.last2.win_0_730",
								"feature_value": 33.22017288208008
							},
							{
								"feature_name": "FTR_000207.MCHC-M.last2.win_0_360",
								"feature_value": 33.142608642578125
							},
							{
								"feature_name": "FTR_000218.MCHC-M.last2.win_0_180",
								"feature_value": 33.04962158203125
							},
							{
								"feature_name": "FTR_000229.MCHC-M.avg.win_0_10000",
								"feature_value": 45.30999755859375
							},
							{
								"feature_name": "FTR_000240.MCHC-M.avg.win_0_1000",
								"feature_value": 45.30999755859375
							},
							{
								"feature_name": "FTR_000251.MCHC-M.avg.win_0_730",
								"feature_value": 45.30999755859375
							},
							{
								"feature_name": "FTR_000262.MCHC-M.avg.win_0_360",
								"feature_value": 45.30999755859375
							},
							{
								"feature_name": "FTR_000273.MCHC-M.avg.win_0_180",
								"feature_value": 45.30999755859375
							},
							{
								"feature_name": "FTR_000284.MCHC-M.min.win_0_10000",
								"feature_value": 45.30999755859375
							},
							{
								"feature_name": "FTR_000295.MCHC-M.min.win_0_1000",
								"feature_value": 45.30999755859375
							},
							{
								"feature_name": "FTR_000306.MCHC-M.min.win_0_730",
								"feature_value": 45.30999755859375
							},
							{
								"feature_name": "FTR_000317.MCHC-M.min.win_0_360",
								"feature_value": 45.30999755859375
							},
							{
								"feature_name": "FTR_000328.MCHC-M.min.win_0_180",
								"feature_value": 45.30999755859375
							},
							{
								"feature_name": "FTR_000339.MCHC-M.max.win_0_10000",
								"feature_value": 45.30999755859375
							},
							{
								"feature_name": "FTR_000350.MCHC-M.max.win_0_1000",
								"feature_value": 45.30999755859375
							},
							{
								"feature_name": "FTR_000361.MCHC-M.max.win_0_730",
								"feature_value": 45.30999755859375
							},
							{
								"feature_name": "FTR_000372.MCHC-M.max.win_0_360",
								"feature_value": 45.30999755859375
							},
							{
								"feature_name": "FTR_000383.MCHC-M.max.win_0_180",
								"feature_value": 45.30999755859375
							},
							{
								"feature_name": "FTR_000504.MCHC-M.last2_time.win_0_10000",
								"feature_value": 449.85882568359375
							},
							{
								"feature_name": "FTR_000515.MCHC-M.last2_time.win_0_1000",
								"feature_value": 315.7171325683594
							},
							{
								"feature_name": "FTR_000526.MCHC-M.last2_time.win_0_730",
								"feature_value": 268.54010009765625
							},
							{
								"feature_name": "FTR_000537.MCHC-M.last2_time.win_0_360",
								"feature_value": 161.85084533691406
							},
							{
								"feature_name": "FTR_000548.MCHC-M.last2_time.win_0_180",
								"feature_value": 85.85099792480469
							},
							{
								"feature_name": "FTR_001149.MCHC-M.last.win_730_10000",
								"feature_value": 33.386741638183594
							},
							{
								"feature_name": "FTR_001160.MCHC-M.min.win_730_10000",
								"feature_value": 33.00123977661133
							},
							{
								"feature_name": "FTR_001171.MCHC-M.max.win_730_10000",
								"feature_value": 33.99413299560547
							},
							{
								"feature_name": "FTR_001209.MCHC-M.Estimate.180",
								"feature_value": 33.09005355834961
							},
							{
								"feature_name": "FTR_001209.MCHC-M.Estimate.360",
								"feature_value": 33.112545013427734
							},
							{
								"feature_name": "FTR_001209.MCHC-M.Estimate.730",
								"feature_value": 33.133628845214844
							}
						],
						"contributor_description": "",
						"contributor_level": 1,
						"contributor_level_max": 4,
						"contributor_records": [],
						"contributor_records_info": {
							"contributor_max_time": 1825,
							"contributor_max_time_unit": "Days",
							"contributor_max_count": 3
						}
					}
				]
			}
		}
	]
}
```
</details>

* Nagative `contributor_value` means the concept resulted in lower score, positive value means the concept contributed to increas risk score
* The contribution magnitude is reported as `contributor_level` and the maximal scale is `contributor_level_max`. Since `contributor_value` magnitude is hard to interapt we used those scaling to report contribution magnitude 

Additional fields may be included in the response, for example, if explainability is requested.

For the full API specification, refer to:  
[AlgoMarker Spec](../../SharePoint_Documents/General/AlgoMarker/RDG-04-11-33%20AM%20Library%20SW%20Version%201.1%20Software%20Design%20Document%20-%20Rev%20D.docx)