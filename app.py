from flask import Flask, request, jsonify, render_template
from data_processing import load_data, plot_historical_data, predict_prices
from chatbot import get_response

app = Flask(__name__)
data = load_data('data/ethereum_price.csv')

# Generate initial plot for historical data
plot_historical_data(data)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response = get_response(user_message)
    return jsonify({'response': response})

@app.route('/help')
def help():
    return render_template('help.html')

if __name__ == '__main__':
    app.run(debug=True)
