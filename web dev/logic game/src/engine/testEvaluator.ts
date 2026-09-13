import { CEvaluator } from './CEvaluator';

const evaluator = new CEvaluator();

const code = `
int x = 0;
int sum = 0;
while (x < 5) {
    sum = sum + x;
    x = x + 1;
    printf("x: %d, sum: %d", x, sum);
}
printf("Final sum: %d", sum);
`;

console.log("Testing CEvaluator with while loop...");
const steps = evaluator.evaluate(code);

console.log("Execution Steps:", steps.length);
steps.forEach((step, i) => {
    console.log(`Step ${i + 1} (Line ${step.line}):`);
    console.log("  Variables:", step.variables);
    if (step.output.length > 0) {
        console.log("  Output:", step.output[step.output.length - 1]);
    }
    if (step.error) {
        console.error("  Error:", step.error);
    }
});

if (steps.length > 0 && !steps[steps.length - 1].error) {
    console.log("Test Passed!");
} else {
    console.log("Test Failed!");
}
