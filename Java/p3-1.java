import java.util.*;
class Plate
{
public static void main(String[] args)
{
Random r=new Random();
int i;
System.out.print("Name:Shivansh Darji        Enrollment No:230410107124");
System.out.print("\nVehicle number is:");
for(i=0;i<7;i++)
{
if(i<3)
{
System.out.print((char)(r.nextInt(26)+65));
}
else
{
System.out.print(r.nextInt(10));
}
}
}
}