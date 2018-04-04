/*---------------------------------------------------------------------------*-

                                                         Author: Jason Ma
                                                         Date:   Apr 04 2018
                                      NumGame

  File Name:      num_game.cpp
  Description:    TODO
-*---------------------------------------------------------------------------*/

#include <cstdlib>
#include <iostream>
#include <ctime>

#include "num_game.h"

using std::cout;
using std::cerr;
using std::endl;

/*---------------------------------------------------------------------------*
 Name: hash_state
 File: num_game.cpp
  
 Desc: Creates a hash for set of cards. Numbers in nums must be within 1-13 
       inclusive. The hash is calculated using the first 13 primes, and is
       unique for any unique set of nums (unordered).
              
 Param Desc:
 name               description
 ------------------ -----------------------------------------------
 nums               array of card numbers
 len                length of nums
 <return>           hashed state
 *---------------------------------------------------------------------------*/
int hash_state(int nums[], int len) {
  int i;
  int hash = 1;

  for(i = 0; i < len; i++) {
    hash *= P[nums[i] - 1];
  }

  return hash;
}

int main(int argc, char * argv[]) {
  
  int target;
  int num_threads = 1;

  //parse args
  if(argc < 2) {
    cerr << "[usage] ./numgame <TARGET> [num_threads]" << endl;
    return -1;
  }
  
  target = atoi(argv[1]);

  if(argc > 2) {
    num_threads = atoi(argv[2]);
  }

  //print usage and return if target or num_threads are invalid
  if(target <= 0 || num_threads <= 0) {
    cerr << "[usage] ./numgame <TARGET> [num_threads]" << endl;
    cerr << "[usage] Target and num_threads need to be positive ints" << endl;
    return -1;
  }

  

  return 0;
}