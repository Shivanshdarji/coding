#include<stdio.h>
void main ()
{
    int a,n=1,sum=0,b=1;
    printf("Enter a Number=");
    scanf("%d",&a);
    while(b<=10)
    {
    
    printf("%d * %d = %d\n",a,n,a*n);
    b++;
    n++;
   
    }
    // while(n<=a)
    // {
    //     printf("%d\n",n);
    //     sum=sum+n;
    //     n++;
    // }
    
}