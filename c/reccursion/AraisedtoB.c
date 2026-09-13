#include<stdio.h>
int atob(int a,int b,int c);
void main()
{

    int a,b,c=1,s;
   printf("Enter a=");
   scanf("%d",&a);
  printf("Enter b=");
  scanf("%d",&b);
   s=atob(a,b,c);
   printf("%d",s);
}
int atob(int a,int b,int c)
{
    int sum=1,i;
   if(c>b)
   return 1;
   else
   {
     (atob(a,b,(c+1)));
    for(i=1;i<=b;i++)
    sum=sum*a;
    return sum;
   }
}