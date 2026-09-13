#include <iostream>
using namespace std;

void printBoard(char num[5][5]) {
    for(int i = 0; i < 5; ++i) {
        for(int j = 0; j < 5; ++j) {
            cout << num[i][j];
        }
        cout << endl;
    }
}
int checkWin(char num[5][5], char player) {
    for(int i = 0; i < 5; i += 2) {
        if(num[i][0] == player && num[i][2] == player && num[i][4] == player)
            return (player == 'x') ? 1 : 2; 
        if(num[0][i] == player && num[2][i] == player && num[4][i] == player)
            return (player == 'x') ? 1 : 2; 
    }
    if(num[0][0] == player && num[2][2] == player && num[4][4] == player)
        return (player == 'x') ? 1 : 2; 
    if(num[0][4] == player && num[2][2] == player && num[4][0] == player)
        return (player == 'x') ? 1 : 2; 
    
    return 0; 
}

int main() {
    game:
    int ans;
    char board[5][5] = {
        {' ', '|', ' ', '|', ' '},
        {'-', '+', '-', '+', '-'},
        {' ', '|', ' ', '|', ' '},
        {'-', '+', '-', '+', '-'},
        {' ', '|', ' ', '|', ' '}
    };

    char currentPlayer = 'x';

    for(int turn = 1; turn <= 9; ++turn) {
        
        printBoard(board);
        
        
        int cell;
        while(true) {
            cout << "Player " << currentPlayer << "'s turn (enter a number 1-9): ";
            cin >> cell;
            int row = (cell - 1) / 3 * 2;
            int col = ((cell - 1) % 3) * 2;
            
            if(cell >= 1 && cell <= 9 && board[row][col] == ' ') {
                board[row][col] = currentPlayer;
                break;
            } else {
                cout << "Invalid move. Please choose an empty cell (1-9).\n";
            }
        }
        
       
        int result = checkWin(board, currentPlayer);
        
        if(result == 1 || result == 2) {
            printBoard(board);
            cout << "Player " << currentPlayer << " wins!\n";
            cout<<"If You Want to play again Enter 1 and to exit enter 2=";
            num:
            cin>>ans;        
            if(ans==1)
            goto game;
            else if(ans!=1||ans!=2)
           { cout<<"Wrong Input Please Enter 1 or 2";goto num;}
           else
            return 0;
        }
        currentPlayer = (currentPlayer == 'x') ? 'o' : 'x';
    }
    printBoard(board);
    cout << "It's a tie!\n";
    cout<<"If You Want to play again Enter 1 and to exit enter 2=";
    numm:
    cin>>ans;
    if(ans==1)
    goto game;
    else if(ans!=1||ans!=2)
           { cout<<"Wrong Input Please Enter 1 or 2";goto numm;}
    else
    return 0;
}
