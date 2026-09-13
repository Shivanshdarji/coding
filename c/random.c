#include<stdio.h>
void main()
{
    int a,b;
    a=rand(100);
    printf("Enter Your Number=");
    scanf("%d",b);
    printf("The no was %d",a);
    if(a==b)
    {printf("WOW!! YOU WON!!!");}
    else
    printf("YOU LOSE!!!");
}