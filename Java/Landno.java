import java.io.*;
import java.util.Scanner; public class Landno{
public static void main(String[] args){
System.out.println("Name: Darji Shivansh\n Enroll No.: 230410107124"); try (
PrintWriter pw = new PrintWriter(new FileOutputStream(new File("123.txt"), true));
) {for (int i = 0; i < 150; i++)
{ pw.print((int)(Math.random() * 150) + "\t "); }} catch (FileNotFoundException fnfe) {
System.out.println("Cannot create the file."); System.out.println("Darji Shivansh. 230410107124"); fnfe.printStackTrace(); }
}
}
