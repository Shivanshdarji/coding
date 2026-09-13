#include<stdio.h>
#define n 3
int front=-1;
int rear=-1;
int queue[n];
void enqueue (int x)
{
    if(front==(-1) &&rear==(-1))
   {
    front=rear=0;
    queue[front]=x;
    front++;
   }
   else if(rear==front)
   printf("Queue Full!\n");
   
   else
   {
    queue[front]=x;
    front=(front+1)%n;
   }
}
void display()
{
    for(int i=rear;i!=front;i=(i+1)%n)
    {
        printf("%d\n",queue[i]);
    }
}
void dequeue()
{
    if(front==-1&&rear==-1)
    {
        printf("\nqueue Underflow\n");
    }
    else if((rear+1)%n==front)
    {
        printf("Deleted element is %d\n",queue[rear]);
        front=rear=-1;
    }
    else
   { int temp;
    temp=queue[rear];
    rear=(rear+1)%n;
    printf("Deleted element is %d\n",temp);
   }
}
void main()
{
    int x,ans;
    printf("1)Enter \n2)Delete\n3)Display\n");
    while(1)
    {
    printf("Enter Number:");
    scanf("%d",&ans);
    switch (ans)
    {
    case 1:
        printf("Enter a Number to insert:");
        scanf("%d",&x);
        enqueue(x);
        break;
    case 2:
       dequeue();
       break;
    case 3:
       display();
       break;
    default:
    printf("Please select proper number.\n");
        break;
    }
    }
}