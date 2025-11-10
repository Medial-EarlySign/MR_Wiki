# Repository Signals File Format

- Lines beginning with `#` are comments.
- Each line in the file defines either:
    - **A Generic Signal Type**  
    Use `GENERIC_SIGNAL_TYPE` prefix to declare a new signal type. The format is:  
    `GENERIC_SIGNAL_TYPE [type_alias] [GSV_string_spec]`  
    (Three tab-separated fields)
        - `GENERIC_SIGNAL_TYPE`: Marks the line as a signal type definition.
        - `type_alias`: A short name for the signal type.
        - `GSV_string_spec`: The full specification is a single, comma-separated string. All T() (Time) channels must be listed before all V() (Value) channels.  For example: `T(i),V(f)`.   
            - Time channels use `T(X)`, where `X` is a comma-separated list of basic types (see [Types](#timevalue-channel-types)).  
            - Example: `T(i)` means one integer time channel; `T(i,i)` means two integer time channels (can also be written as `T(i),T(i)`).  
            - Value channels follow after time channels with comma separator between.
        A signal can include no time channels or no value channels.
    - **A Signal Definition**  
    Use `SIGNAL` to define a signal. Each line should have at least four fields, defaults are used for missing fields.
        - `SIGNAL`: Marks the line as a signal definition.
        - `signal_name`: The name of the signal.
        - `signal_unique_code`: A unique numeric code for the signal within the repository.
        - `signal_type`: Specify the type directly as a `GSV_string_spec` (e.g., `T(i),V(f)` for one integer time channel and one float value channel), or refer to a previously defined type alias using `16:type_alias`. The 16 is required for the parser to use Custom types and not old and deprecated data type structured.
        - `comment`: Free text, ignored by the system. Can be empty. Usually we document the signal group liek demographic,labs,cbc. Sometimes multiple tags are provided.
        - `categorical_bitmask`: A bitmask written left to right with one digit for each value channel indicating which value channels are categorical. `1`=categorical, `0`=numeric. (e.g., `10` means the first of two value channels is categorical, the second is numeric). Default is `0` for all value channels.
        - `units` (optional): Units for the signal, separated by `|` for multiple channels.

## Time/Value Channel Types
Here is a complete list of supported types:

* `u` prefix to specify unsigned number and controls the `_is_signed`
* `c` - character, 8 bit integer that can hold 256 unique numbers
* `s` - short, 16 bit that can hold 65536 unique numbers 
* `i` - integer, 32 bits, can hold 4B unique numbers 
* `l` - long, 64 bits, can hold 1.8*10^19 unique numbers 
* `f` - float 32 bits
* `d` - double float 64 bits
* `D`- long double

For source code please refer to `MedSignals.h` `type_enc::encode`

## Example

```
# Tab-delimited format

# Legacy signals definition (Used only for ColonFlag AlgoMarker)
SIGNAL  GENDER      100     0       Male=1,Female=2    1  
SIGNAL  BP          920     8    systolic,diastoloc    00    mmHg|mmHg
SIGNAL  Hemoglobin  1000    1     cbc   0   mg/dL
SIGNAL  RC          2309    1       Med All ReadCodes ^[0-9A-HJ-NP-U] .no I,O,V,W,X,Y    1
SIGNAL  Drug        2400    8       Drugs: date, drug code, duration in days, use proper    10    days

# Newer signals definition:
GENERIC_SIGNAL_TYPE   VInt    V(i)
GENERIC_SIGNAL_TYPE   LabT1V1    T(i),V(f)
GENERIC_SIGNAL_TYPE   CategoricalT1V1    T(i),V(i)
GENERIC_SIGNAL_TYPE   LabT1V2    T(i),V(f,f)
GENERIC_SIGNAL_TYPE   Date2Val_i_f    T(i),V(i,f)

SIGNAL  GENDER      100     16:VInt       Male=1,Female=2    1  
SIGNAL  BP          920     16:LabT1V2    systolic,diastoloc    00    mmHg|mmHg
SIGNAL  Hemoglobin  1000    16:LabT1V1     cbc   0   mg/dL
SIGNAL  RC          2309    16:CategoricalT1V1       Med All ReadCodes ^[0-9A-HJ-NP-U] .no I,O,V,W,X,Y    1
SIGNAL  Drug        2400    16:Date2Val_i_f       Drugs: date, drug code, duration in days, use proper    10    days
```

A full list of [deprecated signal types](../Infrastructure%20C%20Library/00.InfraMed%20Library%20page/Generic%20(Universal)%20Signal%20Vectors.md) by numeric code