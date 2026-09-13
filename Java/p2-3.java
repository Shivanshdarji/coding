import java.util.*;

class Alphabet
{
public static void main(String[] args)
{
char ch;
Scanner s1=new Scanner(System.in);
System.out.println("Name:Shivansh Darji        Enrollment No:230410107124");
System.out.println("\n enter alphabet");
ch=s1.nextLine().charAt(0);

if(ch=='a' || ch=='e' || ch=='i' || ch=='o' || ch=='u' || ch=='A' || ch=='E' || ch=='I' || ch=='O' || ch=='U')
{
System.out.println("\n Character is vowel");
}
else
{
System.out.println("\n Character is consonant");
}
}
}