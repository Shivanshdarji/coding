#include<stdio.h>
void main()
{
    int max[3];
    for(int i=0;i<3;i++)
   {printf("Enter Number %d",i);
   scanf("%d",&max[i]);}
    int maximum=max[0];
    for(int i=0;i<3;i++)
    {
      if(max[i]>maximum)
      maximum=max[i];
      
      
    }
    printf("Max is %d",maximum);
}