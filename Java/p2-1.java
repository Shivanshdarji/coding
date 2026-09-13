import java.util.*;
class Bmi
{
public static void main(String[] args)
{
  double weight,inches,BMI;
  Scanner s1=new Scanner(System.in);
  System.out.println("Name:Shivansh Darji        Enrollment No:230410107124");
  System.out.println("\n enter weight in pounds");
  weight=s1.nextDouble();
  System.out.println("\n enter your height in inches ");
  inches=s1.nextDouble();

  BMI=(weight*0.45359237)/(inches*0.0254*inches*0.0254);
  System.out.println("\n BMI="+BMI);
}
}