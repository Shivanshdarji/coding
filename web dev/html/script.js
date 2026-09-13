let questionCounter = 0;

// Questions categorized
const mcqQuestions = [
  {
    question: "What will be the output of `if(5 > 3)`?",
    options: ["True", "False", "Error", "None"],
    correct: "True"
  },
  {
    question: "Which symbol is used for equality check in C?",
    options: ["=", "==", "!=", "==="],
    correct: "=="
  }
];

const fillInQuestions = [
  {
    question: "Fill in the blank: `if({condition}) printf('Hello');`",
    blank: "{condition}",
    correct: "5 > 3"
  },
  {
    question: "Write the missing part: `if(a ___ b)` to check if a is greater than b.",
    blank: "___",
    correct: ">"
  }
];

const codingProblems = [
  {
    question: "Write a C program that checks if a number is even or odd.",
    example: "// Input: 4\n// Output: Even",
    correct: "if(num % 2 == 0)"
  },
  {
    question: "Write a C program to find the maximum of two numbers.",
    example: "// Input: a=5, b=7\n// Output: Maximum is 7",
    correct: "if(a > b)"
  }
];

// Generate a new question based on the counter
function generateQuestion() {
  const questionContainer = document.getElementById("question");
  const optionsContainer = document.getElementById("options");
  const codeEditor = document.getElementById("code-editor");
  const answerInput = document.getElementById("answer");

  optionsContainer.innerHTML = "";
  codeEditor.style.display = "none";
  answerInput.style.display = "none";
  document.getElementById("feedback").textContent = "";

  if (questionCounter < 2) {
    // MCQ Question
    const question = mcqQuestions[questionCounter];
    questionContainer.textContent = question.question;
    question.options.forEach(option => {
      const button = document.createElement("button");
      button.textContent = option;
      button.onclick = () => checkMCQAnswer(option, question.correct);
      optionsContainer.appendChild(button);
    });
  } else if (questionCounter < 4) {
    // Fill-in-the-blank Question
    const question = fillInQuestions[questionCounter - 2];
    questionContainer.innerHTML = question.question.replace(question.blank, `<span class="blank">${question.blank}</span>`);
    answerInput.style.display = "block";
    answerInput.dataset.correct = question.correct;
  } else if (questionCounter < 6) {
    // Coding Problem
    const question = codingProblems[questionCounter - 4];
    questionContainer.textContent = `${question.question}\n\n${question.example}`;
    codeEditor.style.display = "block";
    codeEditor.dataset.correct = question.correct;
  }

  questionCounter = (questionCounter + 1) % 6;
}

// Check MCQ answer
function checkMCQAnswer(selected, correct) {
  const feedback = document.getElementById("feedback");
  if (selected === correct) {
    feedback.textContent = "Correct! 🎉";
    feedback.style.color = "green";
  } else {
    feedback.textContent = `Wrong! The correct answer is: ${correct}`;
    feedback.style.color = "red";
  }
}

// Check other answers
function checkAnswer() {
  const answerInput = document.getElementById("answer");
  const codeEditor = document.getElementById("code-editor");
  const feedback = document.getElementById("feedback");

  if (answerInput.style.display !== "none") {
    // Fill-in-the-blank validation
    const userAnswer = answerInput.value.trim();
    if (userAnswer === answerInput.dataset.correct) {
      feedback.textContent = "Correct! 🎉";
      feedback.style.color = "green";
    } else {
      feedback.textContent = `Wrong! Correct answer is: ${answerInput.dataset.correct}`;
      feedback.style.color = "red";
    }
  } else if (codeEditor.style.display !== "none") {
    // Coding problem validation
    const userCode = codeEditor.value.trim();
    if (userCode.includes(codeEditor.dataset.correct)) {
      feedback.textContent = "Well done! Your code is correct. 🎉";
      feedback.style.color = "green";
    } else {
      feedback.textContent = `Incorrect. Hint: Use "${codeEditor.dataset.correct}" in your code.`;
      feedback.style.color = "red";
    }
  }
}

// Event listeners
document.getElementById("generate-question").addEventListener("click", generateQuestion);
document.getElementById("check-answer").addEventListener("click", checkAnswer);
