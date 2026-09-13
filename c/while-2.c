#include<stdio.h>
void main()
{
    int sum=0,num=1;
   // while(num<20)
   for(num=1;num<=20;num++) 
   {     if(num%2!=0)
        { sum=sum+num;
        // num+=2;
        printf("%d",num);
        printf("\n");
        }
        num+=2;
   }
    printf("%d",sum);
}