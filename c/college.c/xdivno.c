#include<stdio.h>

void main ()
{
    float n,num=0;
     float fac=1,j,a=1,k,b=2,c;
     int i,mult=1;
    printf("Enter a Number=");
    scanf("%f",&n);
    for(i=0;i<=9;i++)
    {
        for(k=1;k<=i;k++)
        {
             mult=mult*n;
        }
     printf("mult=%d\n",mult);
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
    if(i%2==0)
    {
      num=num+(mult/fac);}
    else if(i==0)
    {
        num=1;
    } 
      else
    {num=num-(mult/fac);
    
    }printf("ans of %d is %f\n",i,num);
      

    }
    printf("Ans is %f",num);
}

