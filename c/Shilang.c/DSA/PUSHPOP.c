#include<stdio.h>
#define size 5
int main()
{
    int ans,top=-1;
    printf("1)PUSH\n2POP\n3)DISPLAY\n4)EXIT\n Enter your number=");
    while(1)
   {
    scanf("%d",&ans);
    switch(ans)
    {
        case 1:
        if(top==size)
        printf("stack overflow"); 
    }
   }
   return 0;
}