#include<stdio.h>
int a(int);
void main ()
{
     int n,i,j,count,b,no,c;
     printf("Enter a Number");
     scanf("%d",&b);
     a(b);
}

int a(int b)
{
    int count=0,i,j,n;
    
    for(j=1;j<=b;j++)
    {
         if(b%j==0)
         count=count+1;
         
    }
     if(count==2)
    printf("No is prime");
    else
    printf("No is not a prime no");
    
    
}
