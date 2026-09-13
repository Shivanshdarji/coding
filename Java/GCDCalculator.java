import java.util.Scanner;
public class GCDCalculator 		
{
 	public static int gcd(int num1, int num2) 
{
      while (num2 != 0) 
{
       	int temp = num2;
       	num2 = num1 % num2;
       	num1 = temp;
        }
        return num1;
    	  }
    	  public static void main(String[] args) {
  System.out.print("Name : Shivansh Darji        ");
   	  System.out.println("       En No : 240413107124");
        Scanner input = new Scanner(System.in);
        System.out.print("Enter the first integer: ");
        int num1 = input.nextInt();
        System.out.print("Enter the second integer: ");
        int num2 = input.nextInt();
        int result = gcd(num1, num2);
 System.out.println("The GCD of " + num1 + " and " + num2 + " is: " + result);
       input.close();
    }
   } 
