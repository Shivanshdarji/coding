#include<stdio.h>

void main ()
{
    float i,n,num=0;
     float fac=1,j,a=1,b=2,c;
    printf("Enter a Number=");
    scanf("%f",&n);
    for(i=1;i<=n;i++)
    {
        for(j=1;j<=i;j++)
    {
        if(j==1)
        fac=1;
        else
        {// {c=a*b;
        // a=b;
        // b=b+1;}
        fac=fac*j;}
       
    }
    
      num=num+(1/fac);
    }
    printf("Ans is %f",num);
}

