#include<stdio.h>
void main()
{
    int num;
    printf("Enter a Number =");
    scanf("%d",&num);
    int a=1;
    int b=3;
    for(int i=1;i<=num;i++)
    {
        for(int j=1;j<=1;j++)
        {
            //   if(i==1)
            //  {
            //   printf("*");
              
            // }
            // else if(i%2==0&&j==2)
            // {
            //   printf(" *");
             
            // }
            // else if(i==3&&j==3)
            //  {
            //   printf("  *");
              
            // }
            
             if(a==1)
             {
              printf("*");
              a++;
            }
            else if(a==2)
            {
              printf(" *");
             a++;
            }
            else if(a==3)
             {
              printf("  *");
              a++;
              b--;
            }
           else if(b==2)
            {
              printf(" *");
             b--;
             a=b;
            }
           
        }
        printf("\n");
    }
}