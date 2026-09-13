#include<stdio.h>
int num(int);
void main()
{
int a,x=1,numbr;
printf("Enter a Number=");
scanf("%d",&a);
printf("%d",num(a));
printf("%d",nn(a,x));
}
int num(int a)
{
    if(a==1)
    return 1;
    else
   { printf("%d",a);
     (num(a-1));}
     
     
}
int nn(int a,int x)
{
    if(x==a)
    {
        return x;
    }
    else
    {
        printf("%d",x);
        return (nn(a,x+1));
    }
}