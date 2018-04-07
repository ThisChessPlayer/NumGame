/*-----------------------------------------------------------------------------

                                                         Author: Jason Ma
                                                         Date:   Apr 04 2018
                                      NumGame

  File Name:      num_game.h
  Description:    TODO
-----------------------------------------------------------------------------*/

#ifndef NUM_GAME_H
#define NUM_GAME_H

#include <vector>

using std::vector;

const int MAX_STATE_SIZE = 6; // max num of cards used
const int MAX_NUM = 20000;

//const short P[13] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41}; //primes
unsigned int P[MAX_NUM]; //primes

int hash_state(int nums[], int len);
int worker_func(int id);
bool check_join();
void handle_input();
void load_primes(const char * filename);

class state {
  public:
    state(vector<int> n, const char * s);
    vector<int> nums;
    char sol[8 * MAX_STATE_SIZE];
};

#endif /* NUM_GAME_H */