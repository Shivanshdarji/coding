import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from typing import Optional, Dict, Any

class EmailAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.sg_client = SendGridAPIClient(api_key)
        
    def create_email(self, 
                    from_email: str,
                    to_emails: str,
                    subject: str,
                    html_content: str) -> Dict[str, Any]:
        """Create an email message object"""
        message = Mail(
            from_email=from_email,
            to_emails=to_emails,
            subject=subject,
            html_content=html_content
        )
        return message
        
    def send_email(self, message: Mail) -> Dict[str, Any]:
        """Send the email and return response details"""
        try:
            response = self.sg_client.send(message)
            return {
                'status_code': response.status_code,
                'body': response.body,
                'headers': response.headers
            }
        except Exception as e:
            return {
                'error_type': type(e).__name__,
                'error_details': str(e)
            }
            
    def update_email_content(self, 
                           message: Mail,
                           new_subject: Optional[str] = None,
                           new_html_content: Optional[str] = None) -> Mail:
        """Update email content"""
        if new_subject:
            message.subject = new_subject
        if new_html_content:
            message.html_content = new_html_content
        return message

# Example usage:
if __name__ == "__main__":
    # Initialize the agent with your API key
    agent = EmailAgent("YOUR_API_KEY")
    
    # Create an email
    email = agent.create_email(
        from_email="sender@example.com",
        to_emails="recipient@example.com",
        subject="Test Email",
        html_content="<strong>Hello World</strong>"
    )
    
    # Update email content
    updated_email = agent.update_email_content(
        email,
        new_subject="Updated Subject",
        new_html_content="<strong>Updated Content</strong>"
    )
    
    # Send the email
    result = agent.send_email(updated_email) 