import java.util.PriorityQueue; import java.util.Queue;
public class MYPriorityQueue<E> extends PriorityQueue<E> implements Cloneable { public MYPriorityQueue() { super(); }
public MYPriorityQueue(int initialCapacity) { super(initialCapacity); } public MYPriorityQueue(int initialCapacity, java.util.Comparator<? super E>
comparator) {
super(initialCapacity, comparator); } public MYPriorityQueue<E> clone() {
MYPriorityQueue<E> clonedQueue = new MYPriorityQueue<>(this.size(), this.comparator());
clonedQueue.addAll(this); return clonedQueue;
}
public static void main(String[] args) {
System.out.println("Name: Darji Shivansh\n Enroll No.: 230410107124"); MYPriorityQueue<Integer> originalQueue = new MYPriorityQueue<>(); originalQueue.add(10);	originalQueue.add(5);  originalQueue.add(15);
MYPriorityQueue<Integer> clonedQueue = originalQueue.clone(); System.out.println("Original Queue: " + originalQueue); System.out.println("Cloned Queue: " + clonedQueue); originalQueue.poll();
}}
