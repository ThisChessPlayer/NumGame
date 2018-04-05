/*---------------------------------------------------------------------------*-

                                                         Author: Jason Ma
                                                         Date:   Apr 04 2018
                                      NumGame

  File Name:      num_game.cpp
  Description:    TODO
-*---------------------------------------------------------------------------*/

#include <chrono>
#include <cstdlib>
#include <ctime>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <queue>
#include <sstream>
#include <string>
#include <thread>

#include "num_game.h"

using namespace std::chrono;

using std::cin;
using std::cout;
using std::cerr;
using std::endl;
using std::getline;
using std::ifstream;
using std::queue;
using std::setw;
using std::string;
using std::stringstream;
using std::thread;

/*[Global Variables]---------------------------------------------------------*/
queue<state> * q;

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

int worker_func(int id) {
  stringstream msg;
  //int i;

  msg << "[" << setw(4) << id << setw(1) << "] Started" << endl;
  cout << msg.str();

  //TODO implement this as well as helper funcs

  return 0;
}

void handle_input() {
  string input;

  while(getline(cin, input)) {
    cout << input << endl;

    if(input == "q")
      break;

    //TODO parse input and pass it along to q[0].
  }
}

int main(int argc, char * argv[]) {
  
  int i;
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

  //get ready for some hashing
  load_primes("primes.txt");

  thread t[num_threads];

  //have a queue for each thread to process
  q = new queue<state>[num_threads];

  //TODO put timing inside handle input so it only times the computations
  auto start_time = high_resolution_clock::now();

  //create threads and have them be ready to accept tasks from the queue
  for(i = 0; i < num_threads; i++) {
    t[i] = thread(worker_func, i);
  }

  //send init state to queue and wait for all to be empty
  handle_input();

  for(i = 0; i < num_threads; i++) {
    t[i].join();
  }

  auto end_time = high_resolution_clock::now();

  nanoseconds delta_time = duration_cast<nanoseconds>(end_time - start_time);

  

  cout << "[main] Completed execution: " << delta_time.count() / 1000000000.0 << "s" << endl;

  return 0;
}

void load_primes(const char * filename) {
  int i;
  int x;

  ifstream infile;

  infile.open(filename);

  if(!infile) {
    cout << "[lp] Couldn't open prime file." << endl;
    exit(1);
  }

  i = 0;
  while(i < MAX_NUM && infile >> x) {
    P[i] = x;
    i++;
  }
}