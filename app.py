from flask import Flask, jsonify
from flask_cors import CORS
import data_pruning

# configuration
from werkzeug.exceptions import abort

DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# error handlers
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def internal_error(error):
    return "500 error"

# endpoint for assay by category
# [
#     {
#         id:_,
#         assay: [
#             {
#                 concentration:_,
#                 inhibition:_
#             }
#         ]
#     }
# ]
@app.route('/assay/<category>', methods=['GET'])
def assay(category):
    try:
        [df1, df2] = data_pruning.csv_to_dataframes(['ic50_and_label.csv', 'assay_filtered.csv'])
        ids = df1.loc[df1['Assay Result Label'] == category]
        df3 = data_pruning.left_join_df(ids, df2)
        assay_data = []
        obj = {}
        for index, row in df3.iterrows():
            previous_index = index - 1
            concentration = row['Concentration (M)']
            conc_inhibition = {'concentration': concentration, 'inhibition': row['% Inhibition']}
            if previous_index >= 0 and row['Compound ID'] == df3.loc[previous_index, 'Compound ID']:
                obj['assay'].append(conc_inhibition)
            else:
                obj['id'] = int(row['Compound ID'])
                obj['assay'] = [conc_inhibition]
            if df3.index.size == index + 1 or row['Compound ID'] != df3.loc[index + 1, 'Compound ID']:
                assay_data.append(obj)
                obj = {}
        if len(assay_data):
            return jsonify(assay_data), 200
        else:
            abort('No compounds with this category', 404)
    except:
        abort(500)

# endpoint for ic50 and label information
# {
#     label: [
#         {id: _, ic50: _}
#     ]
# }
@app.route('/ic50_label', methods=['GET'])
def ic50_label():
    try:
        [df1] = data_pruning.csv_to_dataframes(['ic50_and_label.csv'])
        ic50_and_result = {}
        for index, row in df1.iterrows():
            result_label = row['Assay Result Label']
            ic50 = row['IC50 (M)']
            compound_id = row['Compound ID']
            if result_label not in ic50_and_result:
                ic50_and_result[result_label] = []
            ic50_and_result[result_label].append({'id': compound_id, 'ic50': ic50})
        if ic50_and_result:
            return jsonify(ic50_and_result), 200
        else:
            abort('No IC50 results', 404)
    except:
        abort(500)

if __name__ == '__main__':
    app.run()
