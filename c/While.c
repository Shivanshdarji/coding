#include<stdio.h>
void main ()
{
    int a,n=1,sum=0,b=1;
    while(b<=10)
    {
    printf("Enter a Number %d=",b);
    scanf("%d",&a);
    sum=sum+a;
    b++;
   
    }
    // while(n<=a)
    // {
    //     printf("%d\n",n);
    //     sum=sum+n;
    //     n++;
    // }
    printf("%d\n",sum);
}