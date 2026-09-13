#include <iostream>
using namespace std;
int n;
int main()
{
    cout << "Enter a number=";
    cin >> n;
    for(int i=1;i<=n;i++)
    {
         for(int j=1;j<=n;j++)
        {
            cout<<j;
        }
        cout<<endl;
    }
    return 0;
}