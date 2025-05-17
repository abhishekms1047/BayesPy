from flask import Flask, request, jsonify, send_from_directory, render_template
import csv
import io
from ConjugatePriorTools import dirichletMultinomialEstimation as DME

app = Flask(__name__)


def compute_priors(rows):
    if not rows:
        return []
    K = len(rows[0])
    data = DME.CompressedRowData(K)
    priors = [0.0] * K
    for row in rows:
        row = [int(x) for x in row]
        weight = 1.0 / (1.0 + sum(row))
        for i in range(K):
            priors[i] += row[i] * weight
        data.appendRow(row, 1)
    prior_sum = sum(priors) + 0.01
    for i in range(K):
        priors[i] /= prior_sum
        priors[i] += 0.01
    priors = DME.findDirichletPriors(data, priors, 50)
    return priors


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/dirichlet', methods=['POST'])
def dirichlet():
    if 'file' not in request.files:
        return jsonify({'error': 'file field required'}), 400
    file = request.files['file']
    content = file.read().decode('utf-8')
    dialect = csv.Sniffer().sniff(content.splitlines()[0])
    reader = csv.reader(io.StringIO(content), dialect)
    rows = [row for row in reader if len(row) > 0]
    priors = compute_priors(rows)
    return jsonify({'priors': priors})


@app.route('/static/samples/<path:filename>')
def samples(filename):
    return send_from_directory('static/samples', filename)


if __name__ == '__main__':
    app.run(debug=True)
