from flask import Flask, request, jsonify, render_template
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    height = float(data['height'])
    weight = float(data['weight'])
    age = int(data['age'])
    gender = data.get('gender', 'male')  # Default: male.
    activity_level = data.get('activityLevel', 'sedentary')  # Default: sedentary.
    diet_type = data.get('dietType', 'balanced')  # Default: balanced.
    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    daily_calories = bmr * activity_multipliers.get(activity_level, 1.2)
    diet_calories = {
        'vegetarian': 1800,
        'meat': 2500,
        'lacto_ovo_vegetarian': 2000,
        'balanced': 2200
    }
    daily_calorie_intake = diet_calories.get(diet_type, 2200)
    calorie_deficit = daily_calorie_intake - daily_calories
    weight_change_per_day = calorie_deficit / 7700  
    predicted_weight = weight + weight_change_per_day * 30 
    height_m = height / 100  
    bmi = weight / (height_m ** 2)
    if bmi < 18.5:
        suggestion = "You are underweight. Consider increasing your calorie intake and doing strength training."
    elif 18.5 <= bmi < 24.9:
        suggestion = "You have a normal weight. Keep up your current diet and exercise habits."
    elif 25 <= bmi < 29.9:
        suggestion = "You are overweight. Consider reducing your calorie intake and increasing aerobic exercise."
    else:
        suggestion = "You are obese. Consult a doctor and create a weight loss plan."
    return jsonify({'predictedWeight': predicted_weight, 'suggestion': suggestion})
if __name__ == '__main__':
    app.run(debug=True)