export interface Level {
    id: number;
    title: string;
    description: string;
    initialCode: string;
    hint: string;
    validate: (output: string[], variables: Record<string, any>) => boolean;
}

export const levels: Level[] = [
    {
        id: 1,
        title: "Boot Camp: The Awakening",
        description: "System initialized. Welcome, Cadet. Your memory banks are empty. To begin your journey, you must declare your first variable. Initialize an integer named 'energy' to 100 to power up your suit.",
        initialCode: `// Initialize your suit's energy
int energy = 0;
printf("Energy level: %d", energy);`,
        hint: "Change the value of 'energy' to 100. The system needs full power.",
        validate: (output: string[], variables: Record<string, any>) => {
            return variables['energy'] === 100;
        }
    },
    {
        id: 2,
        title: "Variable Isle: Data Types",
        description: "We've reached the Variable Isle. The terrain is shifting. You need to calibrate your sensors. Create a float variable named 'gravity' and set it to 9.8. Also, declare a char named 'sector' and set it to 'A'.",
        initialCode: `// Calibrate sensors
float gravity = 0.0;
char sector = 'Z';
printf("Gravity: %f, Sector: %c", gravity, sector);`,
        hint: "Set 'gravity' to 9.8 and 'sector' to 'A'. Precision is key.",
        validate: (output: string[], variables: Record<string, any>) => {
            return Math.abs(variables['gravity'] - 9.8) < 0.01 && variables['sector'] === 'A';
        }
    },
    {
        id: 3,
        title: "Looping Marsh: The Infinite Path",
        description: "The path ahead is blocked by a repeating signal. We need to synchronize with the loop. Create a while loop that prints numbers from 1 to 5 to break the cycle.",
        initialCode: `// Break the loop cycle
int i = 1;
while (i <= 0) {
    printf("%d", i);
    i = i + 1;
}`,
        hint: "The condition 'i <= 0' prevents the loop from running. Change it to 'i <= 5'.",
        validate: (output: string[], variables: Record<string, any>) => {
            // Check if output contains 1, 2, 3, 4, 5
            const joinedOutput = output.join(' ');
            return joinedOutput.includes('1') && joinedOutput.includes('5');
        }
    },
    {
        id: 4,
        title: "Array Reef: Data Streams",
        description: "We are navigating through the Array Reef. Multiple data streams are incoming. Store the first 3 prime numbers (2, 3, 5) in separate variables named 'p1', 'p2', 'p3'. (Arrays are currently simulated as individual variables for stability).",
        initialCode: `// Capture data streams
int p1 = 0;
int p2 = 0;
int p3 = 0;
printf("Primes: %d, %d, %d", p1, p2, p3);`,
        hint: "Set p1=2, p2=3, p3=5. We need these coordinates.",
        validate: (output: string[], variables: Record<string, any>) => {
            return variables['p1'] === 2 && variables['p2'] === 3 && variables['p3'] === 5;
        }
    },
    {
        id: 5,
        title: "Pointers Lab: Memory Lane",
        description: "Welcome to the Pointers Lab. Here, we manipulate the fabric of memory itself. Create an integer 'target' with value 50. Then create a pointer 'ptr' that points to 'target' (simulated by assigning the name of the variable as a string for now, or just matching the value).",
        initialCode: `// Target memory location
int target = 0;
// In this simulation, just ensure target is set correctly.
printf("Target: %d", target);`,
        hint: "Set 'target' to 50. Direct memory manipulation is restricted in this sector.",
        validate: (output: string[], variables: Record<string, any>) => {
            return variables['target'] === 50;
        }
    },
    {
        id: 6,
        title: "Recursion Tower: The Spiral",
        description: "We've reached the summit: Recursion Tower. To ascend, we must understand the spiral. Calculate the factorial of 5 using a loop (since recursion stack is unstable). Store the result in 'factorial'.",
        initialCode: `// Calculate 5!
int n = 5;
int factorial = 1;
int i = 1;
while (i <= n) {
    // Multiply factorial by i
    i = i + 1;
}
printf("Factorial of 5: %d", factorial);`,
        hint: "Inside the loop, update 'factorial' by multiplying it with 'i': factorial = factorial * i;",
        validate: (output: string[], variables: Record<string, any>) => {
            return variables['factorial'] === 120;
        }
    }
];
