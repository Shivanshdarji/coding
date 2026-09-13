#include<stdio.h>
int fib(int);
void main ()
{
    int n,m=0,i;
   printf("Enter a Number=");
   scanf("%d",&n); 
   
   for(i=1;i<=n;i++)
   {
       printf("%d",fib(m));
       m++;
   }

   
}
int fib(int n)
{
    if(n==0||n==1)
    return n;
    else
    return (fib(n-1)+fib(n-2));

}