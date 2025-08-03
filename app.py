from flask import Flask, render_template, request

app = Flask(__name__)

det1_global = None  # Store 1st determinant between requests (temporary)

def determinant_3x3(m):
    a, b, c, d, e, f, g, h, i = m
    return a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g)

def adjoint_manual(elements):
    a, b, c, d, e, f, g, h, i = elements
    A00 =  (e * i - f * h)
    A01 = -(d * i - f * g)
    A02 =  (d * h - e * g)
    A10 = -(b * i - c * h)
    A11 =  (a * i - c * g)
    A12 = -(a * h - b * g)
    A20 =  (b * f - c * e)
    A21 = -(a * f - c * d)
    A22 =  (a * e - b * d)
    cofactor = [
        [A00, A01, A02],
        [A10, A11, A12],
        [A20, A21, A22]
    ]
    adjoint = [[cofactor[j][i] for j in range(3)] for i in range(3)]
    return adjoint

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    adjoint = None
    error = None
    global det1_global

    if request.method == 'POST':
        try:
            elements = [int(request.form.get(f'val{i}')) for i in range(9)]
        except ValueError:
            error = "❌ Please enter valid numbers."
            return render_template("index.html", error=error)

        action = request.form['action']

        if action == 'determinant':
            det1_global = determinant_3x3(elements)
            result = f"Determinant: {det1_global}"

        elif action == 'adjoint':
            adjoint = adjoint_manual(elements)

        elif action == 'variable':
            if det1_global is None:
                error = "❌ Please calculate 1st determinant first."
            else:
                det2 = determinant_3x3(elements)
                if det2 == 0:
                    error = "❌ Cannot divide by zero (2nd determinant is 0)."
                else:
                    result = f"Variable (Det1 / Det2): {det1_global / det2:.3f}"

    return render_template("index.html", result=result, adjoint=adjoint, error=error)

if __name__ == '__main__':
    app.run(debug=True)
