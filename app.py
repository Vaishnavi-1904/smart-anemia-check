from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    risk_score = None
    risk_level = None
    diet_plan = ""
    advice = ""

    if request.method == 'POST':
        age = int(request.form['age'])
        gender = request.form['gender']

        symptoms = [
            request.form.get('fatigue'),
            request.form.get('pale_skin'),
            request.form.get('shortness_of_breath'),
            request.form.get('dizziness'),
            request.form.get('cold_hands_feet'),
            request.form.get('brittle_nails'),
            request.form.get('chest_pain'),
            request.form.get('headache')
        ]

        additional_symptoms = 0

        if gender == 'female':
            if age >= 10:
                additional_symptoms += int(request.form.get('heavy_bleeding') == 'yes')
            if age >= 18:
                additional_symptoms += int(request.form.get('pregnancy') == 'yes')

        yes_count = sum([s == 'yes' for s in symptoms])
        total_symptoms = yes_count + additional_symptoms

        # Score = number of yes symptoms / 8 * 100
        risk_score = int((total_symptoms / 8) * 100)

        # Risk level
        if risk_score <= 39:
            risk_level = "Low"
            diet_plan = "🥦 Eat leafy greens, 🫘 lentils, 🍎 apples, 🍊 citrus fruits"
        elif 40 <= risk_score <= 60:
            risk_level = "Moderate"
            diet_plan = "🥩 Add meat/liver, 🍳 eggs, 🌰 dry fruits, 🧃 iron-rich juices"
            advice = "⚠️ Please consult a doctor for proper evaluation."
        else:
            risk_level = "High"
            diet_plan = "🥩 High-iron diet, 💊 consider supplements, 🧃 vitamin C-rich foods"
            advice = "❗ Immediate medical advice is recommended."

    return render_template('index.html',
                           risk_score=risk_score,
                           risk_level=risk_level,
                           diet_plan=diet_plan,
                           advice=advice)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))  # use 10000 for Render, 81 for Replit
    app.run(host='0.0.0.0', port=port)
