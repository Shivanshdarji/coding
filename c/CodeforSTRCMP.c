#include<stdio.h>
#include<string.h>
void main()
{
    char a[5]="There";
    char s1[4]="Thas";
//    char a[10],b;
//     printf("Enter char=");
//     gets(a);
//     gets(b);
   // strstr(a,b);
   if(strncmp(a,s1,3)==0)
    printf("yess");
    else
    printf("No");
   
}