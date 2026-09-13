#include<stdio.h>
void main()
{
    int num[20]={1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20},f,r,i,m,n;
    printf("Enter a Number:");
    scanf("%d",&n);
    f=0;r=19;
    while(f<=r)
    {
        m=(r+f)/2;
        if(num[m]==n)
        {
            printf("Number found at %d",m+1);
            break;
        }
        else if(n<num[m])
        {
            r=num[m]-1;
        }
        else if(n>num[m])
        {
            f=num[m]+1;
        }
    }
    if(f==r==0)
    printf("Number not found");
}




