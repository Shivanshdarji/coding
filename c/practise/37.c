#include<stdio.h>
#include<stdlib.h>

void main(){
   
    int a;
   char *fp,*chara;
    printf("Enter a Number=");
    scanf("%d",&a);
     //char fp[a],chara[a];
   chara= (int*)calloc(a,sizeof(int));
   fp= (int*)calloc(a,sizeof(int));
    gets(fp);
    for(int i=1;i<=a;i++)
  { if(fp[i]>='a'&&fp[i]<='z'||fp[i]>='A'&&fp[i]<='Z')
   chara[a]=fp[i];}
   printf("%s",&chara);
}