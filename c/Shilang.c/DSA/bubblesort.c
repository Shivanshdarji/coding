#include<stdio.h>
void main()
{
    int num[20]={191,50,182,42,65,401,15,070,10,0},temp;
    for(int i=0;i<10;i++)
    {
        for(int j=0;j<9;j++)
        {
            temp=num[j];
            if(num[j]>num[j+1])
            {
                num[j]=num[j+1];
                num[j+1]=temp;
            }
        }
    }
  for(int i=0;i<10;i++)
  {
      printf("%d    ",num[i]);
  }
    
}




