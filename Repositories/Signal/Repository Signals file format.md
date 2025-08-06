# Repository Signals File Format

- Lines starting with `#` are comments.
- Each line in the file can define either:
  - **A Generic Signal Type**  
    Use the keyword `GENERIC_SIGNAL_TYPE` to define a new signal type. The format is:  
    `GENERIC_SIGNAL_TYPE [type_alias] [GSV_string_spec]`  
    (Three tab-separated tokens)
    - `GENERIC_SIGNAL_TYPE`: Indicates a new signal type definition.
    - `type_alias`: An alias for the signal type.
    - `GSV_string_spec`: The type definition. Start with time channels (if any), followed by value channels.  
      - For time channels, use `T(X)`, where `X` is a comma-separated list of basic types (see [Generic (Universal) Signal Vectors](/Infrastructure%20Home%20Page/Generic%20(Universal)%20Signal%20Vectors)).  
      - Example: `T(i)` means one integer time channel; `T(i,i)` means two integer time channels (can also be written as `T(i),T(i)`).  
      - Then specify value channel types, if any.
  - **A Signal Definition**  
    Use the keyword `SIGNAL` to define a signal. The line should have at least six tokens (extra tokens are ignored). If fewer than six tokens are provided, defaults will be used for the missing fields.
    - `SIGNAL`: Indicates a new signal definition.
    - `signal_name`: The name of the signal.
    - `signal_unique_code`: A unique number for this signal within the repository (used internally).
    - `signal_type`: Specify the type directly as a `GSV_string_spec` (e.g., `T(i),V(f)` for one integer time channel and one float value channel), or refer to a previously defined type alias using `16:type_alias`.
    - `comment`: Free text, ignored by the system. Can be left empty, but ensure the next token is present.
    - `categorical_bitmask`: A bitmask indicating which value channels are categorical (e.g., `10` means the first of two value channels is categorical, the second is numeric). Default is `0` for all value channels.
    - `units` (optional): Document the signal units, separated by `|` for different channels.
