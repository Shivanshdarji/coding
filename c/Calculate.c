#include <stdio.h>

void main()
{
    int a[10],i,n,min,max,add,sub,avg=0;
    printf("Enter a Number=");
    scanf("%d",&n);
    for(i=1;i<=n;i++)
    {
        printf("Enter a Number");
        scanf("%d",&a[i]);
    }
   
    min=a[0];
    for(i=1;i<=n;i++)
    {
        if(a[i]>max)
        max=a[i];
        if(a[i]<min)
        min=a[i];
        
    }
    max=a[i];
     for(i=1;i<=n;i++)
    {
        if(a[i]>max)
        max=a[i];
    }
    add=max+min;
    sub=max-min;
  
    avg=add/n;
    printf("sum=%d\n",avg);
    
    // a[1]=min;
    
    printf("max=%d and min=%d\nadd=%d and sub=%d\navg=%d",max,min,add,sub);
   
}
