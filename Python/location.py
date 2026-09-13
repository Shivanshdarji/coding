import phonenumbers
from phonenumbers import geocoder
phone_number1 = phonenumbers.parse("+91 9727371285")
#phone_number2 = phonenumbers.parse("+1(437)460-6126")

print("\nPhone Numbers Location\n")
print(geocoder.description_for_number(phone_number1,"en"))
#print(geocoder.description_for_number(phone_number2,"en"))