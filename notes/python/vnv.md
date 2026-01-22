# Setting up a virtual ENV for Python

## Why Create a VNV?

VNV's are isolated from the rest of your computer. This means versioning is specific to the vnv you are creating rather than the computer as a whole. Generally it's best practice to create a new VNV for any new project.

## How do we Create a VNV?

From the terminal, make sure you install the virtual environment tool which

### 1. Create a Virtual Environment

Navigate to your project directory and create a virtual environment:

```bash
# Create a virtual environment named 'env' (you can use any name)
python -m venv env

# On some systems, you might need to use python3
python3 -m venv env
```

### 2. Activate the Virtual Environment

**On macOS/Linux:**

```bash
source env/bin/activate
```

**On Windows:**

```bash
# Command Prompt
env\Scripts\activate

# PowerShell
env\Scripts\Activate.ps1
```

When activated, you should see `(env)` at the beginning of your command prompt, indicating the virtual environment is active.
