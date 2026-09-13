#include<stdio.h>
void main()
{
    int num[10];
    printf("Enter Numbers:");
    for(int i=0;i<10;i++)
    {
        scanf("%d",&num[i]);
    }
    int a;
    while(1)
    {
    printf("Enter a number to search:");
    scanf("%d",&a);
    for(int i=0;i<10;i++)
    {
        if(num[i]==a)
        printf("Number Found at %d\n",i+1);
        // else if(i==10 && num[i]!=a)
        // printf("Number not Found");
    }
   
    }
}



