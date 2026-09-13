#include<stdio.h>
void main()
{
    int i,j,k,st[5],sub[3];
    for(i=1;i<=5;i++)
    {
        int total=0; 
        
        printf("Student %d\n",i);
        for(j=1;j<=3;j++)
        {
            printf("Enter marks %d\n",j);
            scanf("%d",&sub[j]);
            total=total+sub[j];

        }
        printf("Total of Student %d=%d\n",i,total);

        total=total/3;
        printf("Avg is %d\n",total);
        total=0;

    }
     for(i=1;i<=5;i++)
     {
        printf("Student %d\n",i);
        for(j=1;j<=3;j++)
        {
            printf("Marks %d=%d\n",j,sub[j]);
        }
     }


 }
// #include <stdio.h>
// int main()
// {
//     int student[5];
//     int sub[3],total=0,total1;
//     for (int i = 1; i <= 5; i++)
//     {
//         printf("Enter marks for student %d\n" , i);
//         for (int j = 1; j <= 3; j++)
//         {
//             printf("Sub %d :\n",j);
//             scanf("%d",&sub[j]);
//             printf("%d\n",sub[j]);
//             total=total+sub[j];
//             total1=total/3;
           
//         }
//         printf("Total is %d",total);
//         printf("Avg=%d",total1);
//          total=0;
//     }
//     return 0;
// }