import java.util.*; 
import java.lang.Integer; 
class Equation{ 
    public static void main(String arg[]){ 
        System.out.println("Name: Rana Manav    Enroll: 240413107007"); 
        System.out.println("Enter expression: "); 
        String n1="",n2="",expr = ""; 
 char op =' '; 
        int num1=0,num2=0; 
        Scanner r = new Scanner(System.in); 
        expr = r.next(); 
        for(int i=0; i<expr.length(); i++){ 
            if(expr.charAt(i)=='+' || expr.charAt(i)=='-' || expr.charAt(i)=='*' || 
expr.charAt(i)=='/' || expr.charAt(i)=='%'){ 
                op = expr.charAt(i); 
                num1 = Integer.parseInt(n1); 
                n1 = ""; 
                continue; 
            } 
            n1 = n1 + ""+expr.charAt(i); 
        } 
        num2 = Integer.parseInt(n1); 
        switch(op){ 
            case '+': 
                System.out.println(num1+num2); 
                break; 
            case '-': 
                System.out.println(num1-num2); 
                break; 
            case '*': 
                System.out.println(num1*num2); 
                break; 
            case '/': 
                System.out.println(num1/num2); 
                break; 
            case '%': 
                System.out.println(num1%num2); 
                break; 
        } 
    } 
}