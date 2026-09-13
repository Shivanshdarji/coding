export interface VariableValue {
    type: 'int' | 'float' | 'char' | 'pointer';
    value: any;
}

export interface ExecutionStep {
    line: number;
    variables: Record<string, VariableValue>;
    output: string[];
    error?: string;
    stack: string[];
    heap: Record<number, any>;
}

type TokenType =
    | 'KEYWORD' | 'IDENTIFIER' | 'NUMBER' | 'STRING'
    | 'OPERATOR' | 'PUNCTUATION' | 'EOF';

interface Token {
    type: TokenType;
    value: string;
    line: number;
}

export class CEvaluator {
    private tokens: Token[] = [];
    private currentTokenIndex = 0;
    private variables: Record<string, VariableValue> = {};
    private output: string[] = [];
    private steps: ExecutionStep[] = [];
    private heap: Record<number, any> = {};
    private nextHeapAddress = 1000;
    private loopSafety = 0;
    private readonly MAX_LOOP_ITERATIONS = 1000;

    evaluate(code: string): ExecutionStep[] {
        this.tokens = this.tokenize(code);
        this.currentTokenIndex = 0;
        this.variables = {};
        this.output = [];
        this.steps = [];
        this.heap = {};
        this.nextHeapAddress = 1000;
        this.loopSafety = 0;

        try {
            this.parseBlock();
        } catch (e: any) {
            this.steps.push({
                line: this.tokens[this.currentTokenIndex]?.line || 0,
                variables: JSON.parse(JSON.stringify(this.variables)),
                output: [...this.output],
                error: e.message,
                stack: ['main'],
                heap: { ...this.heap }
            });
        }

        return this.steps;
    }

    private tokenize(code: string): Token[] {
        const tokens: Token[] = [];
        let line = 1;
        let i = 0;

        const keywords = new Set(['int', 'float', 'char', 'if', 'else', 'while', 'return', 'printf']);

        while (i < code.length) {
            const char = code[i];

            if (/\s/.test(char)) {
                if (char === '\n') line++;
                i++;
                continue;
            }

            if (/[a-zA-Z_]/.test(char)) {
                let value = '';
                while (i < code.length && /[a-zA-Z0-9_]/.test(code[i])) {
                    value += code[i];
                    i++;
                }
                tokens.push({
                    type: keywords.has(value) ? 'KEYWORD' : 'IDENTIFIER',
                    value,
                    line
                });
                continue;
            }

            if (/[0-9]/.test(char)) {
                let value = '';
                while (i < code.length && /[0-9.]/.test(code[i])) {
                    value += code[i];
                    i++;
                }
                tokens.push({ type: 'NUMBER', value, line });
                continue;
            }

            if (char === '"') {
                let value = '';
                i++; // skip opening quote
                while (i < code.length && code[i] !== '"') {
                    value += code[i];
                    i++;
                }
                i++; // skip closing quote
                tokens.push({ type: 'STRING', value, line });
                continue;
            }

            // Multi-char operators
            if (['=', '!', '<', '>', '&', '|'].includes(char)) {
                if (code[i + 1] === '=') {
                    tokens.push({ type: 'OPERATOR', value: char + '=', line });
                    i += 2;
                    continue;
                }
                if (char === '&' && code[i + 1] === '&') {
                    tokens.push({ type: 'OPERATOR', value: '&&', line });
                    i += 2;
                    continue;
                }
                if (char === '|' && code[i + 1] === '|') {
                    tokens.push({ type: 'OPERATOR', value: '||', line });
                    i += 2;
                    continue;
                }
            }

            if (['+', '-', '*', '/', '%', '=', '(', ')', '{', '}', ';', ',', '[', ']', '&', '*'].includes(char)) {
                tokens.push({ type: /[(){};,\[\]]/.test(char) ? 'PUNCTUATION' : 'OPERATOR', value: char, line });
                i++;
                continue;
            }

            i++; // Skip unknown
        }

        tokens.push({ type: 'EOF', value: '', line });
        return tokens;
    }

    private parseBlock() {
        while (this.currentToken().type !== 'EOF' && this.currentToken().value !== '}') {
            this.parseStatement();
        }
    }

