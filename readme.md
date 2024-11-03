## Setting Up the Virtual Environment

### macOS and Ubuntu

1. **Open Terminal**.
2. **Navigate to your project directory**:
   ```bash
   cd /path/to/your/project
   ```

3. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   ```

4. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate
   ```

5. **Install project dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Deactivate the virtual environment** (when you're done):
   ```bash
   deactivate
   ```

### Windows

1. **Open Command Prompt or PowerShell**.
2. **Navigate to your project directory**:
   ```cmd
   cd \path\to\your\project
   ```

3. **Create a virtual environment**:
   ```cmd
   python -m venv venv
   ```

4. **Activate the virtual environment**:
   - For Command Prompt:
     ```cmd
     venv\Scripts\activate
     ```
   - For PowerShell:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```

   > **Note**: If PowerShell blocks the script, you may need to adjust the execution policy. Run this in PowerShell:
   > ```powershell
   > Set-ExecutionPolicy RemoteSigned -Scope Process
   > ```

5. **Install project dependencies**:
   ```cmd
   pip install -r requirements.txt
   ```

6. **Deactivate the virtual environment** (when you're done):
   ```cmd
   deactivate
   ```
