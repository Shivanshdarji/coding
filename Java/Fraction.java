import java.util.*; class Fraction{
    public static void main(String[] ar){ String num;
    Scanner r = new Scanner(System.in);
    System.out.println("Name: Darji Shivansh          Enroll no.: 240410107124 "); 
    System.out.print("Enter Decimal number:");
    num = r.next();
    double n = Double.parseDouble(num); int nume = 1,deno = 1,gcd = 0; while(n%1 != 0){
    n = n*10;
    deno = deno * 10;
    }
    nume = (int)n;
    for(int i = 2; i<=nume || i<=deno; i++){ if(nume%i == 0 && deno%i == 0){ gcd = i;
    }
    }
    nume /= gcd; deno /= gcd;
    System.out.println(num+" in fraction is: "+nume+"/"+deno);
    }
    }
    