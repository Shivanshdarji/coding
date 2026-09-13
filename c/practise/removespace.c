#include<stdio.h>

void main()
{
    char num[]="S h i v a n s h";
    char ans[10];
    
    int x=0;
    printf("%s",num);
    for(int i=0;num!='\0';i++)
    {
        if(num[i]!=' ')
        {
            ans[x]=num[i];
            x++;
        }
    }
    ans[x] = '\0';
    
   printf("%s",ans);
}