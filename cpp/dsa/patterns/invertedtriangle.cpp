#include<iostream>
using namespace std;
int main()
{
    int n,z;
    z=1;
    cout<<"Enter a number:";
    cin>>n;
    for(int i=1;i<=n;i++)
    {
        for(int j=i;j>0;j--)
        {
            cout<<" ";
        }for(int k=2*n;k>=(2*i);k--)
        {
            cout<<z;
        }
        z++;
    cout<<endl;
    }
    return 0;
}