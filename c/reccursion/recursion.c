#include<stdio.h>
int a(int b);
void main()

{
    int b,sum;
   printf("Enter a Number=");
   scanf("%d",&b);
   sum=a(b);
   printf("%d",sum);

}
int a(int b)
{
    int sum=0;
    if(b==0)
    return 0;
    else
    return (b+a(b-1));
   
}