#include<stdio.h>
void main ()
{
    int num,a,b=1,c=1;
    float ans[25];
    printf("Enter a Number=");
    scanf("%d",&num);
    for(int i=1;i<=num;i++)
    {
        printf("Enter Numberr=");
        scanf("%d",&a);
       do
       
        /* code */
      
       
        // while(a>=0)
       { if(a==1)
        printf("Shivansh Wins");
        
        else
        {
            c=c+b*10;
            a=a-c;
            b=b*10;
        }
       }
       while(a>=0);
       printf("%d",a);
       if(a==0)
      { printf("Shivansh Wins");
      }
       else if(a<0)
      { printf("Jaydev Wins");}
    }
}