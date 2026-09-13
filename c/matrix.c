#include<stdio.h>
// int fac(int);
void main()
{
    
  int a[10][10],i,n,x,y,z,fact,det,b=1,j;
   printf("Enter a Number");
   scanf("%d",&n);
   for(i=1;i<=n;i++)
   {
    for(j=1;j<=n;j++)
    {
        printf("Enter a number %d=",b);
        scanf("%d",&a[i][j]);
         b++;
    }
   
   }
   for(i=1;i<=n;i++)
   {
    for(j=1;j<=n;j++)
    {
        printf("%d  ",a[i][j]);
        
    }
    printf("\n");
   }
   if(n==2)
   {
    det=(a[1][1]*a[2][2])-(a[1][2]*a[2][1]);
    printf("The Det is=%d",det);
   }
   if(n==3)
   {
    // det=a[1][1]*(a[2][2]*a[3][3])-(a[2][3]*a[3][2])-a[1][2]*((a[2][1]*a[3][3])-(a[2][3]*a[3][1]))+a[1][3]*((a[2][1]*a[3][2])-(a[2][2]*a[3][1]));
    // printf("%d",det);
    // det=a[1][1]*a[2][2]*a[3][3]-a[2][3]-a[3][2]-a[1][2]*a[2][1]*a[3][3]-a[2][3]*a[3][1]+a[1][3]*a[2][1]*a[3][2]-a[2][2]*a[3][1];
    int fac(n);
     printf("%d",det);
   }
   int fac(n);
  {
    // x=a[2][2]*a[3][3]-a[2][3]-a[3][2];
    // y=a[2][1]*a[3][3]-a[2][3]*a[3][1];
    // z=a[2][1]*a[3][2]-a[2][2]*a[3][1];
    det=a[1][1]*a[2][2]*a[3][3]-a[2][3]-a[3][2]-a[1][2]*a[2][1]*a[3][3]-a[2][3]*a[3][1]+a[1][3]*a[2][1]*a[3][2]-a[2][2]*a[3][1];
   
   }

}