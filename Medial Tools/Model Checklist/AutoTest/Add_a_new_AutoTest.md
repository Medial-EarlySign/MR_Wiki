# Add a new AutoTest

This page explains how to add a new test to the AutoValidation TestKit. It covers where to place the test, the required metadata, a minimal test template, and examples.

## 1) Decide whether the test is generic or specific

- Generic test: applies to many models and is reusable. Put generic test code under:

    MR_Tools/AutoValidation/kits/$KIT_TYPE/Tests

    Replace `$KIT_TYPE` with the appropriate test kit name (for example, `Development`, `ExternalValidation`, etc.).

- Specific test: applies only to a single model or is an override of a generic test. Place specific tests under the generated testkit path for that model, for example:

    /path/to/current/testkit_code/Tests

    (This path is created by `$AUTOTEST_LIB/generate_tests.sh`.)

## 2) Get a template

Copy a template from the `Templates` directory. There are templates for both shell (`.sh`) and Python (`.py`) tests. Use the template that matches the test runner you use.

## 3) Test contract (what your test should declare)

- REQ_PARAMETERS: a list of required environment/config variables (from `configs/env.sh`) that must be present when the test runs.
- DEPENDS: an optional list of other test names this test depends on; the framework will ensure they run first.
- Exit codes:
  - 0 - success
  - 1 - missing required parameter
  - 2 - the test detected a failure (assertion/internal check)
  - 3 - other error or crash

## 4) Minimal Python test example

Save this as a `.py` test file. It demonstrates the common structure and helper usage.

```python
#!/usr/bin/env python

# --- Edit these ---
REQ_PARAMETERS = ['REPOSITORY_PATH', 'WORK_DIR']  # required environment variables
DEPENDS = []  # names of tests this test depends on (optional)
# -------------------

import os
import sys

# argv[1] is the config directory, argv[2] is the base script directory
sys.path.insert(0, os.path.join(sys.argv[2], 'resources'))
from lib.PY_Helper import *

init_env(sys.argv, locals())
test_existence(locals(), REQ_PARAMETERS, TEST_NAME)

# Write your checks below. Use variables from REQ_PARAMETERS directly (they are injected into locals()).


# Example sanity check (replace with your logic)
import med
rep = med.PidRepository()
rep.read_all(REPOSITORY_PATH, [], ['BDATE'])
bdate_sig_df = rep.get_sig('BDATE')

if bdate_sig_df['val0'].max() > 19850101:
    # this indicates too-young patients in dataset (example rule)
    print('Failure: dataset contains patient with age under expected cutoff')
    raise Exception("Dataset contains patient with age range below 40 years old")
    sys.exit(2) # can also use return code 
```

## 5) Tips for editing the test

1. Add any required variables to `REQ_PARAMETERS`. If a required variable is missing at runtime, the test framework will fail with a helpful error.
2. If your test relies on other tests, list them in `DEPENDS` so they run first.
3. Keep tests small and focused: one logical assertion per test is ideal.

## 6) Where to place the file (recap)

- Generic tests: `MR_Tools/AutoValidation/kits/$KIT_TYPE/Tests`
- Specific tests: the testkit path generated for the model, e.g. `/path/to/current/testkit_code/Tests`

## 7) What to document in PRs

- Purpose of the test (what it asserts and why).
- Any new configuration keys added to `configs/env.sh`.
- If the test is generic, confirm it has broad applicability and doesn't hardcode model-specific paths.


