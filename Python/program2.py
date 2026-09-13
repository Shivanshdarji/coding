#Program 1
num =input("Enter a number:")
print("You entered:",num)
print("Data type of num:",type(num))

#Program 2
for i in range(2,10,5):
    print(i)

#while
count=0
while count<(5):
    print(count)
    count+=1

#program2
user_input=''
while user_input.lower() !='quit':
    user_input=input("Enter somthind and 'Quit to leave'")
    print("Input is:",user_input)

#function
def greet():
    print("Hello")
m=int(input())
if(m<5):
    greet()

#function2
def find_sq(num):
    num=num*num
    print(num)
x=int(input())
find_sq(x)

#lamda
func=lambda a :a+10
print(func(5))    