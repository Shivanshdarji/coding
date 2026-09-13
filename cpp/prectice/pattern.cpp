#include<iostream>
using namespace std;
int main()
{
    int i,j;
    for(i=1;i<=6;i++)
    {
        for(j=1;j<=4;j++)
        {
            if(j==2&&i!=1&&i!=6)
            cout<<" ";
            else if(j==3&&i!=1&&i!=6)
            cout<<" ";
            else 
            cout<<"*";
        }
        cout<<"\n";
    }
}