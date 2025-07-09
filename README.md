# wilkinsonLabTools
This web app will house different lab tools for analyzing and visualizing experimental data. 
It’s designed to be easily editable so new tools can be added over time, starting with Missteps by Genotype.

### [webapp link](https://wilkinsonlabtools.streamlit.app/)

## Missteps by Genotype 
A simple web tool for visualizing ladder test missteps across mouse genotypes, runs, and genders. 
Upload your CSV data and get clear, jittered scatter plots by run.

**Features**
</br>
- Landing page interface with *Missteps Scatterplots* button 
- Upload a CSV file with columns: Run, Genotype, Missteps Total, Gender, Walking
- Interactive selection of one or more runs via a dropdown
- Jittered scatter plots show repeated points without overlap
- Color-coded by Gender: 🔵 Male, 🔴 Female, ⚪ Unspecified
- Shapes represent walking scores: ◯ (0), ◼ (1), ◆ (2)
- Custom legend neatly placed in each plot

**Usage**

1. Via Web Browser 
   - Click the link above
   - Click button *Missteps Scatterplots*
   - Upload your LadderTestData.csv
   - All graphs will pop up
   - Option to select the runs you want to visualize
   - View and download the plots

2. Locally (if you want to edit)
    ```
    # Clone the repo
    git clone https://github.com/your-username/WL_Behavior_GUI.git
    cd WL_Behavior_GUI
    ```
    ```  
    # Create and activate a virtual environment
    python3 -m venv venv
    source venv/bin/activate   
    ```
    ```
    # Install dependencies
    pip install -r requirements.txt
   ```
   ```
   #Run App
   streamlit run app.py
   
