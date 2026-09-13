import java.util.Scanner;
public class Reverse 
{
 	public static void reverseArray(int[] numbers) 
{
        		int left = 0, right = numbers.length - 1;
        		while (left < right) 
{
            		int temp = numbers[left];
            		numbers[left] = numbers[right];
            		numbers[right] = temp;
            		left++;
            		right--;
        		}
    	}
    	public static void main(String[] args) {
            System.out.print("Name : Shivansh Darji        ");
            System.out.println("       En No : 240413107124");   
        	Scanner input = new Scanner(System.in);
        	int[] numbers = new int[10];
        	System.out.println("Enter 10 numbers: ");
        	for (int i = 0; i < 10; i++) 
{
            	numbers[i] = input.nextInt();
        	}
        	reverseArray(numbers);
        	System.out.print("Reversed numbers: ");
        	for (int num : numbers) 
{
            	System.out.print(num + " ");
        	}
        	input.close();
    }
}
