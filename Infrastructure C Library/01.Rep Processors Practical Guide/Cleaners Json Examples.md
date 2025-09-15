# Cleaners Json Examples
Examples for creating Jsons with default cleaner. An Example of cleaner can be found in git: [full_rep_processors.json](../MedModel%20json%20format.md#full-example)
 
full_cleaners is based on:

- configured simple cleaner with strict boundaries for each signal 
- sim_val - when signal appears with the same time and different value which value to take? (from my observations in THIN - taking the first value is better)
- panels calculation and remove mismatches of biological rules. For example wrong calculation of BMI
Notes:
- There is a problem with Cholesterol_over_HDL signal in the loading process,  so using full_cleaner is not recommended for now with the rule of the Cholesterol_over_HDL activated (rules 15,17)
- You can now use Flow with "pids_sigs_print" mode or Yaron print program to print pids and signals after rep_processors. It may be useful for cleaners, virtual signals and more. I had created a different print (not in Flow) that shows the difference between 2 run modes of rep_processings (or compare run with rep processing to no rep processing at all) and prints the removed rows with "[REMOVED]" in each removed row to see what happened. for more information contact me.
 
```json
{
  "model_json_version": "2",
  "serialize_learning_set": "0",
  "model_actions": [
	{
      "action_type": "rp_set",
      "members": [
	    {
          "rp_type":"conf_cln",
		  "conf_file":"../settings/cleanDictionary.csv",
          "time_channel":"0",
		  "clean_method":"confirmed",
		  "signal":"file:../settings/all_rules_sigs.list"
		  //,"verbose_file":"/tmp/cleaning.log"
        },
		{
          "rp_type":"conf_cln",
		  "conf_file":"../settings/cleanDictionary.csv",
          "val_channel":["0", "1"],
		  "clean_method":"confirmed",
		  "signal": ["BP"]
		  //,"verbose_file":"/tmp/cleaning.log"
        }
      ]
    },
	{
      "action_type": "rp_set",
      "members": [
		{
          "rp_type":"sim_val",
		  "signal":"file:../settings/all_rules_sigs.list",
		  "type":"first",
          "debug":"0"
		  
        }
		
      ]
    },
    {
      "action_type": "rp_set",
      "members": [
		{
          "rp_type":"rule_cln",
		  "addRequiredSignals":"1",
          "time_window":"0",
		  "tolerance":"0.1",
		  "calc_res":"0.1",
		  "rules2Signals":"../settings/ruls2Signals.tsv",
		  "consideredRules":[ "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22" ] 
		  //,"verbose_file":"/tmp/panel_cleaning.log"
        }
      ]
    }
   
  ]
}
```
 
This was tested with Cleaner Program that checks for filtered stats with examples. here are the filtered stats on THIN:
Stats of simple cleaner
To create this table with full examples:
```bash
Flow --rep /home/Repositories/THIN/thin_jun2017/thin.repository --rep_processor_print --sigs /server/Work/Users/Alon/UnitTesting/examples/general_config_files/Cleaner/all_rules_sigs.list --max_examples 10 --seed 0 --f_output /tmp/test.log --cleaner_path /server/Work/Users/Alon/UnitTesting/examples/general_config_files/Cleaner/only_configure.json 
```
 
Simple Filtering - only Configure Rules for stricted bounderies
<table><tbody>
<tr>
<th>Signal</th>
<th>TOTAL_CNT</th>
<th>TOTAL_CNT_NON_ZERO</th>
<th>TOTAL_CLEANED</th>
<th>CLEAN_PERCENTAGE</th>
<th>CLEAN_NON_ZERO_PERCENTAGE</th>
<th>TOTAL_PIDS</th>
<th>PIDS_FILTERED</th>
<th>PIDS_FILTERED_NON_ZEROS</th>
<th>PIDS_FILTER_PERCENTAGE</th>
<th>PIDS_FILTER_NON_ZERO_PERCENTAGE</th>
<th>comment</th>
</tr>
<tr>
<td>eGFR_MDRD</td>
<td>30992945</td>
<td>30976157</td>
<td>30258567</td>
<td>2.37%</td>
<td>2.32%</td>
<td>5328855</td>
<td>427719</td>
<td>414278</td>
<td>8.03%</td>
<td>7.77%</td>
<td>Remove filter - not needed</td>
</tr>
<tr>
<td>UrineCreatinine</td>
<td>2603228</td>
<td>2602550</td>
<td>2556325</td>
<td>1.80%</td>
<td>1.78%</td>
<td>694781</td>
<td>17213</td>
<td>17210</td>
<td>2.48%</td>
<td>2.48%</td>
<td>Maybe problem in units that can be solved - checking</td>
</tr>
<tr>
<td>PlasmaViscosity</td>
<td>1258162</td>
<td>1257236</td>
<td>1237837</td>
<td>1.62%</td>
<td>1.54%</td>
<td>459295</td>
<td>8899</td>
<td>8147</td>
<td>1.94%</td>
<td>1.77%</td>
<td>Maybe problem in units that can be solved - checking</td>
</tr>
<tr>
<td>Transferrin</td>
<td>386039</td>
<td>386034</td>
<td>382521</td>
<td>0.91%</td>
<td>0.91%</td>
<td>232202</td>
<td>2709</td>
<td>2704</td>
<td>1.17%</td>
<td>1.16%</td>
<td>OK</td>
</tr>
<tr>
<td>HDL_over_nonHDL</td>
<td>14593886</td>
<td>14580124</td>
<td>14459042</td>
<td>0.92%</td>
<td>0.83%</td>
<td>3414705</td>
<td>77777</td>
<td>77335</td>
<td>2.28%</td>
<td>2.26%</td>
<td>OK</td>
</tr>
<tr>
<td>eGFR_CKD_EPI</td>
<td>30992945</td>
<td>30992374</td>
<td>30763090</td>
<td>0.74%</td>
<td>0.74%</td>
<td>5328855</td>
<td>171719</td>
<td>171715</td>
<td>3.22%</td>
<td>3.22%</td>
<td>Remove filter - not needed</td>
</tr>
<tr>
<td>Height</td>
<td>18860856</td>
<td>18780829</td>
<td>18714169</td>
<td>0.78%</td>
<td>0.35%</td>
<td>9334026</td>
<td>124126</td>
<td>57892</td>
<td>1.33%</td>
<td>0.62%</td>
<td>Maybe problem in units that can be solved - checking</td>
</tr>
<tr>
<td>CA125</td>
<td>252667</td>
<td>252550</td>
<td>251745</td>
<td>0.36%</td>
<td>0.32%</td>
<td>193979</td>
<td>599</td>
<td>598</td>
<td>0.31%</td>
<td>0.31%</td>
<td>OK</td>
</tr>
<tr>
<td>BP</td>
<td>90295429</td>
<td>89497237</td>
<td>89264282</td>
<td>1.14%</td>
<td>0.26%</td>
<td>9410580</td>
<td>525587</td>
<td>178924</td>
<td>5.59%</td>
<td>1.90%</td>
<td>bugfix to work on each channel</td>
</tr>
<tr>
<td>MCHC-M</td>
<td>25816227</td>
<td>25786164</td>
<td>25719334</td>
<td>0.38%</td>
<td>0.26%</td>
<td>5459883</td>
<td>56481</td>
<td>38450</td>
<td>1.03%</td>
<td>0.70%</td>
<td>OK</td>
</tr>
<tr>
<td>BMI</td>
<td>35211327</td>
<td>35194623</td>
<td>35118884</td>
<td>0.26%</td>
<td>0.22%</td>
<td>8293631</td>
<td>73201</td>
<td>59596</td>
<td>0.88%</td>
<td>0.72%</td>
<td>OK</td>
</tr>
<tr>
<td>Phosphore</td>
<td>4571174</td>
<td>4570766</td>
<td>4561223</td>
<td>0.22%</td>
<td>0.21%</td>
<td>1866755</td>
<td>3057</td>
<td>2683</td>
<td>0.16%</td>
<td>0.14%</td>
<td> </td>
</tr>
<tr>
<td>Lymphocytes%</td>
<td>24656284</td>
<td>24652334</td>
<td>24610137</td>
<td>0.19%</td>
<td>0.17%</td>
<td>5312408</td>
<td>26240</td>
<td>26119</td>
<td>0.49%</td>
<td>0.49%</td>
<td> </td>
</tr>
<tr>
<td>Neutrophils%</td>
<td>24740548</td>
<td>24736537</td>
<td>24695583</td>
<td>0.18%</td>
<td>0.17%</td>
<td>5321777</td>
<td>25181</td>
<td>25046</td>
<td>0.47%</td>
<td>0.47%</td>
<td> </td>
</tr>
<tr>
<td>INR</td>
<td>8505951</td>
<td>8496622</td>
<td>8488159</td>
<td>0.21%</td>
<td>0.10%</td>
<td>455102</td>
<td>5643</td>
<td>4012</td>
<td>1.24%</td>
<td>0.88%</td>
<td> </td>
</tr>
<tr>
<td>PDW</td>
<td>384442</td>
<td>383910</td>
<td>383555</td>
<td>0.23%</td>
<td>0.09%</td>
<td>109155</td>
<td>772</td>
<td>772</td>
<td>0.71%</td>
<td>0.71%</td>
<td> </td>
</tr>
<tr>
<td>PlasmaAnionGap</td>
<td>21530</td>
<td>21530</td>
<td>21513</td>
<td>0.08%</td>
<td>0.08%</td>
<td>5491</td>
<td>15</td>
<td>15</td>
<td>0.27%</td>
<td>0.27%</td>
<td> </td>
</tr>
<tr>
<td>WBC</td>
<td>26610249</td>
<td>26593657</td>
<td>26572901</td>
<td>0.14%</td>
<td>0.08%</td>
<td>5554159</td>
<td>25789</td>
<td>12033</td>
<td>0.46%</td>
<td>0.22%</td>
<td> </td>
</tr>
<tr>
<td>FreeT3</td>
<td>506119</td>
<td>505466</td>
<td>505091</td>
<td>0.20%</td>
<td>0.07%</td>
<td>205428</td>
<td>877</td>
<td>314</td>
<td>0.43%</td>
<td>0.15%</td>
<td> </td>
</tr>
<tr>
<td>RBC</td>
<td>25905761</td>
<td>25876600</td>
<td>25857697</td>
<td>0.19%</td>
<td>0.07%</td>
<td>5471987</td>
<td>28169</td>
<td>27732</td>
<td>0.51%</td>
<td>0.51%</td>
<td> </td>
</tr>
<tr>
<td>Ca</td>
<td>7173055</td>
<td>7172113</td>
<td>7167232</td>
<td>0.08%</td>
<td>0.07%</td>
<td>2582464</td>
<td>4826</td>
<td>3942</td>
<td>0.19%</td>
<td>0.15%</td>
<td> </td>
</tr>
<tr>
<td>Mg</td>
<td>182248</td>
<td>182218</td>
<td>182094</td>
<td>0.08%</td>
<td>0.07%</td>
<td>107908</td>
<td>134</td>
<td>108</td>
<td>0.12%</td>
<td>0.10%</td>
<td> </td>
</tr>
<tr>
<td>T4</td>
<td>475830</td>
<td>473666</td>
<td>473368</td>
<td>0.52%</td>
<td>0.06%</td>
<td>213799</td>
<td>2235</td>
<td>277</td>
<td>1.05%</td>
<td>0.13%</td>
<td> </td>
</tr>
<tr>
<td>Hematocrit</td>
<td>25862482</td>
<td>25836512</td>
<td>25822132</td>
<td>0.16%</td>
<td>0.06%</td>
<td>5463443</td>
<td>27793</td>
<td>10406</td>
<td>0.51%</td>
<td>0.19%</td>
<td> </td>
</tr>
<tr>
<td>TEMP</td>
<td>1801163</td>
<td>1786361</td>
<td>1785441</td>
<td>0.87%</td>
<td>0.05%</td>
<td>964098</td>
<td>12126</td>
<td>917</td>
<td>1.26%</td>
<td>0.10%</td>
<td> </td>
</tr>
<tr>
<td>Digoxin</td>
<td>93861</td>
<td>93617</td>
<td>93584</td>
<td>0.30%</td>
<td>0.04%</td>
<td>43469</td>
<td>215</td>
<td>212</td>
<td>0.49%</td>
<td>0.49%</td>
<td> </td>
</tr>
<tr>
<td>SerumAnionGap</td>
<td>59666</td>
<td>59661</td>
<td>59640</td>
<td>0.04%</td>
<td>0.04%</td>
<td>22779</td>
<td>24</td>
<td>24</td>
<td>0.11%</td>
<td>0.11%</td>
<td> </td>
</tr>
<tr>
<td>K+</td>
<td>28662323</td>
<td>28620055</td>
<td>28610424</td>
<td>0.18%</td>
<td>0.03%</td>
<td>5174781</td>
<td>35073</td>
<td>6931</td>
<td>0.68%</td>
<td>0.13%</td>
<td> </td>
</tr>
<tr>
<td>MPV</td>
<td>3443266</td>
<td>3442461</td>
<td>3441344</td>
<td>0.06%</td>
<td>0.03%</td>
<td>980181</td>
<td>1361</td>
<td>978</td>
<td>0.14%</td>
<td>0.10%</td>
<td> </td>
</tr>
<tr>
<td>Bicarbonate</td>
<td>3175248</td>
<td>3174729</td>
<td>3173852</td>
<td>0.04%</td>
<td>0.03%</td>
<td>741895</td>
<td>1332</td>
<td>844</td>
<td>0.18%</td>
<td>0.11%</td>
<td> </td>
</tr>
<tr>
<td>Cholesterol</td>
<td>18909856</td>
<td>18888280</td>
<td>18883203</td>
<td>0.14%</td>
<td>0.03%</td>
<td>3882355</td>
<td>22236</td>
<td>4367</td>
<td>0.57%</td>
<td>0.11%</td>
<td> </td>
</tr>
<tr>
<td>Albumin</td>
<td>23700344</td>
<td>23664696</td>
<td>23658553</td>
<td>0.18%</td>
<td>0.03%</td>
<td>4850137</td>
<td>25065</td>
<td>4754</td>
<td>0.52%</td>
<td>0.10%</td>
<td> </td>
</tr>
<tr>
<td>Na</td>
<td>29000033</td>
<td>28945701</td>
<td>28940315</td>
<td>0.21%</td>
<td>0.02%</td>
<td>5195665</td>
<td>26686</td>
<td>5191</td>
<td>0.51%</td>
<td>0.10%</td>
<td> </td>
</tr>
<tr>
<td>Iron_Fe</td>
<td>613710</td>
<td>613514</td>
<td>613409</td>
<td>0.05%</td>
<td>0.02%</td>
<td>363871</td>
<td>284</td>
<td>102</td>
<td>0.08%</td>
<td>0.03%</td>
<td> </td>
</tr>
<tr>
<td>Weight</td>
<td>39402271</td>
<td>39199410</td>
<td>39192705</td>
<td>0.53%</td>
<td>0.02%</td>
<td>9808932</td>
<td>167114</td>
<td>6298</td>
<td>1.70%</td>
<td>0.06%</td>
<td> </td>
</tr>
<tr>
<td>NonHDLCholesterol</td>
<td>14588087</td>
<td>14587707</td>
<td>14585866</td>
<td>0.02%</td>
<td>0.01%</td>
<td>3413836</td>
<td>1912</td>
<td>1909</td>
<td>0.06%</td>
<td>0.06%</td>
<td> </td>
</tr>
<tr>
<td>RandomGlucose</td>
<td>710956</td>
<td>701691</td>
<td>701603</td>
<td>1.32%</td>
<td>0.01%</td>
<td>423583</td>
<td>6726</td>
<td>87</td>
<td>1.59%</td>
<td>0.02%</td>
<td> </td>
</tr>
<tr>
<td>Platelets_Hematocrit</td>
<td>3400998</td>
<td>3399872</td>
<td>3399528</td>
<td>0.04%</td>
<td>0.01%</td>
<td>972680</td>
<td>1193</td>
<td>1191</td>
<td>0.12%</td>
<td>0.12%</td>
<td> </td>
</tr>
<tr>
<td>Hemoglobin</td>
<td>27748929</td>
<td>27701627</td>
<td>27698933</td>
<td>0.18%</td>
<td>0.01%</td>
<td>5689777</td>
<td>24331</td>
<td>2523</td>
<td>0.43%</td>
<td>0.04%</td>
<td> </td>
</tr>
<tr>
<td>LDL</td>
<td>12668050</td>
<td>12639848</td>
<td>12638813</td>
<td>0.23%</td>
<td>0.01%</td>
<td>3124704</td>
<td>20626</td>
<td>965</td>
<td>0.66%</td>
<td>0.03%</td>
<td> </td>
</tr>
<tr>
<td>MCV</td>
<td>26246642</td>
<td>26230251</td>
<td>26228319</td>
<td>0.07%</td>
<td>0.01%</td>
<td>5510085</td>
<td>12313</td>
<td>1833</td>
<td>0.22%</td>
<td>0.03%</td>
<td> </td>
</tr>
<tr>
<td>CO2</td>
<td>262289</td>
<td>261884</td>
<td>261866</td>
<td>0.16%</td>
<td>0.01%</td>
<td>44949</td>
<td>216</td>
<td>18</td>
<td>0.48%</td>
<td>0.04%</td>
<td> </td>
</tr>
<tr>
<td>Glucose</td>
<td>16484078</td>
<td>16472703</td>
<td>16471686</td>
<td>0.08%</td>
<td>0.01%</td>
<td>4466133</td>
<td>9937</td>
<td>928</td>
<td>0.22%</td>
<td>0.02%</td>
<td> </td>
</tr>
<tr>
<td>Amylase</td>
<td>355012</td>
<td>354296</td>
<td>354275</td>
<td>0.21%</td>
<td>0.01%</td>
<td>275843</td>
<td>685</td>
<td>20</td>
<td>0.25%</td>
<td>0.01%</td>
<td> </td>
</tr>
<tr>
<td>CorrectedCa</td>
<td>6448360</td>
<td>6447552</td>
<td>6447174</td>
<td>0.02%</td>
<td>0.01%</td>
<td>2381369</td>
<td>1087</td>
<td>357</td>
<td>0.05%</td>
<td>0.01%</td>
<td> </td>
</tr>
<tr>
<td>Triglycerides</td>
<td>14035783</td>
<td>14004268</td>
<td>14003515</td>
<td>0.23%</td>
<td>0.01%</td>
<td>3295899</td>
<td>19785</td>
<td>707</td>
<td>0.60%</td>
<td>0.02%</td>
<td> </td>
</tr>
<tr>
<td>LDH</td>
<td>223522</td>
<td>218968</td>
<td>218958</td>
<td>2.04%</td>
<td>0.00%</td>
<td>102148</td>
<td>3316</td>
<td>10</td>
<td>3.25%</td>
<td>0.01%</td>
<td> </td>
</tr>
<tr>
<td>ALKP</td>
<td>24501543</td>
<td>24491562</td>
<td>24490462</td>
<td>0.05%</td>
<td>0.00%</td>
<td>4975550</td>
<td>8773</td>
<td>844</td>
<td>0.18%</td>
<td>0.02%</td>
<td> </td>
</tr>
<tr>
<td>PULSE</td>
<td>5607620</td>
<td>5597890</td>
<td>5597659</td>
<td>0.18%</td>
<td>0.00%</td>
<td>2221767</td>
<td>7933</td>
<td>224</td>
<td>0.36%</td>
<td>0.01%</td>
<td> </td>
</tr>
<tr>
<td>Cl</td>
<td>6074637</td>
<td>6068936</td>
<td>6068789</td>
<td>0.10%</td>
<td>0.00%</td>
<td>1205272</td>
<td>4050</td>
<td>146</td>
<td>0.34%</td>
<td>0.01%</td>
<td> </td>
</tr>
<tr>
<td>Protein_Total</td>
<td>15053134</td>
<td>15051906</td>
<td>15051694</td>
<td>0.01%</td>
<td>0.00%</td>
<td>3350737</td>
<td>1336</td>
<td>188</td>
<td>0.04%</td>
<td>0.01%</td>
<td> </td>
</tr>
<tr>
<td>FreeT4</td>
<td>8375885</td>
<td>8347195</td>
<td>8347096</td>
<td>0.34%</td>
<td>0.00%</td>
<td>2572146</td>
<td>19968</td>
<td>99</td>
<td>0.78%</td>
<td>0.00%</td>
<td> </td>
</tr>
<tr>
<td>AST</td>
<td>5017954</td>
<td>5016921</td>
<td>5016887</td>
<td>0.02%</td>
<td>0.00%</td>
<td>1391446</td>
<td>972</td>
<td>33</td>
<td>0.07%</td>
<td>0.00%</td>
<td> </td>
</tr>
<tr>
<td>Platelets</td>
<td>26572350</td>
<td>26551880</td>
<td>26551731</td>
<td>0.08%</td>
<td>0.00%</td>
<td>5546115</td>
<td>15154</td>
<td>133</td>
<td>0.27%</td>
<td>0.00%</td>
<td> </td>
</tr>
<tr>
<td>ALT</td>
<td>20504083</td>
<td>20485612</td>
<td>20485528</td>
<td>0.09%</td>
<td>0.00%</td>
<td>4431602</td>
<td>12872</td>
<td>82</td>
<td>0.29%</td>
<td>0.00%</td>
<td> </td>
</tr>
<tr>
<td>MCH</td>
<td>25858658</td>
<td>25846546</td>
<td>25846464</td>
<td>0.05%</td>
<td>0.00%</td>
<td>5463374</td>
<td>7628</td>
<td>82</td>
<td>0.14%</td>
<td>0.00%</td>
<td> </td>
</tr>
<tr>
<td>B12</td>
<td>3015306</td>
<td>3013860</td>
<td>3013860</td>
<td>0.05%</td>
<td>0%</td>
<td>1607426</td>
<td>1212</td>
<td>0</td>
<td>0.08%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>RDW</td>
<td>4969565</td>
<td>4969446</td>
<td>4969563</td>
<td>4.02E-07</td>
<td>0.00%</td>
<td>1579652</td>
<td>2</td>
<td>2</td>
<td>0.00%</td>
<td>0.00%</td>
<td> </td>
</tr>
<tr>
<td>Urea</td>
<td>22375296</td>
<td>22373145</td>
<td>22373971</td>
<td>0.01%</td>
<td>0.00%</td>
<td>4367623</td>
<td>1291</td>
<td>1289</td>
<td>0.03%</td>
<td>0.03%</td>
<td> </td>
</tr>
<tr>
<td>Monocytes%</td>
<td>24411657</td>
<td>24387478</td>
<td>24388588</td>
<td>0.09%</td>
<td>0.00%</td>
<td>5276761</td>
<td>13670</td>
<td>13512</td>
<td>0.26%</td>
<td>0.26%</td>
<td> </td>
</tr>
<tr>
<td>VitaminD_25</td>
<td>352787</td>
<td>352738</td>
<td>352775</td>
<td>0.00%</td>
<td>-0.01%</td>
<td>228066</td>
<td>12</td>
<td>12</td>
<td>0.01%</td>
<td>0.01%</td>
<td> </td>
</tr>
<tr>
<td>Fibrinogen</td>
<td>196551</td>
<td>196504</td>
<td>196550</td>
<td>0.00%</td>
<td>-0.02%</td>
<td>143822</td>
<td>1</td>
<td>1</td>
<td>0.00%</td>
<td>0.00%</td>
<td> </td>
</tr>
<tr>
<td>HDL_over_LDL</td>
<td>12596626</td>
<td>12590998</td>
<td>12594958</td>
<td>0.01%</td>
<td>-0.03%</td>
<td>3118377</td>
<td>1509</td>
<td>1507</td>
<td>0.05%</td>
<td>0.05%</td>
<td> </td>
</tr>
<tr>
<td>Urine_Dipstick_pH</td>
<td>136097</td>
<td>136047</td>
<td>136091</td>
<td>0.00%</td>
<td>-0.03%</td>
<td>64581</td>
<td>6</td>
<td>6</td>
<td>0.01%</td>
<td>0.01%</td>
<td> </td>
</tr>
<tr>
<td>Transferrin_Saturation_Index</td>
<td>252126</td>
<td>251899</td>
<td>251984</td>
<td>0.06%</td>
<td>-0.03%</td>
<td>162901</td>
<td>134</td>
<td>134</td>
<td>0.08%</td>
<td>0.08%</td>
<td> </td>
</tr>
<tr>
<td>Ferritin</td>
<td>3729644</td>
<td>3728208</td>
<td>3729625</td>
<td>0.00%</td>
<td>-0.04%</td>
<td>1809350</td>
<td>18</td>
<td>18</td>
<td>0.00%</td>
<td>0.00%</td>
<td> </td>
</tr>
<tr>
<td>Bilirubin</td>
<td>23598709</td>
<td>23588476</td>
<td>23598656</td>
<td>0.00%</td>
<td>-0.04%</td>
<td>4904303</td>
<td>50</td>
<td>50</td>
<td>0.00%</td>
<td>0.00%</td>
<td> </td>
</tr>
<tr>
<td>Sex_Hormone_Binding_Globulin</td>
<td>133505</td>
<td>133441</td>
<td>133503</td>
<td>0.00%</td>
<td>-0.05%</td>
<td>110127</td>
<td>2</td>
<td>2</td>
<td>0.00%</td>
<td>0.00%</td>
<td> </td>
</tr>
<tr>
<td>Lymphocytes#</td>
<td>24916931</td>
<td>24903489</td>
<td>24916729</td>
<td>0.00%</td>
<td>-0.05%</td>
<td>5337938</td>
<td>159</td>
<td>159</td>
<td>0.00%</td>
<td>0.00%</td>
<td> </td>
</tr>
<tr>
<td>HbA1C</td>
<td>7597400</td>
<td>7592635</td>
<td>7597179</td>
<td>0.00%</td>
<td>-0.06%</td>
<td>1520278</td>
<td>163</td>
<td>160</td>
<td>0.01%</td>
<td>0.01%</td>
<td> </td>
</tr>
<tr>
<td>TIBC</td>
<td>151135</td>
<td>151012</td>
<td>151114</td>
<td>0.01%</td>
<td>-0.07%</td>
<td>97981</td>
<td>21</td>
<td>21</td>
<td>0.02%</td>
<td>0.02%</td>
<td> </td>
</tr>
<tr>
<td>Prolactin</td>
<td>407790</td>
<td>407328</td>
<td>407663</td>
<td>0.03%</td>
<td>-0.08%</td>
<td>297447</td>
<td>91</td>
<td>91</td>
<td>0.03%</td>
<td>0.03%</td>
<td> </td>
</tr>
<tr>
<td>Cholesterol_over_HDL</td>
<td>15035230</td>
<td>15018683</td>
<td>15031577</td>
<td>0.02%</td>
<td>-0.09%</td>
<td>3421173</td>
<td>3150</td>
<td>2923</td>
<td>0.09%</td>
<td>0.09%</td>
<td> </td>
</tr>
<tr>
<td>Follic_Acid</td>
<td>2703458</td>
<td>2701120</td>
<td>2703458</td>
<td>0%</td>
<td>-0.09%</td>
<td>1472362</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>HDL_over_Cholesterol</td>
<td>14670753</td>
<td>14656530</td>
<td>14669390</td>
<td>0.01%</td>
<td>-0.09%</td>
<td>3420769</td>
<td>1342</td>
<td>1331</td>
<td>0.04%</td>
<td>0.04%</td>
<td> </td>
</tr>
<tr>
<td>Neutrophils#</td>
<td>24970648</td>
<td>24946553</td>
<td>24970234</td>
<td>0.00%</td>
<td>-0.09%</td>
<td>5346509</td>
<td>383</td>
<td>378</td>
<td>0.01%</td>
<td>0.01%</td>
<td> </td>
</tr>
<tr>
<td>FSH</td>
<td>1045438</td>
<td>1044297</td>
<td>1045438</td>
<td>0%</td>
<td>-0.11%</td>
<td>688285</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Testosterone</td>
<td>388036</td>
<td>387595</td>
<td>388027</td>
<td>0.00%</td>
<td>-0.11%</td>
<td>292007</td>
<td>9</td>
<td>9</td>
<td>0.00%</td>
<td>0.00%</td>
<td> </td>
</tr>
<tr>
<td>LDL_over_HDL</td>
<td>12606025</td>
<td>12591423</td>
<td>12605655</td>
<td>0.00%</td>
<td>-0.11%</td>
<td>3118883</td>
<td>357</td>
<td>349</td>
<td>0.01%</td>
<td>0.01%</td>
<td> </td>
</tr>
<tr>
<td>Globulin</td>
<td>8009111</td>
<td>7999593</td>
<td>8008795</td>
<td>0.00%</td>
<td>-0.12%</td>
<td>1896822</td>
<td>254</td>
<td>253</td>
<td>0.01%</td>
<td>0.01%</td>
<td> </td>
</tr>
<tr>
<td>Creatinine</td>
<td>31070691</td>
<td>31033058</td>
<td>31069711</td>
<td>0.00%</td>
<td>-0.12%</td>
<td>5331326</td>
<td>753</td>
<td>732</td>
<td>0.01%</td>
<td>0.01%</td>
<td> </td>
</tr>
<tr>
<td>eGFR</td>
<td>16442849</td>
<td>16422354</td>
<td>16442849</td>
<td>0%</td>
<td>-0.12%</td>
<td>3426403</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Monocytes#</td>
<td>24612290</td>
<td>24579520</td>
<td>24612015</td>
<td>0.00%</td>
<td>-0.13%</td>
<td>5298350</td>
<td>234</td>
<td>219</td>
<td>0.00%</td>
<td>0.00%</td>
<td> </td>
</tr>
<tr>
<td>CK</td>
<td>942771</td>
<td>938846</td>
<td>940828</td>
<td>0.21%</td>
<td>-0.21%</td>
<td>481006</td>
<td>1367</td>
<td>1364</td>
<td>0.28%</td>
<td>0.28%</td>
<td> </td>
</tr>
<tr>
<td>Uric_Acid</td>
<td>1151516</td>
<td>1147621</td>
<td>1150405</td>
<td>0.10%</td>
<td>-0.24%</td>
<td>655507</td>
<td>1073</td>
<td>1068</td>
<td>0.16%</td>
<td>0.16%</td>
<td> </td>
</tr>
<tr>
<td>Erythrocyte</td>
<td>7239836</td>
<td>7222198</td>
<td>7239830</td>
<td>8.29E-07</td>
<td>-0.24%</td>
<td>2647537</td>
<td>6</td>
<td>5</td>
<td>0.00%</td>
<td>0.00%</td>
<td> </td>
</tr>
<tr>
<td>Lithium</td>
<td>274155</td>
<td>273378</td>
<td>274113</td>
<td>0.02%</td>
<td>-0.27%</td>
<td>21344</td>
<td>26</td>
<td>26</td>
<td>0.12%</td>
<td>0.12%</td>
<td> </td>
</tr>
<tr>
<td>GGT</td>
<td>9354116</td>
<td>9324434</td>
<td>9354066</td>
<td>0.00%</td>
<td>-0.32%</td>
<td>2369564</td>
<td>49</td>
<td>49</td>
<td>0.00%</td>
<td>0.00%</td>
<td> </td>
</tr>
<tr>
<td>UrineAlbumin</td>
<td>1366696</td>
<td>1361871</td>
<td>1366696</td>
<td>0%</td>
<td>-0.35%</td>
<td>391018</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>GFR</td>
<td>3225746</td>
<td>3213478</td>
<td>3225746</td>
<td>0%</td>
<td>-0.38%</td>
<td>882940</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>LUC</td>
<td>1330513</td>
<td>1324624</td>
<td>1330144</td>
<td>0.03%</td>
<td>-0.42%</td>
<td>324604</td>
<td>250</td>
<td>215</td>
<td>0.08%</td>
<td>0.07%</td>
<td> </td>
</tr>
<tr>
<td>HDL</td>
<td>14818204</td>
<td>14749529</td>
<td>14813285</td>
<td>0.03%</td>
<td>-0.43%</td>
<td>3431910</td>
<td>3956</td>
<td>2632</td>
<td>0.12%</td>
<td>0.08%</td>
<td> </td>
</tr>
<tr>
<td>UrineTotalProtein</td>
<td>386928</td>
<td>384724</td>
<td>386787</td>
<td>0.04%</td>
<td>-0.54%</td>
<td>179141</td>
<td>115</td>
<td>115</td>
<td>0.06%</td>
<td>0.06%</td>
<td> </td>
</tr>
<tr>
<td>Reticulocyte</td>
<td>69816</td>
<td>69418</td>
<td>69814</td>
<td>0.00%</td>
<td>-0.57%</td>
<td>49484</td>
<td>2</td>
<td>2</td>
<td>0.00%</td>
<td>0.00%</td>
<td> </td>
</tr>
<tr>
<td>UrineAlbumin_over_Creatinine</td>
<td>2451211</td>
<td>2431361</td>
<td>2451204</td>
<td>0.00%</td>
<td>-0.82%</td>
<td>678233</td>
<td>7</td>
<td>7</td>
<td>0.00%</td>
<td>0.00%</td>
<td> </td>
</tr>
<tr>
<td>PSA</td>
<td>1926651</td>
<td>1906549</td>
<td>1926420</td>
<td>0.01%</td>
<td>-1.04%</td>
<td>660296</td>
<td>159</td>
<td>157</td>
<td>0.02%</td>
<td>0.02%</td>
<td> </td>
</tr>
<tr>
<td>Serum_Oestradiol</td>
<td>394083</td>
<td>389241</td>
<td>394083</td>
<td>0%</td>
<td>-1.24%</td>
<td>274758</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>PFR</td>
<td>5264955</td>
<td>5164019</td>
<td>5264358</td>
<td>0.01%</td>
<td>-1.94%</td>
<td>1355995</td>
<td>569</td>
<td>535</td>
<td>0.04%</td>
<td>0.04%</td>
<td> </td>
</tr>
<tr>
<td>TSH</td>
<td>16173524</td>
<td>15848163</td>
<td>16172909</td>
<td>0.00%</td>
<td>-2.05%</td>
<td>4501457</td>
<td>528</td>
<td>450</td>
<td>0.01%</td>
<td>0.01%</td>
<td> </td>
</tr>
<tr>
<td>LuteinisingHormone</td>
<td>847445</td>
<td>830210</td>
<td>847445</td>
<td>0%</td>
<td>-2.08%</td>
<td>585366</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Rheumatoid_Factor</td>
<td>461205</td>
<td>450087</td>
<td>460648</td>
<td>0.12%</td>
<td>-2.35%</td>
<td>364740</td>
<td>494</td>
<td>492</td>
<td>0.14%</td>
<td>0.13%</td>
<td> </td>
</tr>
<tr>
<td>Progesterone</td>
<td>233686</td>
<td>227831</td>
<td>233686</td>
<td>0%</td>
<td>-2.57%</td>
<td>156019</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>CRP</td>
<td>5980408</td>
<td>5820488</td>
<td>5980374</td>
<td>0.00%</td>
<td>-2.75%</td>
<td>2320376</td>
<td>30</td>
<td>30</td>
<td>0.00%</td>
<td>0.00%</td>
<td> </td>
</tr>
<tr>
<td>Urine_Protein_Creatinine</td>
<td>324747</td>
<td>314833</td>
<td>324741</td>
<td>0.00%</td>
<td>-3.15%</td>
<td>151145</td>
<td>6</td>
<td>6</td>
<td>0.00%</td>
<td>0.00%</td>
<td> </td>
</tr>
<tr>
<td>Urine_Epithelial_Cell</td>
<td>299537</td>
<td>287827</td>
<td>299537</td>
<td>0%</td>
<td>-4.07%</td>
<td>145624</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Eosinophils%</td>
<td>24273861</td>
<td>22801564</td>
<td>24270972</td>
<td>0.01%</td>
<td>-6.44%</td>
<td>5260185</td>
<td>2185</td>
<td>1951</td>
<td>0.04%</td>
<td>0.04%</td>
<td> </td>
</tr>
<tr>
<td>Eosinophils#</td>
<td>24445262</td>
<td>22942339</td>
<td>24445176</td>
<td>0.00%</td>
<td>-6.55%</td>
<td>5281030</td>
<td>70</td>
<td>59</td>
<td>0.00%</td>
<td>0.00%</td>
<td> </td>
</tr>
<tr>
<td>Urine_Microalbumin</td>
<td>1386074</td>
<td>1269197</td>
<td>1386072</td>
<td>0.00%</td>
<td>-9.21%</td>
<td>375904</td>
<td>2</td>
<td>0</td>
<td>0.00%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Basophils#</td>
<td>23695244</td>
<td>14449541</td>
<td>23692629</td>
<td>0.01%</td>
<td>-63.97%</td>
<td>5194395</td>
<td>2007</td>
<td>1665</td>
<td>0.04%</td>
<td>0.03%</td>
<td> </td>
</tr>
<tr>
<td>Basophils%</td>
<td>23660542</td>
<td>9994176</td>
<td>23648885</td>
<td>0.05%</td>
<td>-136.63%</td>
<td>5193897</td>
<td>9473</td>
<td>3998</td>
<td>0.18%</td>
<td>0.08%</td>
<td> </td>
</tr>
<tr>
<td>NRBC</td>
<td>2113870</td>
<td>3939</td>
<td>2113869</td>
<td>4.73E-07</td>
<td>-53565.10%</td>
<td>733525</td>
<td>1</td>
<td>0</td>
<td>0.00%</td>
<td>0%</td>
<td> </td>
</tr>
</tbody></table>
 
Examples of filtered row log from program:
EXAMPLE pid     13055975        Signal  UrineCreatinine Time    20090210        Value   12225   [**REMOVED**]
EXAMPLE pid     13055975        Signal  UrineCreatinine Time    20100204        Value   14970   [**REMOVED**]
EXAMPLE pid     13055975        Signal  UrineCreatinine Time    20110304        Value   15219   [**REMOVED**]
EXAMPLE pid     13055975        Signal  UrineCreatinine Time    20120319        Value   15607   [**REMOVED**]
EXAMPLE pid     13055975        Signal  UrineCreatinine Time    20130221        Value   14.8
EXAMPLE pid     13055975        Signal  UrineCreatinine Time    20131115        Value   13
EXAMPLE pid     13055975        Signal  UrineCreatinine Time    20141124        Value   9
EXAMPLE pid     13055975        Signal  UrineCreatinine Time    20160122        Value   6.1
EXAMPLE pid     11134171        Signal  UrineCreatinine Time    20091215        Value   6694    [**REMOVED**]
EXAMPLE pid     11134171        Signal  UrineCreatinine Time    20111115        Value   6.4
EXAMPLE pid     6835336 Signal  UrineCreatinine Time    20080424        Value   3686    [**REMOVED**]
EXAMPLE pid     6835336 Signal  UrineCreatinine Time    20090918        Value   4630    [**REMOVED**]
EXAMPLE pid     6835336 Signal  UrineCreatinine Time    20100611        Value   13229   [**REMOVED**]
EXAMPLE pid     6835336 Signal  UrineCreatinine Time    20110106        Value   13349   [**REMOVED**]
EXAMPLE pid     6835336 Signal  UrineCreatinine Time    20110404        Value   3275    [**REMOVED**]
EXAMPLE pid     6835336 Signal  UrineCreatinine Time    20111202        Value   5063    [**REMOVED**]
EXAMPLE pid     6835336 Signal  UrineCreatinine Time    20120315        Value   3616    [**REMOVED**]
EXAMPLE pid     6835336 Signal  UrineCreatinine Time    20120628        Value   5262    [**REMOVED**]
EXAMPLE pid     6835336 Signal  UrineCreatinine Time    20130306        Value   2.9
EXAMPLE pid     6835336 Signal  UrineCreatinine Time    20140221        Value   4.3
EXAMPLE pid     6835336 Signal  UrineCreatinine Time    20150527        Value   4
EXAMPLE pid     6835336 Signal  UrineCreatinine Time    20160822        Value   3.6
EXAMPLE pid     8685466 Signal  UrineCreatinine Time    20091113        Value   11823   [**REMOVED**]
EXAMPLE pid     14408958        Signal  UrineCreatinine Time    20081124        Value   5452    [**REMOVED**]
EXAMPLE pid     14408958        Signal  UrineCreatinine Time    20100125        Value   6526    [**REMOVED**]
EXAMPLE pid     14408958        Signal  UrineCreatinine Time    20100624        Value   4616    [**REMOVED**]
EXAMPLE pid     14408958        Signal  UrineCreatinine Time    20110715        Value   3074    [**REMOVED**]
EXAMPLE pid     14408958        Signal  UrineCreatinine Time    20120615        Value   3674    [**REMOVED**]
EXAMPLE pid     14408958        Signal  UrineCreatinine Time    20130611        Value   4.2
EXAMPLE pid     14408958        Signal  UrineCreatinine Time    20140607        Value   3.1
EXAMPLE pid     14408958        Signal  UrineCreatinine Time    20140722        Value   3
STATS   UrineCreatinine TOTAL_CNT       2603228 TOTAL_CNT_NON_ZERO      2602550 TOTAL_CLEANED   2556325 CLEAN_PERCENTAGE        1.80172%        CLEAN_NON_ZERO_PERCENTAGE       1.77614%        TOTAL_PIDS    694781   PIDS_FILTERED   17213   PIDS_FILTERED_NON_ZEROS 17210   PIDS_FILTER_PERCENTAGE  2.47747%        PIDS_FILTER_PERCENTAGE  2.47704% 
1. Height- looks like there is factor 100 sometimes
EXAMPLE pid     17008937        Signal  Height  Time    20041111        Value   165
EXAMPLE pid     17008937        Signal  Height  Time    20050302        Value   16500   [**REMOVED**]
EXAMPLE pid     17008937        Signal  Height  Time    20060522        Value   16500   [**REMOVED**]
EXAMPLE pid     17008937        Signal  Height  Time    20060607        Value   165
EXAMPLE pid     17008937        Signal  Height  Time    20060607        Value   16500   [**REMOVED**]
EXAMPLE pid     17008937        Signal  Height  Time    20071109        Value   165
EXAMPLE pid     17008937        Signal  Height  Time    20090617        Value   165
EXAMPLE pid     5044235 Signal  Height  Time    19980408        Value   17      [**REMOVED**]
EXAMPLE pid     5044235 Signal  Height  Time    20040209        Value   173
EXAMPLE pid     5044235 Signal  Height  Time    20061212        Value   173
EXAMPLE pid     5044235 Signal  Height  Time    20091203        Value   173
EXAMPLE pid     5044235 Signal  Height  Time    20111122        Value   173
EXAMPLE pid     5044235 Signal  Height  Time    20121113        Value   173
EXAMPLE pid     11310017        Signal  Height  Time    19930902        Value   150
EXAMPLE pid     11310017        Signal  Height  Time    19990422        Value   12      [**REMOVED**]
EXAMPLE pid     5188073 Signal  Height  Time    20031118        Value   165
EXAMPLE pid     5188073 Signal  Height  Time    20031118        Value   16500   [**REMOVED**]
EXAMPLE pid     5188073 Signal  Height  Time    20040809        Value   158
EXAMPLE pid     5188073 Signal  Height  Time    20041120        Value   165
EXAMPLE pid     5188073 Signal  Height  Time    20060901        Value   158
EXAMPLE pid     5188073 Signal  Height  Time    20071010        Value   159
EXAMPLE pid     10759614        Signal  Height  Time    19930602        Value   168
EXAMPLE pid     10759614        Signal  Height  Time    19980225        Value   2       [**REMOVED**]
STATS   Height  TOTAL_CNT       18860856        TOTAL_CNT_NON_ZERO      18780829        TOTAL_CLEANED   18714169        CLEAN_PERCENTAGE        0.777732%       CLEAN_NON_ZERO_PERCENTAGE       0.354936%     TOTAL_PIDS       9334026 PIDS_FILTERED   124126  PIDS_FILTERED_NON_ZEROS 57892   PIDS_FILTER_PERCENTAGE  1.32982%        PIDS_FILTER_PERCENTAGE  0.620225%
1. MCHC-M – looks like factor 10 problem:
EXAMPLE pid     17224844        Signal  MCHC-M  Time    20010622        Value   357     [****]
EXAMPLE pid     17224844        Signal  MCHC-M  Time    20060711        Value   34.4
EXAMPLE pid     17224844        Signal  MCHC-M  Time    20090505        Value   32
EXAMPLE pid     16311924        Signal  MCHC-M  Time    19950502        Value   330     [****]
EXAMPLE pid     16311924        Signal  MCHC-M  Time    19950605        Value   326     [****]
EXAMPLE pid     16311924        Signal  MCHC-M  Time    20021114        Value   33.1
EXAMPLE pid     16311924        Signal  MCHC-M  Time    20050328        Value   32.9
EXAMPLE pid     16311924        Signal  MCHC-M  Time    20070111        Value   32.5
EXAMPLE pid     16311924        Signal  MCHC-M  Time    20070201        Value   33.4
EXAMPLE pid     16311924        Signal  MCHC-M  Time    20071030        Value   33.4
EXAMPLE pid     16311924        Signal  MCHC-M  Time    20071112        Value   33.1
EXAMPLE pid     16311924        Signal  MCHC-M  Time    20080422        Value   31.7
EXAMPLE pid     16311924        Signal  MCHC-M  Time    20081030        Value   34.8
EXAMPLE pid     16311924        Signal  MCHC-M  Time    20090611        Value   31.1
EXAMPLE pid     16311924        Signal  MCHC-M  Time    20090715        Value   33.5
EXAMPLE pid     16311924        Signal  MCHC-M  Time    20091230        Value   31.6
EXAMPLE pid     16311924        Signal  MCHC-M  Time    20100106        Value   30
EXAMPLE pid     16311924        Signal  MCHC-M  Time    20100126        Value   32.1
EXAMPLE pid     16311924        Signal  MCHC-M  Time    20100204        Value   31.6
EXAMPLE pid     16311924        Signal  MCHC-M  Time    20100225        Value   31.2
EXAMPLE pid     16311924        Signal  MCHC-M  Time    20100301        Value   31.7
EXAMPLE pid     16311924        Signal  MCHC-M  Time    20100308        Value   31.5
EXAMPLE pid     16311924        Signal  MCHC-M  Time    20100315        Value   29.5
EXAMPLE pid     15517308        Signal  MCHC-M  Time    20040511        Value   313     [****]
EXAMPLE pid     15517308        Signal  MCHC-M  Time    20071022        Value   32.7
EXAMPLE pid     17224984        Signal  MCHC-M  Time    19991116        Value   326     [****]
EXAMPLE pid     17224984        Signal  MCHC-M  Time    20050808        Value   34.1
EXAMPLE pid     17224984        Signal  MCHC-M  Time    20051026        Value   34.4
EXAMPLE pid     17224984        Signal  MCHC-M  Time    20051222        Value   34.8
EXAMPLE pid     17141004        Signal  MCHC-M  Time    20040728        Value   33.9
EXAMPLE pid     17141004        Signal  MCHC-M  Time    20090522        Value   396     [****]
EXAMPLE pid     17141004        Signal  MCHC-M  Time    20090623        Value   35
EXAMPLE pid     17141004        Signal  MCHC-M  Time    20090918        Value   35.3
EXAMPLE pid     17141004        Signal  MCHC-M  Time    20091123        Value   34.9
EXAMPLE pid     17141004        Signal  MCHC-M  Time    20100319        Value   370     [****]
STATS   MCHC-M  TOTAL_CNT       25816227        TOTAL_CNT_NON_ZERO      25786164        TOTAL_CLEANED   25719334        CLEAN_PERCENTAGE        0.375318%       CLEAN_NON_ZERO_PERCENTAGE       0.25917%      TOTAL_PIDS       5459883 PIDS_FILTERED   56481   PIDS_FILTERED_NON_ZEROS 38450   PIDS_FILTER_PERCENTAGE  1.03447%        PIDS_FILTER_PERCENTAGE  0.704228%
 
Stats of Full (with panels check)
```bash
Flow --rep /home/Repositories/THIN/thin_jun2017/thin.repository --rep_processor_print --sigs "Cholesterol_over_HDL,HDL_over_Cholesterol,UrineAlbumin,HDL,UrineAlbumin_over_Creatinine,UrineCreatinine,LDL,Cholesterol,LDL_over_HDL,HDL_over_LDL,Platelets_Hematocrit,MPV,NonHDLCholesterol,HDL_over_nonHDL,MCV,RBC,Hematocrit,Platelets,MCH,MCHC-M,Protein_Total,Hemoglobin,Height,Albumin,Basophils#,Eosinophils#,Monocytes#,Lymphocytes#,Neutrophils#,NRBC,WBC,BMI,Weight,UrineTotalProtein,ALKP,ALT,Amylase,AST,B12,Basophils%,Bicarbonate,Bilirubin,Ca,CA125,CK,Cl,CO2,CorrectedCa,Creatinine,CRP,Digoxin,eGFR,Eosinophils%,Erythrocyte,Ferritin,Fibrinogen,Follic_Acid,FreeT3,FreeT4,FSH,GFR,GGT,Globulin,Glucose,HbA1C,INR,Iron_Fe,K+,LDH,Lithium,LUC,LuteinisingHormone,Lymphocytes%,Mg,Monocytes%,Na,Neutrophils%,PDW,PFR,Phosphore,PlasmaAnionGap,PlasmaViscosity,Progesterone,Prolactin,PSA,PULSE,RandomGlucose,RDW,Reticulocyte,Rheumatoid_Factor,Serum_Oestradiol,SerumAnionGap,Sex_Hormone_Binding_Globulin,T4,Testosterone,TIBC,Transferrin,Transferrin_Saturation_Index,Triglycerides,TSH,Urea,Uric_Acid,Urine_Dipstick_pH,Urine_Epithelial_Cell,Urine_Microalbumin,Urine_Protein_Creatinine,VitaminD_25,TEMP" --max_examples 10 --seed 0 --f_output /tmp/test.log --cleaner_path_before /server/Work/Users/Alon/UnitTesting/examples/general_config_files/Cleaner/configure_sim_val.json --cleaner_path /server/Work/Users/Alon/UnitTesting/examples/general_config_files/Cleaner/full_cleaners.json 
```
<table><tbody>
<tr>
<th>Signal</th>
<th>TOTAL_CNT</th>
<th>TOTAL_CNT_NON_ZERO</th>
<th>TOTAL_CLEANED</th>
<th>CLEAN_PERCENTAGE</th>
<th>TOTAL_PIDS</th>
<th>PIDS_FILTERED</th>
<th>PIDS_FILTERED_NON_ZEROS</th>
<th>PIDS_FILTER_PERCENTAGE</th>
<th>PIDS_FILTER_NON_ZERO_PERCENTAGE</th>
<th>Comment</th>
</tr>
<tr>
<td>UrineAlbumin</td>
<td>1364175</td>
<td>1359350</td>
<td>1301695</td>
<td>4.58%</td>
<td>391018</td>
<td>33583</td>
<td>33206</td>
<td>8.59%</td>
<td>8.49%</td>
<td> Urine_panel, lot of real errors</td>
</tr>
<tr>
<td>UrineAlbumin_over_Creatinine</td>
<td>2444786</td>
<td>2424936</td>
<td>2382427</td>
<td>2.55%</td>
<td>678233</td>
<td>33467</td>
<td>30981</td>
<td>4.93%</td>
<td>4.57%</td>
<td> Urine_panel, lot of real errors</td>
</tr>
<tr>
<td>UrineCreatinine</td>
<td>2550757</td>
<td>2550079</td>
<td>2488398</td>
<td>2.44%</td>
<td>694781</td>
<td>33467</td>
<td>33438</td>
<td>4.82%</td>
<td>4.81%</td>
<td> Urine_panel, lot of real errors</td>
</tr>
<tr>
<td>Cholesterol_over_HDL</td>
<td>14653976</td>
<td>14653976</td>
<td>14375111</td>
<td>1.90%</td>
<td>3421173</td>
<td>115517</td>
<td>115517</td>
<td>3.38%</td>
<td>3.38%</td>
<td>there is problem in load of wrong source</td>
</tr>
<tr>
<td>HDL_over_LDL</td>
<td>12594284</td>
<td>12588656</td>
<td>12368827</td>
<td>1.79%</td>
<td>3118377</td>
<td>129667</td>
<td>128275</td>
<td>4.16%</td>
<td>4.11%</td>
<td> </td>
</tr>
<tr>
<td>Platelets_Hematocrit</td>
<td>3398224</td>
<td>3398224</td>
<td>3337846</td>
<td>1.78%</td>
<td>972680</td>
<td>19763</td>
<td>19763</td>
<td>2.03%</td>
<td>2.03%</td>
<td> </td>
</tr>
<tr>
<td>MPV</td>
<td>3438309</td>
<td>3438309</td>
<td>3377931</td>
<td>1.76%</td>
<td>980181</td>
<td>19763</td>
<td>19763</td>
<td>2.02%</td>
<td>2.02%</td>
<td> </td>
</tr>
<tr>
<td>HDL</td>
<td>14751464</td>
<td>14682789</td>
<td>14546126</td>
<td>1.39%</td>
<td>3431910</td>
<td>114884</td>
<td>98162</td>
<td>3.35%</td>
<td>2.86%</td>
<td> </td>
</tr>
<tr>
<td>HDL_over_Cholesterol</td>
<td>14665993</td>
<td>14651770</td>
<td>14467583</td>
<td>1.35%</td>
<td>3420769</td>
<td>86917</td>
<td>86067</td>
<td>2.54%</td>
<td>2.52%</td>
<td>there is problem in load of wrong source</td>
</tr>
<tr>
<td>Cholesterol</td>
<td>18855175</td>
<td>18855175</td>
<td>18649837</td>
<td>1.09%</td>
<td>3882355</td>
<td>114884</td>
<td>114884</td>
<td>2.96%</td>
<td>2.96%</td>
<td> </td>
</tr>
<tr>
<td>NonHDLCholesterol</td>
<td>14585464</td>
<td>14585084</td>
<td>14428102</td>
<td>1.08%</td>
<td>3413836</td>
<td>83548</td>
<td>83450</td>
<td>2.45%</td>
<td>2.44%</td>
<td> </td>
</tr>
<tr>
<td>LDL_over_HDL</td>
<td>12605642</td>
<td>12591040</td>
<td>12550215</td>
<td>0.44%</td>
<td>3118883</td>
<td>27352</td>
<td>26925</td>
<td>0.88%</td>
<td>0.86%</td>
<td> </td>
</tr>
<tr>
<td>LDL</td>
<td>12633401</td>
<td>12633401</td>
<td>12577976</td>
<td>0.44%</td>
<td>3124704</td>
<td>37293</td>
<td>37293</td>
<td>1.19%</td>
<td>1.19%</td>
<td> </td>
</tr>
<tr>
<td>MCV</td>
<td>26166367</td>
<td>26166367</td>
<td>26084584</td>
<td>0.31%</td>
<td>5510085</td>
<td>44007</td>
<td>44007</td>
<td>0.80%</td>
<td>0.80%</td>
<td> </td>
</tr>
<tr>
<td>HDL_over_nonHDL</td>
<td>14459035</td>
<td>14445273</td>
<td>14414026</td>
<td>0.31%</td>
<td>3414705</td>
<td>19387</td>
<td>18580</td>
<td>0.57%</td>
<td>0.54%</td>
<td> </td>
</tr>
<tr>
<td>RBC</td>
<td>25832962</td>
<td>25803801</td>
<td>25758846</td>
<td>0.29%</td>
<td>5471987</td>
<td>38602</td>
<td>34538</td>
<td>0.71%</td>
<td>0.63%</td>
<td> </td>
</tr>
<tr>
<td>Hematocrit</td>
<td>25784644</td>
<td>25784644</td>
<td>25725376</td>
<td>0.23%</td>
<td>5463443</td>
<td>29769</td>
<td>29769</td>
<td>0.54%</td>
<td>0.54%</td>
<td> </td>
</tr>
<tr>
<td>Platelets</td>
<td>26511344</td>
<td>26511344</td>
<td>26450966</td>
<td>0.23%</td>
<td>5546115</td>
<td>19763</td>
<td>19763</td>
<td>0.36%</td>
<td>0.36%</td>
<td> </td>
</tr>
<tr>
<td>MCH</td>
<td>25791202</td>
<td>25791202</td>
<td>25735104</td>
<td>0.22%</td>
<td>5463374</td>
<td>36564</td>
<td>36564</td>
<td>0.67%</td>
<td>0.67%</td>
<td> </td>
</tr>
<tr>
<td>MCHC-M</td>
<td>25697538</td>
<td>25697538</td>
<td>25655308</td>
<td>0.16%</td>
<td>5459883</td>
<td>25802</td>
<td>25802</td>
<td>0.47%</td>
<td>0.47%</td>
<td> </td>
</tr>
<tr>
<td>Protein_Total</td>
<td>15030698</td>
<td>15030698</td>
<td>15014686</td>
<td>0.11%</td>
<td>3350737</td>
<td>10857</td>
<td>10857</td>
<td>0.32%</td>
<td>0.32%</td>
<td> </td>
</tr>
<tr>
<td>Hemoglobin</td>
<td>27672196</td>
<td>27672196</td>
<td>27648170</td>
<td>0.09%</td>
<td>5689777</td>
<td>16426</td>
<td>16426</td>
<td>0.29%</td>
<td>0.29%</td>
<td> </td>
</tr>
<tr>
<td>Albumin</td>
<td>23630785</td>
<td>23630785</td>
<td>23614773</td>
<td>0.07%</td>
<td>4850137</td>
<td>10857</td>
<td>10857</td>
<td>0.22%</td>
<td>0.22%</td>
<td> </td>
</tr>
<tr>
<td>Basophils#</td>
<td>23647655</td>
<td>14401952</td>
<td>23636707</td>
<td>0.05%</td>
<td>5194395</td>
<td>9378</td>
<td>3885</td>
<td>0.18%</td>
<td>0.07%</td>
<td> </td>
</tr>
<tr>
<td>Eosinophils#</td>
<td>24411167</td>
<td>22908244</td>
<td>24400219</td>
<td>0.04%</td>
<td>5281030</td>
<td>9378</td>
<td>7428</td>
<td>0.18%</td>
<td>0.14%</td>
<td> </td>
</tr>
<tr>
<td>Monocytes#</td>
<td>24561221</td>
<td>24528451</td>
<td>24550273</td>
<td>0.04%</td>
<td>5298350</td>
<td>9378</td>
<td>9178</td>
<td>0.18%</td>
<td>0.17%</td>
<td> </td>
</tr>
<tr>
<td>Lymphocytes#</td>
<td>24824132</td>
<td>24810690</td>
<td>24813184</td>
<td>0.04%</td>
<td>5337938</td>
<td>9378</td>
<td>9326</td>
<td>0.18%</td>
<td>0.17%</td>
<td> </td>
</tr>
<tr>
<td>Neutrophils#</td>
<td>24907730</td>
<td>24883635</td>
<td>24896782</td>
<td>0.04%</td>
<td>5346509</td>
<td>9378</td>
<td>9272</td>
<td>0.18%</td>
<td>0.17%</td>
<td> </td>
</tr>
<tr>
<td>NRBC</td>
<td>2113731</td>
<td>3800</td>
<td>2112819</td>
<td>0.04%</td>
<td>733525</td>
<td>646</td>
<td>503</td>
<td>0.09%</td>
<td>0.07%</td>
<td> </td>
</tr>
<tr>
<td>WBC</td>
<td>26543214</td>
<td>26543214</td>
<td>26532266</td>
<td>0.04%</td>
<td>5554159</td>
<td>9378</td>
<td>9378</td>
<td>0.17%</td>
<td>0.17%</td>
<td> </td>
</tr>
<tr>
<td>BMI</td>
<td>35030317</td>
<td>35030317</td>
<td>35017055</td>
<td>0.04%</td>
<td>8293631</td>
<td>12869</td>
<td>12869</td>
<td>0.16%</td>
<td>0.16%</td>
<td> </td>
</tr>
<tr>
<td>UrineTotalProtein</td>
<td>385952</td>
<td>383748</td>
<td>385824</td>
<td>0.03%</td>
<td>179141</td>
<td>125</td>
<td>91</td>
<td>0.07%</td>
<td>0.05%</td>
<td> </td>
</tr>
<tr>
<td>Height</td>
<td>18664187</td>
<td>18664187</td>
<td>18664187</td>
<td>0%</td>
<td>9334026</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Weight</td>
<td>39068717</td>
<td>39068717</td>
<td>39068717</td>
<td>0%</td>
<td>9808932</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>ALKP</td>
<td>24458720</td>
<td>24458720</td>
<td>24458720</td>
<td>0%</td>
<td>4975550</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>ALT</td>
<td>20471720</td>
<td>20471720</td>
<td>20471720</td>
<td>0%</td>
<td>4431602</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Amylase</td>
<td>353637</td>
<td>353637</td>
<td>353637</td>
<td>0%</td>
<td>275843</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>AST</td>
<td>5013392</td>
<td>5013392</td>
<td>5013392</td>
<td>0%</td>
<td>1391446</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>B12</td>
<td>3011237</td>
<td>3011237</td>
<td>3011237</td>
<td>0%</td>
<td>1607426</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Basophils%</td>
<td>23647760</td>
<td>9981394</td>
<td>23647760</td>
<td>0%</td>
<td>5193897</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Bicarbonate</td>
<td>3171108</td>
<td>3171108</td>
<td>3171108</td>
<td>0%</td>
<td>741895</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Bilirubin</td>
<td>23542527</td>
<td>23532294</td>
<td>23542527</td>
<td>0%</td>
<td>4904303</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Ca</td>
<td>7095160</td>
<td>7095160</td>
<td>7095160</td>
<td>0%</td>
<td>2582464</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>CA125</td>
<td>252115</td>
<td>251998</td>
<td>252115</td>
<td>0%</td>
<td>193979</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>CK</td>
<td>939752</td>
<td>935827</td>
<td>939752</td>
<td>0%</td>
<td>481006</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Cl</td>
<td>6064395</td>
<td>6064395</td>
<td>6064395</td>
<td>0%</td>
<td>1205272</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>CO2</td>
<td>261631</td>
<td>261631</td>
<td>261631</td>
<td>0%</td>
<td>44949</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>CorrectedCa</td>
<td>6440715</td>
<td>6440715</td>
<td>6440715</td>
<td>0%</td>
<td>2381369</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Creatinine</td>
<td>31019168</td>
<td>30981535</td>
<td>31019168</td>
<td>0%</td>
<td>5331326</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>CRP</td>
<td>5976368</td>
<td>5816448</td>
<td>5976368</td>
<td>0%</td>
<td>2320376</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Digoxin</td>
<td>92754</td>
<td>92510</td>
<td>92754</td>
<td>0%</td>
<td>43469</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>eGFR</td>
<td>16433805</td>
<td>16413310</td>
<td>16433805</td>
<td>0%</td>
<td>3426403</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Eosinophils%</td>
<td>24269187</td>
<td>22796890</td>
<td>24269187</td>
<td>0%</td>
<td>5260185</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Erythrocyte</td>
<td>7233824</td>
<td>7216186</td>
<td>7233824</td>
<td>0%</td>
<td>2647537</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Ferritin</td>
<td>3722680</td>
<td>3721244</td>
<td>3722680</td>
<td>0%</td>
<td>1809350</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Fibrinogen</td>
<td>196069</td>
<td>196022</td>
<td>196069</td>
<td>0%</td>
<td>143822</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Follic_Acid</td>
<td>2700849</td>
<td>2698511</td>
<td>2700849</td>
<td>0%</td>
<td>1472362</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>FreeT3</td>
<td>504917</td>
<td>504917</td>
<td>504917</td>
<td>0%</td>
<td>205428</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>FreeT4</td>
<td>8340984</td>
<td>8340984</td>
<td>8340984</td>
<td>0%</td>
<td>2572146</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>FSH</td>
<td>1044260</td>
<td>1043119</td>
<td>1044260</td>
<td>0%</td>
<td>688285</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>GFR</td>
<td>3223523</td>
<td>3211255</td>
<td>3223523</td>
<td>0%</td>
<td>882940</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>GGT</td>
<td>9337150</td>
<td>9307468</td>
<td>9337150</td>
<td>0%</td>
<td>2369564</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Globulin</td>
<td>7992922</td>
<td>7983404</td>
<td>7992922</td>
<td>0%</td>
<td>1896822</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Glucose</td>
<td>16291642</td>
<td>16291642</td>
<td>16291642</td>
<td>0%</td>
<td>4466133</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>HbA1C</td>
<td>7510232</td>
<td>7505467</td>
<td>7510232</td>
<td>0%</td>
<td>1520278</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>INR</td>
<td>8402552</td>
<td>8402552</td>
<td>8402552</td>
<td>0%</td>
<td>455102</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Iron_Fe</td>
<td>610270</td>
<td>610270</td>
<td>610270</td>
<td>0%</td>
<td>363871</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>K+</td>
<td>28586751</td>
<td>28586751</td>
<td>28586751</td>
<td>0%</td>
<td>5174781</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>LDH</td>
<td>218679</td>
<td>218679</td>
<td>218679</td>
<td>0%</td>
<td>102148</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Lithium</td>
<td>273406</td>
<td>272629</td>
<td>273406</td>
<td>0%</td>
<td>21344</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>LUC</td>
<td>1328863</td>
<td>1322974</td>
<td>1328863</td>
<td>0%</td>
<td>324604</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>LuteinisingHormone</td>
<td>844893</td>
<td>827658</td>
<td>844893</td>
<td>0%</td>
<td>585366</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Lymphocytes%</td>
<td>24605312</td>
<td>24601362</td>
<td>24605312</td>
<td>0%</td>
<td>5312408</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Mg</td>
<td>181832</td>
<td>181832</td>
<td>181832</td>
<td>0%</td>
<td>107908</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Monocytes%</td>
<td>24385874</td>
<td>24361695</td>
<td>24385874</td>
<td>0%</td>
<td>5276761</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Na</td>
<td>28917933</td>
<td>28917933</td>
<td>28917933</td>
<td>0%</td>
<td>5195665</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Neutrophils%</td>
<td>24692458</td>
<td>24688447</td>
<td>24692458</td>
<td>0%</td>
<td>5321777</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>PDW</td>
<td>383011</td>
<td>382479</td>
<td>383011</td>
<td>0%</td>
<td>109155</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>PFR</td>
<td>5127271</td>
<td>5026335</td>
<td>5127271</td>
<td>0%</td>
<td>1355995</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Phosphore</td>
<td>4557642</td>
<td>4557642</td>
<td>4557642</td>
<td>0%</td>
<td>1866755</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>PlasmaAnionGap</td>
<td>21500</td>
<td>21500</td>
<td>21500</td>
<td>0%</td>
<td>5491</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>PlasmaViscosity</td>
<td>1237193</td>
<td>1237193</td>
<td>1237193</td>
<td>0%</td>
<td>459295</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Progesterone</td>
<td>233310</td>
<td>227455</td>
<td>233310</td>
<td>0%</td>
<td>156019</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Prolactin</td>
<td>406527</td>
<td>406065</td>
<td>406527</td>
<td>0%</td>
<td>297447</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>PSA</td>
<td>1924332</td>
<td>1904230</td>
<td>1924332</td>
<td>0%</td>
<td>660296</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>PULSE</td>
<td>5527058</td>
<td>5527058</td>
<td>5527058</td>
<td>0%</td>
<td>2221767</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>RandomGlucose</td>
<td>700394</td>
<td>700394</td>
<td>700394</td>
<td>0%</td>
<td>423583</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>RDW</td>
<td>4960073</td>
<td>4959954</td>
<td>4960073</td>
<td>0%</td>
<td>1579652</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Reticulocyte</td>
<td>69336</td>
<td>68938</td>
<td>69336</td>
<td>0%</td>
<td>49484</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Rheumatoid_Factor</td>
<td>460276</td>
<td>449158</td>
<td>460276</td>
<td>0%</td>
<td>364740</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Serum_Oestradiol</td>
<td>393299</td>
<td>388457</td>
<td>393299</td>
<td>0%</td>
<td>274758</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>SerumAnionGap</td>
<td>59530</td>
<td>59525</td>
<td>59530</td>
<td>0%</td>
<td>22779</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Sex_Hormone_Binding_Globulin</td>
<td>132646</td>
<td>132582</td>
<td>132646</td>
<td>0%</td>
<td>110127</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>T4</td>
<td>473023</td>
<td>473023</td>
<td>473023</td>
<td>0%</td>
<td>213799</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Testosterone</td>
<td>386501</td>
<td>386060</td>
<td>386501</td>
<td>0%</td>
<td>292007</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>TIBC</td>
<td>149863</td>
<td>149740</td>
<td>149863</td>
<td>0%</td>
<td>97981</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Transferrin</td>
<td>382006</td>
<td>382006</td>
<td>382006</td>
<td>0%</td>
<td>232202</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Transferrin_Saturation_Index</td>
<td>251706</td>
<td>251479</td>
<td>251706</td>
<td>0%</td>
<td>162901</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Triglycerides</td>
<td>13994934</td>
<td>13994934</td>
<td>13994934</td>
<td>0%</td>
<td>3295899</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>TSH</td>
<td>16164536</td>
<td>15839175</td>
<td>16164536</td>
<td>0%</td>
<td>4501457</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Urea</td>
<td>22350867</td>
<td>22348716</td>
<td>22350867</td>
<td>0%</td>
<td>4367623</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Uric_Acid</td>
<td>1149741</td>
<td>1145846</td>
<td>1149741</td>
<td>0%</td>
<td>655507</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Urine_Dipstick_pH</td>
<td>136044</td>
<td>135994</td>
<td>136044</td>
<td>0%</td>
<td>64581</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Urine_Epithelial_Cell</td>
<td>299102</td>
<td>287392</td>
<td>299102</td>
<td>0%</td>
<td>145624</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Urine_Microalbumin</td>
<td>1379741</td>
<td>1262864</td>
<td>1379741</td>
<td>0%</td>
<td>375904</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>Urine_Protein_Creatinine</td>
<td>321517</td>
<td>311603</td>
<td>321517</td>
<td>0%</td>
<td>151145</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>VitaminD_25</td>
<td>349534</td>
<td>349485</td>
<td>349534</td>
<td>0%</td>
<td>228066</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
<tr>
<td>TEMP</td>
<td>1779120</td>
<td>1779120</td>
<td>1779120</td>
<td>0%</td>
<td>964098</td>
<td>0</td>
<td>0</td>
<td>0%</td>
<td>0%</td>
<td> </td>
</tr>
</tbody></table>
 
 
****
 
