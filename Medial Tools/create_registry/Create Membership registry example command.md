# Create Membership registry example command
```bash
create_registry --rep ${REP_PATH} --registry_type keep_alive --registry_init "duration=${CONNECT_BUFFER};max_repo_date=${MAX_REP_DATE};secondry_start_buffer_duration=0;start_buffer_duration=0;end_buffer_duration=0;signal_list=${SIGNAL_LIST}" --registry_save $OUTPUT_PATH
```
Parameters explained:
- REP_PATH - repository path
- SIGNAL_LIST - list of signals with comma. Those list will be used to calculate membership, if there is event of either one of them, the membership signal will continue. Example: Hemoglobin,DIAGNOSIS,Drug,Glucose
- CONNECT_BUFFER - how many days to take from each "event" of signal appearance to consider the patient as a member - going forward. Example values: 365 or 730
- MAX_REP_DATE - maximal time of repository.

