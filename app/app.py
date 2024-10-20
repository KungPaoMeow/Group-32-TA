from flask import Flask, render_template, request, redirect

app = Flask(__name__)

drugs = [
        {"name": "Drug1", "company": "C1", "type": "Prescription", "stock": 20},
        {"name": "Drug2", "company": "C2", "type": "Over the Counter", "stock": 30},
    ]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        return render_template('index.html', user_input=user_input)
    return render_template('testpage.html', user_input=None)

@app.route('/inv-monitoring')
def drug_table():
    # list of drugs to be displayed on inventory monitoring page
    # hard coded for now but will be changed later
    
    return render_template('inv-monitoring.html', drugs=drugs)

@app.route('/drug-edit/<int:id>', methods=['GET', 'POST'])
def drug_edit(id):
    # get the info of the selected drug
    drug = drugs[id]
    if request.method == 'POST':
        # update the drug info
        drug['name'] = request.form['name']
        drug['company'] = request.form['company']
        drug['type'] = request.form['type']
        drug['stock'] = request.form['stock']
        # send the user back to inventory monitoring page
        return redirect('/inv-monitoring')
    # display the drug info
    return render_template('drug-edit.html', drug=drug, ids=range(len(drugs)))
    
@app.route('/new-drug', methods=['GET', 'POST'])
def new_drug():
    # initialize the new drug to add
    drug = {"name": "", "company": "", "type": "", "stock": 0}
    if request.method == 'POST':
        # add the user-provided drug info to the list
        drug['name'] = request.form['name']
        drug['company'] = request.form['company']
        drug['type'] = request.form['type']
        drug['stock'] = request.form['stock']
        drugs.append(drug)
        # send the user back to inventory monitoring page
        return redirect('/inv-monitoring')
    # show form to add a drug
    return render_template('new-drug.html')

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(port=5001, debug=True)