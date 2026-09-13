#include<iostream>
#include<ctime>
using namespace std;
int main()
{
    num:
    int num,ans,ans1;
    srand(time(0));
    
    cout<<"Enter 1=for Easy Mode\n"<<"Enter 2=for Medium Mode\n"<<"Enter 3=for Hard Mode\n";
    cin>>ans;
    if(ans<1||ans>3)
     goto num;
    else if(ans==1)
    {
        num=rand()%10;
        anss:
        cout<<"Enter Number Between 1-10=";
        cin>>ans1;
         if(ans1<num)
        {
            cout<<"Add some more number and try!!!\n";
            goto anss;
        }
        else if(ans1>num)
        {
            cout<<"TOO HIGH!!! GO DOWN!!!\n";
            goto anss;
        }
        else if(ans1==num)
        {cout<<"You Won!!!\n";
        goto num;}
      
    }
     else if(ans==2)
    {
        num=rand()%100;
        ansss:
        cout<<"Enter Number Between 1-100=";
        cin>>ans1;
         if(ans1<num)
        {
            cout<<"Add some more number and try!!!\n";
            goto ansss;
        }
        else if(ans1>num)
        {
            cout<<"TOO HIGH!!! GO DOWN!!!\n";
            goto ansss;
        }
        else if(ans1==num)
        {cout<<"You Won!!!\n";
        goto num;}
       
    }
    else if(ans==3)
    {
        num=rand()%1000;
        anssss:
        cout<<"Enter Number Between 1-1000=";
        cin>>ans1;
        if(ans1<num)
        {
            cout<<"Add some more number and try!!!\n";
            goto anssss;
        }
        else if(ans1>num)
        {
            cout<<"TOO HIGH!!! GO DOWN!!!\n";
            goto anssss;
        }
        else if(ans1==num)
        {cout<<"You Won!!!\n";
        goto num;}
        
        
    }
    
    return 0;
}