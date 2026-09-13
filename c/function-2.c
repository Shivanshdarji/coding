#include<stdio.h>
void main ()
{
    int fact=4,a;
    a(fact);

}
int a(int fact)
{
    if(fact==0)
    return 0;
    else
    {
    int a=1,b=2,c;
    c=a*b;
    a=c;
    b=b+1;
    return(c+(fact-1));
    }

}