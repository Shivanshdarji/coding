#include<iostream>
using namespace std;
int main()
{
    int a,b,c;
    cout<<"Enter 3 Numbers";
    cin>>a>>b>>c;
    c *= c;
    b *=b;
    a*=a;
    if(c=a+b)
    cout<<"possible";
    else
    cout<<"Not Possible";
}