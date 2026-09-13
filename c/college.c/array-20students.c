#include<stdio.h>
void main()
{
    int i,roll[10];
    int st[10];
   for(i=1;i<=10;i++)
   {
    printf("Enter Student marks %d",i);
    scanf("%d",&st[i]);
    printf("Enter Roll No %d",i);
    scanf("%d",&roll[i]);
   }
}