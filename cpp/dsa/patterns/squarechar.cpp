#include <iostream>
using namespace std;
int n;
char a;
int main()
{
    a='A';
    cout << "Enter a number=";
    cin >> n;
    for(int i=1;i<=n;i++)
    {
         for(int j=1;j<=n;j++)
        {
            cout<<a<<" ";
            a++;
        }
        a='A';
        cout<<endl;
    }
    return 0;
}