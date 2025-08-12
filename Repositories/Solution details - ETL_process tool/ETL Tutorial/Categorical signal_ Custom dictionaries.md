# Categorical signal/ Custom dictionaries
# Use case 1 - Known/Uses signals that we have known ontologies
When you are going to use a "known" categorical signal from [ETL_INFRA_DIR](../High%20level%20-%20important%20paths/ETL_INFRA_DIR.md)/rep_signals/general.signals like "DIAGNOSIS" or "Drug" or "PROCEDURE", you will want to use known "ontologies" and mapping between codes.
For example RX_CODES to ATC.
The only thing you need to do in "prepare_final_signals" in the Drug signal is to create the values of the Drug signal with the right prefix. The ETL code will identify for example that you are using RX_CODE in Drug signal and will pull the RX_Code dictionary and the ATC codes dictionary and the mapping between RX_CODE to ATC. No need to do anything beside keeping the values with the right prefix. The call to "finish_prepare_load" will take care of that.
 
Here is a table of "Known" ontologies and their prefix:
<img src="/attachments/14811570/14811582.png"/>
# Use case 2 - new signal received from client, list of values
In this use case, we received list of values from client and there is no "known" ontology to be used, we didn't receive a mapping dictionary from client.  
For example "Cancer_Type" with "Adenocarcinoma", "Small_Cells", etc extracted from cancer patients./
We don't need to anything, we have defined a new categorical signal in [CODE_DIR](../High%20level%20-%20important%20paths/CODE_DIR.md)/configs/rep.signals and "finish_prepare_load" will identify those signals and will create the dictionary for us.
# Use case 3 - new/known signal, but with additional mapping information from client
In this use case we received a signal that might be "known" like DIAGNOSIS or new signal, and the client had provided us with external "dictionary".
For example - diagnosis codes are documented in "client's internal" coding system and we received a 2 dictionary :
1. Dictionary that translate the code values to their description. For example "EDG_CODE:1234" is Diabetes type II
2. Dictionary that translate the codes into other known coding system like ICD10 in this example. "EDG_CODE:1234" which is "Diabetes type II" is mapped to "ICD10_CODE:E11". The client can provide this dictionary or we can/need to create this our own.If this "ontology" is common and known, we might want to store the mapping dictionary in our ETL for future support in this type of ontology
In some cases we might only receive "internal" codes and "description, so might only have the optional Dictionary (#1) and without any mappings, that's also OK.
In other cases we might have just the "mappings", that's also OK,
 
We will need to use the function "[prepare_dicts](http://node-01/ETL_Infra/ETL_Infra.html#etl_process.prepare_dicts)" and pass the 2 dataframes.
The first optional dataframe is the "translation" dict - from internal codes to description - a dataframe with 2 columns: code,description. 
The second optional dataframe is "mapping" dict - from the code/value we recieved from client to our known ontologies codes - a dataframe with 2 columns: client value, our coding ontology.
 
# Howto read the output of prepare_dicts/finish_prepare_load
TODO: complete. [itamar Menuhin](https://www.linkedin.com/in/itamar-menuhin-932252a7/)
 
 
 
 
 