    private parseStatement() {
        const token = this.currentToken();
        // Don't record step for closing braces or empty statements to avoid clutter
        if (token.value !== '}') {
            this.recordStep(token.line);
        }

        if (token.type === 'KEYWORD') {
            if (token.value === 'int' || token.value === 'float' || token.value === 'char') {
                this.parseDeclaration();
            } else if (token.value === 'if') {
                this.parseIf();
            } else if (token.value === 'while') {
                this.parseWhile();
            } else if (token.value === 'printf') {
                this.parsePrintf();
            } else if (token.value === 'return') {
                this.consume('KEYWORD');
                this.parseExpression(); // Ignore return value for now
                this.consume('PUNCTUATION', ';');
            }
        } else if (token.type === 'IDENTIFIER') {
            this.parseAssignment();
        } else {
            this.advance(); // Skip invalid
        }
    }

    private parseDeclaration() {
        const type = this.consume('KEYWORD').value as 'int' | 'float' | 'char';
        const name = this.consume('IDENTIFIER').value;

        let value: any = 0;
        if (this.currentToken().value === '=') {
            this.consume('OPERATOR', '=');
            value = this.parseExpression();
        }

        this.consume('PUNCTUATION', ';');
        this.variables[name] = { type, value };
        this.recordStep(this.currentToken().line);
    }

    private parseAssignment() {
        const name = this.consume('IDENTIFIER').value;

        // Handle array assignment later if needed

        this.consume('OPERATOR', '=');
        const value = this.parseExpression();
        this.consume('PUNCTUATION', ';');

        if (this.variables[name]) {
            this.variables[name].value = value;
        } else {
            throw new Error(`Undefined variable: ${name}`);
        }
        this.recordStep(this.currentToken().line);
    }

    private parseIf() {
        this.consume('KEYWORD', 'if');
        this.consume('PUNCTUATION', '(');
        const condition = this.parseExpression();
        this.consume('PUNCTUATION', ')');
        this.consume('PUNCTUATION', '{');

        if (condition) {
            this.parseBlock();
            this.consume('PUNCTUATION', '}');
            // Handle else if needed, skipping it
            if (this.currentToken().value === 'else') {
                this.consume('KEYWORD', 'else');
                this.consume('PUNCTUATION', '{');
                this.skipBlock();
                this.consume('PUNCTUATION', '}');
            }
        } else {
            this.skipBlock();
            this.consume('PUNCTUATION', '}');
            if (this.currentToken().value === 'else') {
                this.consume('KEYWORD', 'else');
                this.consume('PUNCTUATION', '{');
                this.parseBlock();
                this.consume('PUNCTUATION', '}');
            }
        }
    }

    private parseWhile() {
        const startTokenIndex = this.currentTokenIndex;
        this.consume('KEYWORD', 'while');
        this.consume('PUNCTUATION', '(');

        // We need to parse the expression to check condition, but we need to be able to re-parse it.
        // Since our parser consumes tokens, we need to reset index.

        // Strategy:
        // 1. Remember start index of 'while'.
        // 2. Parse condition.
        // 3. If true:
        //    a. Parse block.
        //    b. Jump back to start index.
        // 4. If false:
        //    a. Skip block.

        // Problem: parseExpression consumes tokens. We need to know where the condition ENDS to jump back to it?
        // No, we jump back to the 'while' token, re-parse 'while', re-parse '(', re-parse condition.

        // To do this properly, we need to evaluate the condition without side effects?
        // Or just let it consume, and if we loop, we reset the index.

        // But wait, we've already consumed 'while' and '(' above.
        // So if we loop, we reset to startTokenIndex.

        // Let's reset to just before parsing expression for the check?
        // No, easier to reset to the very beginning of the loop structure.

        // We need to know if the condition is true.
        // We are currently at the start of the expression.
        // We are currently at the start of the expression.
        const condition = this.parseExpression();
        this.consume('PUNCTUATION', ')');
        this.consume('PUNCTUATION', '{');

        if (condition) {
            this.loopSafety++;
            if (this.loopSafety > this.MAX_LOOP_ITERATIONS) {
                throw new Error("Infinite loop detected!");
            }

            this.parseBlock();
            this.consume('PUNCTUATION', '}');

            // Jump back
            this.currentTokenIndex = startTokenIndex;
            // We are now back at 'while'. The next call to parseStatement (or the loop in parseBlock) 
            // will call parseWhile again.
            // Wait, parseWhile is called by parseStatement.
            // If we reset index here, we are inside parseWhile.
            // We shouldn't recurse infinitely.

            // If we reset index, we return from this function?
            // No, if we return, the caller (parseBlock) continues to next token.
            // But we reset the index to 'while'.
            // So the caller will see 'while' again and call parseWhile again.
            // This works!

        } else {
            this.loopSafety = 0;
            this.skipBlock();
            this.consume('PUNCTUATION', '}');
        }
    }

