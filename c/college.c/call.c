#include<stdio.h>
#include<conio.h>
void swap(int a, int b){
a = a+b;
b = a-b;
a = a-b;
printf("after the swap\n value of a: %d",a);
printf("\n value of b:%d",b);

}
void main(){
int a,b;
printf("enter the value of a and b:");
scanf("%d%d",&a,&b);
printf("before the swap\n value of a:%d ",a);
printf("\n value of b:%d",b,"\n");
swap(a,b);
getch();
}