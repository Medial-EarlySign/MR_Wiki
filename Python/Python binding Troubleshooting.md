# Python Binding Troubleshooting

## Problem: `"import med"` does not work

### Possible Cause 1: Incorrect Python Version

- **Check:** If this happens in the command line, verify your Python interpreter path:
  ```bash
  which python
  ```
- **Solution:** Activate the correct Python environment:
  ```bash
  source /nas1/Work/python-env/python312/bin/activate
  ```
  Then try importing again.

---

### Possible Cause 2: Binding Not Compiled or Wrong Python Headers

- **Check:** The binding may not be compiled, or was compiled with incorrect Python headers.
- **Solution:** [Recompile the Python binding](Medial's%20C++%20API%20in%20Python/Build%20the%20python%20extention.md) using the correct environment