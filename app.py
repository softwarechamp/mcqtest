from flask import Flask, render_template, request, redirect, url_for
import csv
import datetime

app = Flask(__name__)

# Read question bank from CSV
def read_questions():
    questions = []
    with open('question_bank.csv', mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            questions.append(row)
    return questions

# Save user responses to CSV
def save_response(response_data):
    with open('user_responses.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(response_data)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        responses = []

        # Loop through each question and capture the response
        for i in range(1, len(request.form) // 2 + 1):
            question_id = str(i)
            response = request.form.get(f'question_{question_id}')
            correct_answer = request.form.get(f'answer_{question_id}')
            question_text = request.form.get(f'question_text_{question_id}')

            # Prepare response data
            responses.append([
                question_id,
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                username,
                question_text,
                correct_answer,
                response
            ])
        
        # Save each response to the CSV
        for response in responses:
            save_response(response)

        return redirect(url_for('thank_you'))

    questions = read_questions()
    return render_template('index.html', questions=questions)

@app.route('/thank-you')
def thank_you():
    return "<h1>Thank you for your responses!</h1>"

if __name__ == '__main__':
    app.run(debug=True)
