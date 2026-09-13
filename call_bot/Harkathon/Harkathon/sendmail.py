import sys
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# --- CONFIG ---
SENDGRID_API_KEY = "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"
FROM_EMAIL = "23ec6@svitvasad.ac.in"  # Replace with your verified sender email from SendGrid

def send_email(name, email, date, time):
    subject = "Your Booking Confirmation"
    html_content = f"""
    <h2>Hi {name},</h2>
    <p>Your booking is confirmed for <strong>{date}</strong> at <strong>{time}</strong>.</p>
    <p>We look forward to hosting you!</p>
    <br>
    <p>Cheers,<br>Team</p>
    """

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=email,
        subject=subject,
        html_content=html_content
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"[Email Sent] Status Code: {response.status_code}")
    except Exception as e:
        print(f"[Email Error] {e}")

# --- Entry Point ---
if __name__ == "__main__":
    try:
        data = json.loads(sys.argv[1])
        send_email(
            name=data.get("name", "Guest"),
            email=data["email"],
            date=data.get("date", "TBD"),
            time=data.get("time", "TBD")
        )
    except Exception as err:
        print(f"[Script Error] {err}")
