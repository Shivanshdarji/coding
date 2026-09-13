#include<iostream>
using namespace std;
int main()
{
    int a,b;
    a=rand()%100;
    cout<<"Enter Your Number=";
    cin>>b;
   // cout<<"The no was "<<a<<endl;
    if(a==b)
    {cout<<"WOW!! YOU WON!!!";}
    else
    cout<<"YOU LOSE!!!";
    return 0;
}