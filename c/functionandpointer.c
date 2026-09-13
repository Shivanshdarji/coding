#include <stdio.h>
int* add(int *x,int *y)
{
    int sum;
    sum=*x+*y;
    return sum;

}
void main()
{
    int *x,*y,*sum;
    printf("Enter two numbers 1");
    scanf("%d",&*x);
    printf("Enter two numbers 2");
    scanf("%d",&*y);
    sum=add(*x,*y);
     printf("sum is %d",*sum);
}