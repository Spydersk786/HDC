# from twilio.rest import Client

# def send_alert(message_body):
#     print('alerted')


import requests

def send_alert(alert_message, url):
    data = {'message': alert_message}
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Alert sent successfully.")
        else:
            print(f"Failed to send alert. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending alert: {e}")
