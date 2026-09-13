import json
import os
from openai import OpenAI
from email_agent import EmailAgent

class HotelBookingAgent:
    def __init__(self, openai_api_key: str, sendgrid_api_key: str):
        self.openai_client = OpenAI(api_key=openai_api_key)
        self.email_agent = EmailAgent(sendgrid_api_key)
        
    def read_conversation_from_file(self, file_path: str = "conversation.txt"):
        """Read conversation from a text file"""
        try:
            if not os.path.exists(file_path):
                print(f"❌ Error: {file_path} not found!")
                return None
                
            with open(file_path, 'r', encoding='utf-8') as file:
                conversation = file.read().strip()
                
            if not conversation:
                print(f"❌ Error: {file_path} is empty!")
                return None
                
            print(f"📖 Successfully read conversation from {file_path}")
            return conversation
            
        except Exception as e:
            print(f"❌ Error reading {file_path}: {str(e)}")
            return None
        
    def analyze_conversation(self, conversation: str):
        """Analyze the conversation using OpenAI to extract booking information"""
        
        system_prompt = """You are an expert at analyzing hotel booking conversations. 
Extract booking information and return ONLY a valid JSON object with these fields:
- booking_successful (boolean)
- guest_name (string or null)
- guest_email (string or null) 
- hotel_name (string or null)
- checkin_date (string or null)
- checkout_date (string or null)
- number_of_guests (number or null)
- room_type (string or null)
- total_price (string or null)
- booking_reference (string or null)
- special_requests (string or null)

Return ONLY the JSON object, no additional text."""
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Analyze this conversation:\n\n{conversation}"}
                ],
                temperature=0.1
            )
            
            raw_content = response.choices[0].message.content
            
            if not raw_content or raw_content.strip() == "":
                return {
                    "error": "OpenAI returned empty response",
                    "booking_successful": False
                }
            
            # Clean up the response
            cleaned_content = raw_content.strip()
            if cleaned_content.startswith("```json"):
                cleaned_content = cleaned_content.replace("```json", "").replace("```", "").strip()
            
            booking_info = json.loads(cleaned_content)
            return booking_info
            
        except json.JSONDecodeError as e:
            return {
                "error": f"Invalid JSON from OpenAI: {str(e)}",
                "booking_successful": False
            }
        except Exception as e:
            return {
                "error": f"OpenAI API error: {str(e)}",
                "booking_successful": False
            }
    
    def generate_confirmation_email_content(self, booking_info):
        """Generate professional confirmation email HTML content"""
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #2c3e50; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .booking-details {{ background-color: #f8f9fa; padding: 15px; border-left: 4px solid #007bff; margin: 20px 0; }}
                .footer {{ background-color: #f8f9fa; padding: 15px; text-align: center; font-size: 12px; }}
                .highlight {{ color: #007bff; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🏨 Hotel Booking Confirmation</h1>
            </div>
            
            <div class="content">
                <h2>Dear {booking_info.get('guest_name', 'Valued Guest')},</h2>
                
                <p>Thank you for choosing our hotel booking service! We're delighted to confirm your reservation.</p>
                
                <div class="booking-details">
                    <h3>📋 Booking Details</h3>
                    <p><strong>Hotel:</strong> <span class="highlight">{booking_info.get('hotel_name', 'N/A')}</span></p>
                    <p><strong>Guest Name:</strong> {booking_info.get('guest_name', 'N/A')}</p>
                    <p><strong>Check-in Date:</strong> <span class="highlight">{booking_info.get('checkin_date', 'N/A')}</span></p>
                    <p><strong>Check-out Date:</strong> <span class="highlight">{booking_info.get('checkout_date', 'N/A')}</span></p>
                    <p><strong>Number of Guests:</strong> {booking_info.get('number_of_guests', 'N/A')}</p>
                    <p><strong>Room Type:</strong> {booking_info.get('room_type', 'N/A')}</p>
                    <p><strong>Total Price:</strong> <span class="highlight">{booking_info.get('total_price', 'N/A')}</span></p>
                    {f'<p><strong>Booking Reference:</strong> <span class="highlight">{booking_info.get("booking_reference")}</span></p>' if booking_info.get('booking_reference') else ''}
                    {f'<p><strong>Special Requests:</strong> {booking_info.get("special_requests")}</p>' if booking_info.get('special_requests') else ''}
                </div>
                
                <h3>📞 Important Information</h3>
                <ul>
                    <li>Please arrive at the hotel after 3:00 PM on your check-in date</li>
                    <li>Check-out time is 11:00 AM</li>
                    <li>Please bring a valid ID and credit card for check-in</li>
                    <li>If you need to modify or cancel your booking, please contact us at least 24 hours in advance</li>
                </ul>
                
                <p>We look forward to hosting you and ensuring you have a comfortable stay!</p>
                
                <p>Best regards,<br>
                <strong>Hotel Booking Team</strong></p>
            </div>
            
            <div class="footer">
                <p>This is an automated confirmation email. Please do not reply to this message.</p>
                <p>For assistance, contact our customer service team.</p>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def process_booking_from_file(self, file_path: str = "conversation.txt"):
        """Process booking conversation from a text file"""
        
        # Step 1: Read conversation from file
        conversation = self.read_conversation_from_file(file_path)
        if not conversation:
            return {
                "error": "Failed to read conversation from file",
                "analysis_result": {"booking_successful": False},
                "email_sent": False,
                "email_result": None
            }
        
        # Step 2: Process the conversation
        return self.process_booking_conversation(conversation)
    
    def process_booking_conversation(self, conversation: str):
        """Process the entire booking conversation workflow"""
        
        # Fixed FROM email as requested
        hotel_email = "23ec6@svitvasad.ac.in"
        
        print("🔄 Analyzing conversation...")
        
        # Step 1: Analyze the conversation
        booking_info = self.analyze_conversation(conversation)
        
        result = {
            "analysis_result": booking_info,
            "email_sent": False,
            "email_result": None
        }
        
        # Step 2: If booking is successful, send confirmation email
        if booking_info.get("booking_successful") and booking_info.get("guest_email"):
            print(f"✅ Booking successful! Sending email to: {booking_info.get('guest_email')}")
            
            # Generate email content
            email_content = self.generate_confirmation_email_content(booking_info)
            
            # Create email
            email = self.email_agent.create_email(
                from_email=hotel_email,
                to_emails=booking_info["guest_email"],
                subject=f"Hotel Booking Confirmation - {booking_info.get('hotel_name', 'Your Hotel')}",
                html_content=email_content
            )
            
            # Send email
            print("📧 Sending confirmation email...")
            email_result = self.email_agent.send_email(email)
            result["email_sent"] = True
            result["email_result"] = email_result
            
            if email_result.get('status_code') == 202:
                print("✅ Email sent successfully!")
            else:
                print("❌ Email sending failed!")
                
        else:
            print("❌ No successful booking found or missing email address")
            
        return result

# Main execution
if __name__ == "__main__":
    # API Keys
    OPENAI_API_KEY = "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"
    SENDGRID_API_KEY = "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"
    
    # Initialize the agent
    agent = HotelBookingAgent(OPENAI_API_KEY, SENDGRID_API_KEY)
    
    print("🏨 Hotel Booking Agent - Reading from conversation.txt")
    print("=" * 60)
    
    # Process the conversation from the text file
    result = agent.process_booking_from_file("conversation.txt")
    
    # Display results
    print("\n📊 Analysis Results:")
    print(json.dumps(result["analysis_result"], indent=2))
    print("\n" + "=" * 60)
    
    if result["email_sent"]:
        print("✅ Booking confirmation email sent successfully!")
        print(f"📧 Email status code: {result['email_result'].get('status_code', 'N/A')}")
    else:
        print("❌ No email sent")
        if result.get("error"):
            print(f"Error: {result['error']}")
    
    print("\n🎉 Processing complete!") 