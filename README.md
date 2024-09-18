# Kaas - Excel Viewer and Adapter

This application is a PyQt6-based desktop GUI tool designed to work as an Excel viewer and adapter. The app enables users to view, manage, and process data from multiple Excel sheets, with specific functionalities like payment tracking, meetings, and dashboards. 

## Features

1. **Excel Viewer**: The app allows you to view and navigate different Excel sheets such as Tasks, Accounts, Transactions, etc.
2. **Checklist Dashboard**: Displays lists of payments like "Today's Payments," "Past Due Payments," and "Upcoming Week's Payments."
3. **Meeting Widget**: Users can select an audio file, provide context, and submit it for processing (simulated processing in the current version).
4. **Project Dashboard**: Displays project metrics such as current expenses, budget left, and project countdown using info boxes and progress bars.
5. **Configurable Sidebar**: The sidebar lets users navigate between different features like the Excel Viewer, Configuration, and Meeting.
6. **Dynamic Tabs**: Easily switch between different tabs that display Excel data, including categories like Salaries, Maintenance, Income, etc.
7. **Progress Dialogs**: Simulated loading dialogs appear when performing specific tasks like loading or processing data.
8. **Fullscreen & Shortcuts**: The app supports fullscreen mode and multiple keyboard shortcuts for easier navigation.
9. **Audio Processing**: Allows users to select and process audio files with user-provided context (currently simulated).

## Requirements

- **Python 3.x**
- **PyQt6**
- **Pandas** (for handling Excel data)
- **OpenPyXL** or **XlsxWriter** (for managing Excel files)

## Installation

1. **Clone this repository**:

   ```bash
   git clone https://github.com/username/kaas-excel-viewer.git
   ```

2. **Install dependencies**:

   Install the required dependencies using `pip`:

   ```bash
   pip install PyQt6 pandas openpyxl
   ```

3. **Running the application**:

   Navigate to the directory and run the `Kaas.py` script:

   ```bash
   python Kaas.py
   ```

## Usage

1. **Excel Viewer**:
   - The `Excel Viewer` tab allows you to view multiple Excel sheets. You can switch between tabs like "Tasks," "Accounts(Present)," "Transactions(Past)," etc.

2. **Main Dashboard**:
   - Displays project statistics such as total project expenses, budget left, and project countdown. Data is presented in the form of cards with a progress bar to represent the remaining budget.

3. **Checklist Dashboard**:
   - Displays different payment-related data categorized into sections like "Today's Payments," "Past Due Payments," and "Upcoming Payments." Payments can be selected and processed.

4. **Meeting Widget**:
   - Allows you to browse and select an audio file, enter a context for that file, and simulate processing it for transcription (future enhancements will involve actual audio processing).

5. **Configuration**:
   - A placeholder configuration page that can be extended for app customization.

6. **Shortcuts**:
   - Ctrl+E: Switch to Excel Viewer.
   - Ctrl+G: Switch to Configuration.
   - Alt+1 to Alt+6: Switch between different Excel tabs (Tasks, Accounts, Transactions, etc.).
   - Ctrl+Q: Exit the application.
   - F11: Toggle fullscreen mode.

## Folder Structure

```plaintext
|-- config_manager.py        # Manages application configuration settings.
|-- excel_manager.py         # Handles Excel file loading and data extraction.
|-- ui_components.py         # Custom UI components such as the Excel viewer tab.
|-- Kaas.py                  # Main application file that launches the GUI.
```

## Code Overview

1. **MainWindow**:
   - The main class that manages the entire application window and its components.
   - Initializes the UI with a sidebar, stacked widget for content, and a title bar with minimize, maximize, and close buttons.

2. **Tabs and Widgets**:
   - The app creates and manages different tabs, including the Main Dashboard, Checklist Dashboard, and category-specific Excel tabs.
   - The meeting widget allows users to select an audio file and submit it for simulated processing.

3. **Excel Manager**:
   - The `ExcelManager` class handles the loading of Excel data and provides the required data to populate the various UI components.

4. **Config Manager**:
   - The `ConfigManager` class is responsible for managing app settings and configurations, which are stored in a JSON file.

5. **Exception Handling**:
   - The application includes exception handling for uncaught errors and clean application shutdown.

## Simulated Features

- **Audio Processing**: The current version simulates the audio processing feature. Actual audio transcription is yet to be integrated.
- **Progress Dialogs**: Simulates loading dialogs for data-intensive operations like loading Excel sheets and processing payments.

## Future Enhancements

1. **Audio Processing Integration**: Add real audio processing functionality using a library like OpenAI Whisper or SpeechRecognition.
2. **Improved Error Handling**: Provide detailed error handling for user actions like invalid Excel files or incorrect configurations.
3. **Additional Configurations**: Add more settings and preferences under the Configuration tab for better app customization.
