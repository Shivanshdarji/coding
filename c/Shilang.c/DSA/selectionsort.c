#include<stdio.h>
void main()
{
    int num[20]={10,9,8,7,6,5,4,3,2,1},temp,temp2;
    int min;
    for(int j=0;j<10;j++)
    {
    min=num[j];
    for(int i=j+1;i<10;i++)
    {
        if(num[i]<min)
        {
            min=num[i];
            temp2=i;
        }
    }
    temp=num[j];
    num[j]=min;
    num[temp2]=temp;
    }
    for(int i=0;i<10;i++)
    {
        printf("%d  ",num[i]);
    }
}




