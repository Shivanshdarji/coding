import json
from openai import OpenAI

# Read conversation from file
with open("conversation.txt", "r", encoding="utf-8") as file:
    conversation = file.read()

print("📖 Conversation from file:")
print(conversation)
print("\n" + "="*50)

# Initialize OpenAI
client = OpenAI(api_key="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")

# System prompt
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

print("🤖 Calling OpenAI...")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Analyze this conversation:\n\n{conversation}"}
    ],
    temperature=0.1
)

raw_response = response.choices[0].message.content
print(f"🔍 Raw OpenAI Response:")
print(raw_response)
print("\n" + "="*50)

# Try to parse
try:
    result = json.loads(raw_response)
    print("✅ Successfully parsed JSON:")
    print(json.dumps(result, indent=2))
except Exception as e:
    print(f"❌ Failed to parse JSON: {e}") 