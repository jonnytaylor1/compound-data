# What the application does

1. Filters out unwanted data (invalid and inactive) from the CSV files and removes whitespace on some columns (python)
2. Has endpoints that can fetch the required data from the CSV (flask)
2. Displays the assay results by category (separate graphs) (Vue)
3. Displays the ic50 results by category (on same graph) (Vue)

# Server

## Project setup
```
pip3 install -r requirements.txt
```

### Generate CSV files
```
python3 data_pruning.py
```
2 CSV files should be generated and named assay_filtered.csv and ic50_and_label.csv

### Start Flask Server

```
python3 app.py
```

# Client

Navigate to the client directory
## Project setup

```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```
