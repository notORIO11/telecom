from flask import Flask, render_template, request, redirect, url_for, jsonify
import time
from chatbot import get_bot_reply

app = Flask(__name__)
app.secret_key = '1234'  # Needed if you later want sessions

def classify_support_ticket(text):
    text = text.lower()

    guide_keywords = [
        'باقة', 'الاشتراك', 'تجديد', 'طريقة', 'guide', 'how to', 'subscribe',
        'باقات', 'اشترك', 'code', 'كود', 'activation'
    ]
    
    chatbot_keywords = [
        'رصيد', 'الفلوس', 'billing', 'فواتير', 'شحن', 'سداد', 'balance', 'تم الخصم',
        'الخصم', 'charge', 'bill', 'الرسوم', 'pricing',
        'الباقة خلصت', 'ميجابايتس', 'النت خلص', 'الباقه خلصت',
        'بطئ', 'بطيء', 'بطيئ', 'slow', 'سرعة النت', 'النت بطئ',
        'مش عارف اختار', 'مش قادر اختار', 'i can’t choose', 'recommend bundle',
        'عاوز باقة', 'help me choose'
    ]

    human_keywords = [
        'شريحة', 'الشريحة', 'ضاعت', 'فقدت', 'مسروقة', 'مقفولة', 'activation failed',
        'sim lost', 'sim not working', 'الشبكة مش شغالة', 'انقطاع',
        'لا يوجد تغطية', 'no signal', 'network issue', 'قطع', 'disconnected',
        'رقمي', 'مفيش شبكة', 'مش شغال', 'مش شغالة'
    ]

    if any(keyword in text for keyword in guide_keywords):
        return 'guide'
    elif any(keyword in text for keyword in chatbot_keywords):
        return 'chatbot'
    elif any(keyword in text for keyword in human_keywords):
        return 'human'
    else:
        return 'human'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form.get('message', '')
        classification = classify_support_ticket(message)
        time.sleep(5)

        if classification == 'chatbot':
            return redirect(url_for('chatbot_page'))
        elif classification == 'guide':
            return redirect(url_for('guide'))
        else:
            return redirect(url_for('human'))

    return render_template('index.html')

@app.route('/guide')
def guide():
    return render_template('guide.html')

@app.route('/chatbot')
def chatbot_page():
    return render_template('chatbot.html')

@app.route('/chatbot_api', methods=['POST'])
def chatbot_api():
    user_input = request.json.get("message", "")
    reply = get_bot_reply(user_input)
    return jsonify({'reply': reply})

@app.route('/human')
def human():
    return render_template('human.html')

if __name__ == '__main__':
    app.run(debug=True)
