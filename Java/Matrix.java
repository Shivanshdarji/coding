import java.util.Random;
public class Matrix {
    public static void main(String[] args) {
System.out.print("Name : Shivansh Darji        ");
   	System.out.print("       En No : 240413107124");
int[][] matrix = new int[6][6];
        	Random random = new Random();
        	for (int i = 0; i < 6; i++) {
            	for (int j = 0; j < 6; j++) {
                		matrix[i][j] = random.nextInt(2); // Generates 0 or 1
            	}
        	}
        	System.out.println("Generated 6x6 Matrix:");
        	for (int i = 0; i < 6; i++) {
            	for (int j = 0; j < 6; j++) {
                		System.out.print(matrix[i][j] + " ");
            	}
            	System.out.println();
        	}
        	boolean rowsValid = checkOddOnesInRows(matrix);
        	boolean colsValid = checkOddOnesInColumns(matrix);
System.out.println("\nChecking if each row has an odd number of 1s: " + (rowsValid ? "Yes" : "No"));
System.out.println("Checking if each column has an odd number of 1s: " + (colsValid ? "Yes" : "No"));
    }
    public static boolean checkOddOnesInRows(int[][] matrix) {
        for (int i = 0; i < 6; i++) {
            int count = 0;
            for (int j = 0; j < 6; j++) {
                if (matrix[i][j] == 1) {
                    count++;
                }
            }
            if (count % 2 == 0) { // Even number of 1s in a row
                return false;
            }
        }
        return true;
    }
    public static boolean checkOddOnesInColumns(int[][] matrix) {
        for (int j = 0; j < 6; j++) {
            int count = 0;
            for (int i = 0; i < 6; i++) {
                if (matrix[i][j] == 1) {
                    	count++;
                }
            }
            if (count % 2 == 0) { // Even number of 1s in a column
                return false;
            }
        }
        return true;
    }
}
