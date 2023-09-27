# Installation (Windows)
### 1. Prerequisites
- [Microsoft Visual C++ Redistributable](https://learn.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist?view=msvc-170)

### 2. Setup
1. Install the Microsoft Visual C++ Redistributable if not available already
2. Download the latest release on the project page (.exe file)

After this the Application can directly be run through the `tracker.exe` file.<br>
See [Running the Application](#running-the-application) for more information.

# Installation (Python)

### 1. Prerequisites
- [Python](https://www.python.org/downloads/) (Built with 3.11)

### 2. Setup
1. Install Python
2. Download the project
3. Install the required packages
   1. Run `pip install -r requirements.txt` in the project directory via the command line

After this the Application can directly be run through the `tracker.py` file.<br>
See [Running the Application](#running-the-application) for more information.

# Running the Application

Depending on how the Application was installed, it's either run through the `tracker.exe` or `tracker.py` file.<br>
Either option is executed through the command line. When running the Python version, the command might need to be prefixed with `python` or `py` depending on the system configuration.

## 1. Modules

### 1.1 Habit

The Habit module is used to create, edit and delete habits. It's accessed through the `habit` command.

#### 1.1.1 Subcommands

The following commands are available in the Habit module:
- `habit` - Lists all existing habits
- `habit create` - Create a new habit
- `habit modify` - Modify an existing habit
- `habit delete` - Delete an existing habit
- `habit complete` - Complete a habit

Examples:<br>
`tracker.exe habit create --name "Drink 2L of water" --period "Daily"`<br>
`tracker.exe habit complete --name "Drink 2L of water"`

### 1.2 Analytics

The Analytics module is used to view statistics about the habits. It's accessed through the `analytics` command.

#### 1.2.1 Subcommands

The following commands are available in the Analytics module:
- `analytics list` - Lists all habits and their statistics with various filter options
- `analytics streak` - Lists all habits and their streaks with various filter options

### 1.3 General

Every command mentioned above also has a `--help` option which displays a help message for the command.<br>

When used with the main command of either module, it displays a list of all available subcommands.<br>
When used with a specific command, it displays the required and optional arguments for the command.

