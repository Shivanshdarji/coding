import java.util.Scanner;
public class BinaryToDecimal {
    public static void main(String[] args) {
       System.out.println("\nName=Shivansh Darji     En no. 230410107124");
        System.out.println("Enter the number:");
        Scanner sc = new Scanner(System.in);
        String a1 = sc.next();
        sc.close();
        try {
            if (Integer.parseInt(""+a1.charAt(0))!=0 && Integer.parseInt(""+a1.charAt(0))!=1) {
                throw new NumberFormatException("The number is not binary");
            }
            int l=a1.length();
            int dec = 0;
            for (int i = 0; i < a1.length(); i++) {
                dec = (int) (dec + (Integer.parseInt(""+a1.charAt(i))*Math.pow(2,l-i-1)));
            }
            System.out.println(dec);
        } catch (NumberFormatException e) {
            System.out.println("Exception "+e.getMessage());
        }
    }
}
