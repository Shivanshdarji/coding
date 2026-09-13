import java.util.Date;
import java.util.ArrayList;
public class Arraylist{
    public static void main(String[] args) {
System.out.println("\nName=Shivansh Darji       En no. 230410107124");
     ArrayList<Object> a1 = new ArrayList<Object>();
        loan a2 = new loan();
        Date a3 = new Date();
        String a4 = new String("Hello how are you?");
        Circle a5 = new Circle();
        a1.add(a2);
        a1.add(a3);
        a1.add(a4);
        a1.add(a5);
        System.out.println(a1);
        a1.add(new Circle(5));
        a1.add(new loan(10000000));
        for (Object i : a1) {
            System.out.println(i);
        }
    }
}
class loan {
    private double amount;
    private int ac;
    loan() {
        this.amount = 1000000;
        this.ac = (int) (Math.random() + 100);
    }
    loan(int amount) {
        this.amount = amount;
        this.ac = (int) (Math.random() + 100);
    }
    double getam() {
        return amount;
    }
    int getacc() {
        return ac;
    }
    public String toString() {
        return "The loan Amount is : " + getam() + " and account number " + getacc();
    }
}

class Circle {
    private double area;
    private int radius;
    Circle() {
        this.radius = 2;
        this.area = Math.PI * Math.pow(2, 2);
    }
    Circle(int radius) {
        this.radius = radius;
        this.area = Math.PI * Math.pow(radius, 2);
    }
    int getr() {
        return radius;
    }
    double getarea() {
        return area;
    }
    public String toString() {
        return "The radius is : " + getr() + " and area is : " + getarea();
    }
}

