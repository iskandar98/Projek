#include <iostream>
#include <conio.h>
#include <windows.h>
#include <vector>
#include <cstdlib>
#include <ctime>

using namespace std;

bool gameOver;
const int width = 20;
const int height = 20;
int x, y, fruitX, fruitY, score;
vector<pair<int, int>> snake;
enum eDirection { STOP = 0, LEFT, RIGHT, UP, DOWN };
eDirection dir;

void Setup() {
    gameOver = false;
    dir = STOP;
    x = width / 2;
    y = height / 2;
    snake.push_back({x, y});
    
    srand(time(0));
    fruitX = rand() % width;
    fruitY = rand() % height;
    
    score = 0;
}

void Draw() {
    system("cls");
    
    // Draw top border
    for (int i = 0; i < width + 2; i++)
        cout << "#";
    cout << endl;

    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            if (j == 0)
                cout << "#"; // Left border
            
            // Draw snake head or body
            bool isSnake = false;
            for (int k = 0; k < snake.size(); k++) {
                if (snake[k].first == j && snake[k].second == i) {
                    if (k == 0)
                        cout << "O"; // Head
                    else
                        cout << "o"; // Body
                    isSnake = true;
                    break;
                }
            }
            
            // Draw fruit
            if (!isSnake) {
                if (i == fruitY && j == fruitX)
                    cout << "F";
                else
                    cout << " ";
            }
            
            if (j == width - 1)
                cout << "#"; // Right border
        }
        cout << endl;
    }

    // Draw bottom border
    for (int i = 0; i < width + 2; i++)
        cout << "#";
    cout << endl;
    
    cout << "Score: " << score << endl;
}

void Input() {
    if (_kbhit()) {
        switch (_getch()) {
            case 'a':
                if (dir != RIGHT) dir = LEFT;
                break;
            case 'd':
                if (dir != LEFT) dir = RIGHT;
                break;
            case 'w':
                if (dir != DOWN) dir = UP;
                break;
            case 's':
                if (dir != UP) dir = DOWN;
                break;
            case 'x':
                gameOver = true;
                break;
        }
    }
}

void Logic() {
    if (snake.size() > 1) {
        for (int i = snake.size() - 1; i > 0; i--) {
            snake[i].first = snake[i-1].first;
            snake[i].second = snake[i-1].second;
        }
    }
    
    switch (dir) {
        case LEFT:
            snake[0].first--;
            break;
        case RIGHT:
            snake[0].first++;
            break;
        case UP:
            snake[0].second--;
            break;
        case DOWN:
            snake[0].second++;
            break;
    }
    
    // Check wall collision
    if (snake[0].first >= width || snake[0].first < 0 ||
        snake[0].second >= height || snake[0].second < 0) {
        gameOver = true;
    }
    
    // Check self collision
    for (int i = 1; i < snake.size(); i++) {
        if (snake[0].first == snake[i].first && snake[0].second == snake[i].second) {
            gameOver = true;
        }
    }
    
    // Check fruit collision
    if (snake[0].first == fruitX && snake[0].second == fruitY) {
        score += 10;
        
        // Add new segment to snake
        int tailX = snake.back().first;
        int tailY = snake.back().second;
        
        switch (dir) {
            case LEFT:
                tailX++;
                break;
            case RIGHT:
                tailX--;
                break;
            case UP:
                tailY++;
                break;
            case DOWN:
                tailY--;
                break;
        }
        
        snake.push_back({tailX, tailY});
        
        // Place new fruit
        fruitX = rand() % width;
        fruitY = rand() % height;
    }
}

int main() {
    Setup();
    while (!gameOver) {
        Draw();
        Input();
        Logic();
        Sleep(100); // game speed
    }
    
    cout << "Game Over!" << endl;
    cout << "Final Score: " << score << endl;
    return 0;
}
