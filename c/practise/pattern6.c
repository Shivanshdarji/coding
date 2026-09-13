#include<stdio.h>
void main()
{
    int n,m;
    char a,z;
    m=1;
    a='A';
    z='b';
    printf("Enter a number=");
    scanf("%d",&n);
    for(int i=1;i<=n;i++)
    {
        for(int j=1;j<=i;j++)
        {
            if(m%2!=0)
            {
                printf("%c",a);
                a=a+2;
                m++;
            }
            else if(m%2==0)
            {
                printf("%c",z);
                z=z+2;
                m++;
            }
        }
        printf("\n");
    }
}