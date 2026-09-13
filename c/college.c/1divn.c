#include <stdio.h>

 void main()
{
    float i;
    float n,total=0;
    printf("Enter a number=");
    scanf("%f",&n);
    for(i=1;i<=n;i++)
    {
       total=total+1/i;
       
    }
    printf("%f",total);
    

}