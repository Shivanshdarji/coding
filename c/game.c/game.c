#include <stdio.h>
#include <stdbool.h>
#include <SDL2/SDL.h>

// Define some constants for screen size and ball properties
const int SCREEN_WIDTH = 640;
const int SCREEN_HEIGHT = 480;
const int BALL_RADIUS = 20;
const int BALL_SPEED = 5;

int main(int argc, char* argv[]) {
  // Initialize SDL and create a window
  if (SDL_Init(SDL_INIT_VIDEO) < 0) {
    printf("SDL could not initialize! SDL Error: %s\n", SDL_GetError());
    return 1;
  }

  SDL_Window* window = SDL_CreateWindow("Bouncing Ball", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
                                          SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN);

  if (window == NULL) {
    printf("Window could not be created! SDL Error: %s\n", SDL_GetError());
    return 1;
  }

  // Create a renderer for the window
  SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

  if (renderer == NULL) {
    printf("Renderer could not be created! SDL Error: %s\n", SDL_GetError());
    return 1;
  }

  // Define the ball's starting position and movement direction
  int ball_x = SCREEN_WIDTH / 2;
  int ball_y = SCREEN_HEIGHT / 2;
  int ball_x_dir = BALL_SPEED;
  int ball_y_dir = BALL_SPEED;

  // Game loop
  bool running = true;
  while (running) {
    SDL_Event event;
    SDL_PollEvent(&event);

    // Handle closing the window
    if (event.type == SDL_QUIT) {
      running = false;
    }

    // Update ball position based on direction and handle wall collisions
    ball_x += ball_x_dir;
    ball_y += ball_y_dir;

    if (ball_x + BALL_RADIUS >= SCREEN_WIDTH || ball_x <= 0) {
      ball_x_dir = -ball_x_dir;
    }

    if (ball_y + BALL_RADIUS >= SCREEN_HEIGHT || ball_y <= 0) {
      ball_y_dir = -ball_y_dir;
    }

    // Clear the screen
    SDL_SetRenderDrawColor(renderer, 0x00, 0x00, 0x00, 0xFF);
    SDL_RenderClear(renderer);

    // Draw the ball as a filled circle
    SDL_SetRenderDrawColor(renderer, 0xFF, 0xFF, 0xFF, 0xFF);
    SDL_FillCircle(renderer, ball_x, ball_y, BALL_RADIUS);

    // Update the screen
    SDL_RenderPresent(renderer);
  }

  // Clean up SDL resources
  SDL_DestroyRenderer(renderer);
  SDL_DestroyWindow(window);
  SDL_Quit();

  return 0;
}
