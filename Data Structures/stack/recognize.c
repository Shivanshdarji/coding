#include<stdio.h>
#define n 10
char top=0;
char rec[n];
char stack[n];
void push(char x)
   {
     stack[top]=x;
     top++;
   }
void pop()
{
  
    
       // printf("Popped element is %c\n",stack[top]);
        top--;
 
}
void main()
{
    int a=0;
    char x=0;
    printf("Enter Your String=");
    scanf("%s",&rec);
    stack[top]='c';
    while(rec[a] != 'c')
    {
        push(rec[x]);
        x++;
        a++;
    }
    if(rec[a]=='c')
      {
        a++;
        x++;
      }
    while (rec[a]!='\0')
    {
        if (rec[x]==stack[top])
        {
           pop(); 
           x++;
        }
       else 
       printf("Invalid string!");
        
    }
    if(stack[top]=='c')
    {
        printf("valid string!");
    }
   else 
   printf("Not a valid string");
}