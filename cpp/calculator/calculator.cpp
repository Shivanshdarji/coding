#include<iostream>
#include<string.h>
using namespace std;
int main ()
{
    float a,c,anss;
    ans:
    char b[10];
    cout<<"Enter Your Eq=";
    cin>>b;
   
    for(int i=0;i!='\0';i++)
    {

   
    if(b[i]=='*')
    {
        anss=(b[i-1])*(b[i+1]);
    }
    else if(b[i]=='/')
    {
        
        
        anss=(b[i-1])/(b[i+1]);
        
    }
    else if(b[i]=='+')
    {
       anss=(b[i-1])+(b[i+1]) ;
       
    }
    else if(b[i]=='-')
    {
       anss=b[i-1]-b[i+1];
        
    }
    cout<<anss<<endl;
    goto ans;
}
}