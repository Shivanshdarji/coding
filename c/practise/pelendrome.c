#include <stdio.h>
int main()
{int x,c;
scanf("%d",&x);
while (x>=0)
{
 c=c*10+x%10;
 x=x/10;
}
while (x<0)
{
 c=c*10+(x%10);
 x=x/10;
}
printf("%d",c);
}
