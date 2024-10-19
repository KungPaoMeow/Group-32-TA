from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        return render_template('index.html', user_input=user_input)
    return render_template('testpage.html', user_input=None)

@app.route('/inv-monitoring', methods=['GET', 'POST'])
def drug_table():
    # list of drugs to be displayed on inventory monitoring page
    # hard coded for now but will be changed later
    drugs = [
        {"name": "Drug1", "company": "C1", "type": "Prescription", "stock": 20},
        {"name": "Drug2", "company": "C2", "type": "Over the Counter", "stock": 30},
    ]
    return render_template('inv-monitoring.html', drugs=drugs)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(port=5001, debug=True)