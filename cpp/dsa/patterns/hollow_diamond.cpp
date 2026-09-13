#include<iostream>
using namespace std;
int main()
{
    int n,x;
    x=1;
    cout<<"Enter a number:";
    cin>>n;
    for(int i=1;i<=n;i++)
    {
        for(int j=n;j>=i;j--)
        {
            cout<<" ";
        }
        for(int k=1;k<=(2*i-1);k++)
        {
           if(k==1||k==(2*i-1))
           cout<<"*";
           else
           cout<<" ";
        }
        x=1;
        cout<<endl;
    }
    for(int i=n;i>=1;i--)
    {
        for(int j=1;j<=x;j++)
        {
            cout<<" ";
        }
        x++;
        for(int k=1;k<=(2*i-1);k++)
        {
           if(k==1||k==(2*i-1))
           cout<<"*";
           else
           cout<<" ";
        }
        cout<<endl;
    }
}