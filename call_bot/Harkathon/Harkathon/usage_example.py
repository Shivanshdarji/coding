from hotel_booking_agent import HotelBookingAgent
import json

# Replace these with your actual API keys
OPENAI_API_KEY = "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"
SENDGRID_API_KEY = "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"  # You can use the one from demo.py

def main():
    # Initialize the agent
    agent = HotelBookingAgent(OPENAI_API_KEY, SENDGRID_API_KEY)
    
    # Example conversation - you can replace this with any hotel booking conversation
    conversation = """
    AI: Hello! Welcome to our hotel booking service. How can I help you today?
    
    Human: Hi, I'd like to book a room for my upcoming trip to New York.
    
    AI: Great! I'd be happy to help you with that. Could you please provide me with your travel dates?
    
    Human: I need a room from March 15th to March 17th, 2024.
    
    AI: Perfect! For 2 nights from March 15-17, 2024. How many guests will be staying?
    
    Human: Just 2 adults.
    
    AI: Excellent. I have availability at the Grand Plaza Hotel in Manhattan. We have a Deluxe Suite available for $299.99 per night. Would you like to proceed with this booking?
    
    Human: Yes, that sounds perfect!
    
    AI: Wonderful! Could you please provide your name and email address for the booking?
    
    Human: My name is John Smith and my email is naiteekchoksi@gmail.com
    
    AI: Thank you, John! I've successfully booked your Deluxe Suite at Grand Plaza Hotel for March 15-17, 2024 for 2 guests. Your total is $599.98 for 2 nights. Your booking confirmation number is HTL789123. You'll receive a confirmation email shortly.
    
    Human: Perfect! Thank you so much for your help.
    
    AI: You're very welcome! Have a wonderful stay at Grand Plaza Hotel!
    """
    
    print("🔄 Processing hotel booking conversation...")
    print("=" * 50)
    
    # Process the conversation (no hotel_email parameter needed - it's hardcoded)
    result = agent.process_booking_conversation(conversation)
    
    # Display results
    print("📊 Analysis Results:")
    print(json.dumps(result["analysis_result"], indent=2))
    print("\n" + "=" * 50)
    
    if result["email_sent"]:
        print("✅ Booking confirmation email sent successfully!")
        print(f"📧 Email status code: {result['email_result'].get('status_code', 'N/A')}")
    else:
        print("❌ No email sent (booking not successful or missing email)")
    
    print("\n🎉 Processing complete!")

if __name__ == "__main__":
    main() 