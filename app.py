from turtle import title

from flask import Flask, jsonify, render_template, request, url_for

from app.service.model_ml import get_prediction, getDepLevel

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('index.html', title='Home')


@app.route("/tool")
def depression_check_tool():
    return render_template('tool.html', title='Depression Test')


@app.route("/result", methods=["POST"])
def show_depression_result():
    if not request.form:
        return jsonify({
            "message": "invalid post request"
        })

    body = request.form

    categorical_data = {
        'Age Group': {0: body['age-group']},
        'Gender': {0: body['gender']},
        'Qualification': {0: body['Qualification']},
        'Occupation': {0: body['Occupation']},
        'Annual Income': {0: body['Annual Income']},
        'Marital Status': {0: body['Marital Status']},
        'Residence': {0: body['Residence']}
    }

    if categorical_data['Qualification'][0] == 'Illiterate':
        categorical_data['Qualification'][0] = 'Doctorate'

    avg_sentiment = 0
    avg_sentiment += int(body['Monday'])
    avg_sentiment += int(body['Tuesday'])
    avg_sentiment += int(body['Wednesday'])
    avg_sentiment += int(body['Thursday'])
    avg_sentiment += int(body['Friday'])
    avg_sentiment += int(body['Satuarday'])

    binary_data = {
        'Q1': {0: body['q1']},
        'Q2': {0: body['q2']},
        'Q3': {0: body['q3']},
        'Q4': {0: body['q4']},
        'Q5': {0: body['q5']},
        'Q6': {0: body['q6']},
        'Q7': {0: body['q7']},
        'Q8': {0: body['q8']},
        'Q9': {0: body['q9']},
        'Q10': {0: body['q10']},
        'Q11': {0: body['q11']},
        'Q12': {0: body['q12']},
        'Q13': {0: body['q13']},
        'Q14': {0: body['q14']},
        'Q15': {0: body['q15']},
        'Q16': {0: body['q16']},
        'Q17': {0: body['q17']},
        'Q18': {0: body['q18']},
        'Q19': {0: body['q19']},
        'Q20': {0: body['q20']},
        'Q21': {0: body['q21']},
        'has_pet': {0: body['has_pet']},
        'has_park': {0: body['has_park']},
        'is_smu_high': {0: body['is_smu_high']},
        'has_flexible_work_hours': {0: body['has_flexible_work_hours']},
        'average_sentiment': {0: avg_sentiment}
    }
    result = int(get_prediction(categorical_data, binary_data))
    if (avg_sentiment >= 0):
        result = -1

    return render_template('result.html', result=result, name=request.form.get('name'))


@app.route("/traditional-tool")
def traditional_depression_check_tool():
    return render_template('traditional_model.html', title='Depression Test')


@app.route("/result-traditional", methods=["POST"])
def show_traditional_result():
    if not request.form:
        return jsonify({
            "message": "invalid post request"
        })
    body = request.form
    binary_data = [
        body['q1'],
        body['q2'],
        body['q3'],
        body['q4'],
        body['q5'],
        body['q6'],
        body['q7'],
        body['q8'],
        body['q9'],
        body['q10'],
        body['q11'],
        body['q12'],
        body['q13'],
        body['q14'],
        body['q15'],
        body['q16'],
        body['q17'],
        body['q18'],
        body['q20'],
        body['q19'],
        body['q21']
    ]
    score = 0
    for val in binary_data:
        score += int(val)
    result = getDepLevel(score)

    if (score <= 3):
        result = -1

    return render_template('result.html', result=result, name=request.form.get('name'))


if __name__ == "__main__":
    app.run()
