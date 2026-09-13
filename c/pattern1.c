#include <stdio.h>
void main()
{
    int rows,number=1;
    
    printf("Enter number of rows :" , rows);
    scanf("%d", &rows);
    for (int i = 1; i <= rows; i++)
    {
        for (int j = 1; j <= i; j++)
        {
            printf("%d" ,number);
            number++;
        }
        printf("\n");
    }
    
}