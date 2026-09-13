import java.util.Random;
public class RandomIntegers {
    public static void main(String[] args) {
        System.out.println("\nName=Shivansh Darji   En no.230410107124");
        Random r = new Random();
        r.setSeed(1000);
        for (int i = 0; i < 100; i++) {
            System.out.print(" " + r.nextInt(49));
        }
    }
}
