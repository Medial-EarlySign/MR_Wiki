# Howto Use AlgoMarker

## How to Deploy AlgoMarker

This guide explains how to set up AlgoMarker to run and expose a predictive model API.

### 1. **Obtain the Model**
- For public models, simply download the directory containing the model and its configuration files. [Full List of Models](../../Models)
- For your own model, you’ll need to create a configuration file.  
  See: [Setup a new AlgoMarker](Setup%20a%20new%20AlgoMarker.md)

### 2. **Build the AlgoMarker Library**
- Follow the [AlgoMarker Library Setup](../../New%20employee%20landing%20page/index.md#1-algomarker-library) to build the `libdyn_AlgoMarker.so` library, or use a pre-built version if available.

### 3. **Build AlgoMarker_Server**
- Follow the [AlgoMarker_Server Setup](../../New%20employee%20landing%20page/index.md#2-algomarker-wrapper) to build `AlgoMarker_Server`, or use an existing compiled binary.

### 4. **Run the Server**
You can run the server either locally or using Docker.

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
More details can be found [here](/Python/Medial's%20C++%20API%20in%20Python/Python%20AlgoMarker%20API%20Wrapper.html)

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
   docker build -t algomarker_X --no-cache .
   ```

4. **Run a Container**
   execute this command `docker run -id algomarker_X --name algomarker_container_X -p 1234:1234` and expose port 1234 to 1234 in your local machine.

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
Additional fields may be included in the response, for example, if explainability is requested.

For the full API specification, refer to:  
[AlgoMarker Spec](/SharePoint_Documents/General/AlgoMarker/RDG-04-11-33%20AM%20Library%20SW%20Version%201.1%20Software%20Design%20Document%20-%20Rev%20D.docx)