    private skipBlock() {
        let depth = 1;
        while (depth > 0 && this.currentToken().type !== 'EOF') {
            if (this.currentToken().value === '{') depth++;
            if (this.currentToken().value === '}') depth--;
            // Don't consume the final closing brace here, let the caller do it
            if (depth === 0) break;
            this.advance();
        }
    }

    private parsePrintf() {
        this.consume('KEYWORD', 'printf');
        this.consume('PUNCTUATION', '(');
        const format = this.consume('STRING').value;
        // Handle args if any
        let output = format;
        while (this.currentToken().value === ',') {
            this.consume('PUNCTUATION', ',');
            const val = this.parseExpression();
            output = output.replace(/%[dfc]/, String(val));
        }
        this.consume('PUNCTUATION', ')');
        this.consume('PUNCTUATION', ';');
        this.output.push(output);
        this.recordStep(this.currentToken().line);
    }

    private parseExpression(): any {
        return this.parseLogicalOr();
    }

    private parseLogicalOr(): any {
        let left = this.parseLogicalAnd();
        while (this.currentToken().value === '||') {
            this.consume('OPERATOR');
            const right = this.parseLogicalAnd();
            left = left || right;
        }
        return left;
    }

    private parseLogicalAnd(): any {
        let left = this.parseEquality();
        while (this.currentToken().value === '&&') {
            this.consume('OPERATOR');
            const right = this.parseEquality();
            left = left && right;
        }
        return left;
    }

    private parseEquality(): any {
        let left = this.parseRelational();
        while (['==', '!='].includes(this.currentToken().value)) {
            const op = this.consume('OPERATOR').value;
            const right = this.parseRelational();
            if (op === '==') left = (left === right ? 1 : 0);
            if (op === '!=') left = (left !== right ? 1 : 0);
        }
        return left;
    }

    private parseRelational(): any {
        let left = this.parseAdditive();
        while (['<', '>', '<=', '>='].includes(this.currentToken().value)) {
            const op = this.consume('OPERATOR').value;
            const right = this.parseAdditive();
            if (op === '<') left = (left < right ? 1 : 0);
            if (op === '>') left = (left > right ? 1 : 0);
            if (op === '<=') left = (left <= right ? 1 : 0);
            if (op === '>=') left = (left >= right ? 1 : 0);
        }
        return left;
    }

    private parseAdditive(): any {
        let left = this.parseMultiplicative();
        while (this.currentToken().value === '+' || this.currentToken().value === '-') {
            const op = this.consume('OPERATOR').value;
            const right = this.parseMultiplicative();
            if (op === '+') left += right;
            if (op === '-') left -= right;
        }
        return left;
    }

    private parseMultiplicative(): any {
        let left = this.parseFactor();
        while (this.currentToken().value === '*' || this.currentToken().value === '/' || this.currentToken().value === '%') {
            const op = this.consume('OPERATOR').value;
            const right = this.parseFactor();
            if (op === '*') left *= right;
            if (op === '/') left /= right;
            if (op === '%') left %= right;
        }
        return left;
    }

    private parseFactor(): any {
        const token = this.currentToken();
        if (token.type === 'NUMBER') {
            this.advance();
            return parseFloat(token.value);
        } else if (token.type === 'IDENTIFIER') {
            this.advance();
            return this.variables[token.value]?.value || 0;
        } else if (token.value === '(') {
            this.consume('PUNCTUATION', '(');
            const val = this.parseExpression();
            this.consume('PUNCTUATION', ')');
            return val;
        } else if (token.value === '-') {
            this.consume('OPERATOR', '-');
            return -this.parseFactor();
        } else if (token.value === '!') {
            this.consume('OPERATOR', '!');
            return !this.parseFactor() ? 1 : 0;
        }
        return 0;
    }

    private consume(type: TokenType, value?: string): Token {
        const token = this.currentToken();
        if (token.type === type && (!value || token.value === value)) {
            this.advance();
            return token;
        }
        throw new Error(`Expected ${value || type}, found ${token.value} at line ${token.line}`);
    }

    private advance() {
        this.currentTokenIndex++;
    }

    private currentToken(): Token {
        return this.tokens[this.currentTokenIndex] || { type: 'EOF', value: '', line: 0 };
    }

    private recordStep(line: number) {
        this.steps.push({
            line,
            variables: JSON.parse(JSON.stringify(this.variables)),
            output: [...this.output],
            stack: ['main'],
            heap: { ...this.heap }
        });
    }
}
