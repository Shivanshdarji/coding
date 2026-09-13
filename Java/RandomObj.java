import java.util.Random; 
class RandomObj{ 
    public static void main(String arg[]){ 
        Random r = new Random(1000); 
        System.out.println("Name: Rana Manav    Enroll: 240413107007"); 
        int a = 0; 
        for(int i=0;i<100;i++){ 
            a = r.nextInt(49); 
            System.out.print(a+" "); 
        } 
    } 
} 