#include<stdio.h>
void main ()
{
    int n,st;
printf("Enter a Number=");
scanf("%d",&n);
st=stair(n);
printf("%d",st);
}
int stair(int n)
{
  if(n==1)return 1;
  else if (n==2)return 2;
  else
  return (stair(n-1)+stair(n-2));
}