#include<stdio.h>
void main()
{
    int array[]={4,5,6,10};
    int min;
    min=array[0];
    for(int i=1;i<5;i++)
    

{
    if(min>array[i])
{
  min=array[i];
}
 if(i==5)
{
     if(min>array[i])
{
  min=array[i];
}
    printf("%d\n",min);
    min=0;
}
}


}