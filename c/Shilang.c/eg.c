#include <stdio.h>
#include <string.h>

// Define keywords (can be expanded for more functionality)
#define PRINT "print"

// Function to handle print statements
void shillong_print(char *arg) {
  // Remove leading/trailing quotes (if any) for the argument
  if (arg[0] == '"' && arg[strlen(arg) - 1] == '"') {
    arg[strlen(arg) - 1] = '\0';
    arg++;
  }
  printf("%s\n", arg);
}

// Function to interpret a single Shillong statement
void interpret_statement(char *statement) {
  char *parts[2]; // Assuming maximum of 2 parts (keyword and argument)

  // Split the statement at the first whitespace
  parts[0] = strtok(statement, " ");
  parts[1] = strtok(NULL, " "); // Get the next token (argument)

  // Check if the first part is a keyword
  if (strcmp(parts[0], PRINT) == 0) {
    if (parts[1] != NULL) {
      shillong_print(parts[1]);
    } else {
      printf("Error: Missing argument for print\n");
    }
  } else {
    printf("Error: Unknown keyword '%s'\n", parts[0]);
  }
}

int main() {
  char input[100];

  printf("Shillong interpreter (very basic!)\n");

  while (1) {
    printf("> ");
    fgets(input, sizeof(input), stdin); // Read user input

    // Remove trailing newline character
    if (strchr(input, '\n') != NULL) {
      input[strcspn(input, "\n")] = '\0';
    }

    // Skip empty lines
    if (strlen(input) == 0) {
      continue;
    }

    interpret_statement(input);
  }

  return 0;
}
