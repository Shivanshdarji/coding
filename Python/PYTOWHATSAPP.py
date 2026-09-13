import pywhatkit    
phone_number = ["+919725265524","+917984207959","+919824065138"]  # Replace with the actual phone number and country code
message_content = "Hello Family"  # Message to be sent
waiting_time = 0  # Seconds to wait before sending
for i in phone_number:
    pywhatkit.sendwhatmsg_instantly(i, message_content, waiting_time)