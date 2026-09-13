#include <stdio.h>
#define n 5
int top=-1;
int stack[n],new;
void push(int element)
{
    printf("Print number to push:");
    scanf("%d",&element);
    if(top==-1)
    {
        
        stack[++top]=element;
        
    }
    else if(top==n)
    {
        printf("Stack Overflow!\n");
    }
    else
    {
        stack[++top]=element;
        
    }
}
void change()
{
    int temp;
    if(top==-1)
    printf("Stack is empty!\n");
    else
    {
        printf("Enter New Element=");
        scanf("%d",&new);
        temp=stack[top];
        stack[top]=new;
        printf("Element changed from %d to %d\n",temp,stack[top]);
    }
}
void pop()
{
    if(top==-1)
    {
        printf("stack underflow\n");
    }
    else
    {
        printf("Popped element is %d\n",stack[top]);
        top--;
    }
}
void peep()
{
    if(top==-1)
    printf("Stack is empty!\n");
    else
    {
      printf("The element at top is %d\n",stack[top]);
    }
}
void display()
{
    if(top==-1)
    printf("Nothing to display!");
    else
    {
    for(int i=0;i<=top;i++)
    {
        printf("Number %d in stack is %d\n",i+1,stack[i]);
    }
    }
}
int main()
{
    while(top!=100)
    {
        int ans,element;
          printf("Please select the number\n1)Push\n2)Pop\n3)peep\n4)display\n5)Change\n6)exit\n");
          scanf("%d",&ans);
          
        switch(ans)
        {
            case 1:
            push(element);
            break;

            case 2:
            pop();
            break;

            case 3:
            peep();
            break; 

            case 4:
            display();
            break;

            case 5:
            change();
            break;

            case 6:
            return 0;

            default:
            printf("Wrong number! please enter from 1-5.\n");
        }
    }
}