#include<stdio.h>
struct student
{
    char name[20];
    int age;
    float cpi;
    int rollno;
}student1;
void main ()
{
    int *ptr,cpi=5,*ptrr;
    // printf("Enter the cpi=");
    // scanf("%s",student1.cpi);
    ptr=&cpi;
    ptrr=&ptr;
     printf("%p\n",ptr);
    // printf("Enter the Name=");
    // scanf("%s",student1.name);
    // printf("%s",student1.name);
    printf("%p",*ptrr);
}