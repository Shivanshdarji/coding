#include<iostream>
#include<stdio.h>
using namespace std;
int main()
{
    int a,b;
    cout<<"Enter A Number";
    cin>>a;
    cout<<"\nEnter a Number";
    cin>>b;
    if(b>a)
    {
       // cout<<"\nprofit";
        printf("Profit");
        cout<<"\nProfit is="<<b-a;
    }
}