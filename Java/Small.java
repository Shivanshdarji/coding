import java.util.Scanner; public class Small{
    public static int findMinimum(int A[], int n)
    { if(n == 1) return A[0];
    return Math.min(A[n-1], findMinimum(A, n-1)); } public static void main(String args[]){
    System.out.println("Name: Darji Shivansh\n Enroll No.: 230410107124"); Scanner sc= new Scanner(System.in);
    System.out.print("How many elements you want in array?"); int n = sc.nextInt();
    System.out.print("enter elements: "); int A[] = new int[n];
    for (int i=0;i<n;i++){ A[i]=sc.nextInt(); }
    System.out.println("Smallest element in the array is: "+findMinimum(A, n));
    }
    }
    