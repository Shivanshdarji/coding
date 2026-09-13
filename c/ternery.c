#include<stdio.h>
void main ()
{
    int a,i,b,c,d,e;
    for(d=1;d<=2;d++)
    {
        printf("Enter a Number=");
        scanf("%d",&a);
        if(d==1)
        b=a;
    }
   
    
    c=a>b?a:b;
    printf("%d",c);
}