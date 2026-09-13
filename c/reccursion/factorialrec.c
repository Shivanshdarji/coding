#include<stdio.h>

void main()
{
    int n;
 printf("Enter a Number=");
 scanf("%d",&n);
 int a=fact(n);
 printf("%d",a);
}
int fact(int n)
{
    if(n==1)
    return 1;
    else return(n*fact(n-1));
}