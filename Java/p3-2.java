import java.util.*;
class Factors
{
public static void main(String[] args)
{
int i,N;
Scanner s1=new Scanner(System.in);
N=s1.nextInt();
System.out.print("Name:Shivansh Darji        Enrollment No:230410107124\n");
for(i=2;N>1;i++)
{
if(N%i==0)
{
System.out.print(i+" ");

N=N/i;
i=1;
}
}
}
}