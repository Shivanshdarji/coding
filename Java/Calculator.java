import java.util.Scanner;
class Calculator {
    public static void main(String[] args) {
        System.out.println("\nName=Shivansh Darji    En no.230410107124");
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter Expression : ");
        String exp = sc.nextLine();
        if (exp.contains("+")) {
            String[] t = exp.split("\\+");
            double result = Integer.parseInt(t[0].trim());
            for (int i = 1; i < t.length; i++) {
                result = result + Integer.parseInt(t[i].trim());
            }
            System.out.println("Result : " + result);
        } else if (exp.contains("-")) {
            String[] t = exp.split("\\-");
            double result = Integer.parseInt(t[0].trim());
            for (int i = 1; i < t.length; i++) {
                result = result - Integer.parseInt(t[i].trim());
            }
            System.out.println("Result : " + result);
        } else if (exp.contains("*")) {
            String[] t = exp.split("\\*");
            double result = Integer.parseInt(t[0].trim());
            for (int i = 1; i < t.length; i++) {
                result = result * Integer.parseInt(t[i].trim());
            }
            System.out.println("Result : " + result);
        } else if (exp.contains("/")) {
            String[] t = exp.split("\\/");
            double result = Integer.parseInt(t[0].trim());
            for (int i = 1; i < t.length; i++) {
                result = result / Integer.parseInt(t[i].trim());
            }
            System.out.println("Result : " + result);
        }
    }
}
