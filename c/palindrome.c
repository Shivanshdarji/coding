#include<stdio.h>
void main()
{
    int a,b,c,i,rem,rev=0;
     printf("Enter a number=");
    scanf("%d",&a);
    a=c;
    
    // for(i=a;i<0;i--)
     while(a>0)
    {
        rem=a%10;
         
        rev=(rev*10)+rem;
          
        
        
        a=a/10;
    }
    printf("%d\n",rev);
    
   
    if(rev==c)
    printf("It is Pelendrome");
    else
    printf("Not a Pelendrome");
   
}