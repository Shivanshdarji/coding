#include<stdio.h>
#include<math.h>
void main()
{
    float num[5],ar=0;
    for(int i=1;i<=5;i++)
    {
        printf("Enter Number %d=",i);
        scanf("%f",&num[i]);
    }
    printf("Arithamatic Mean:");
    for(int i=1;i<=5;i++)
    {
         ar=ar+num[i];
       printf("%f\n",ar);
        
    }
     ar=ar/5;
    printf("%f\n",ar);
    ar=ar*5;
    printf("Geomatric Mean\n");
    float power=1;
    float geo;
    float a=5;
    for(int i=1;i<=5;i++)
    {
     power=power*num[i];
    }
    geo=pow(power,(1/a));
    printf("%f\n",geo);
    printf("Harmonic mean\n");
    float har=0;
    for(int i=1;i<=5;i++)
    {
       har=har+(1/num[i]);
    }
    har=5/har;
    printf("%f",har);
  
}



