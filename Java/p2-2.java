import java.util.*;

class Desc
{
public static void main(String[] args)
{
int a,b,c;
Scanner s1=new Scanner(System.in);
System.out.println("Name:Shivansh Darji        Enrollment No:230410107124");
System.out.println("\n Enter first number");
a=s1.nextInt();
System.out.println("\n Enter second number");
b=s1.nextInt();
System.out.println("\n Enter third number");
c=s1.nextInt();

int max=-1,mid=-1,min=-1;

if(a>b)
{
if(a>c)
{
max=a;

if(b>c)
{
mid=b;
min=c;
}
else
{
mid=c;
min=b;
}
}
else
{
max=c;
mid=a;
min=b;
}
}
else
{
if(b>c)
{
max=b;
if(a>c)
{
mid=a;
min=c;
}
else
{
mid=c;
min=a;
}
}
else
{
max=c;
mid=b;
min=a;
}
}
System.out.println("\nAfter Decreasing order:");
System.out.println("  "+max+"  "+mid+"  "+min);
}
}