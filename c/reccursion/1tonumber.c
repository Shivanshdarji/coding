#include<stdio.h>
int num(int,int);
void main()
{
    int i,x=1,n;
    printf("Enter a Number=");
    scanf("%d",&n);
    num(x,n);
   
   
}
int num(int x,int n)
{
    if(x>n)
     return 0;
     else
    { printf("%d\n",x);
    return(num(x+1,n));
    }
   
}