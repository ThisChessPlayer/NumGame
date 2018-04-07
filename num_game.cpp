/*---------------------------------------------------------------------------*-

                                                         Author: Jason Ma
                                                         Date:   Apr 04 2018
                                      NumGame

  File Name:      num_game.cpp
  Description:    TODO
-*---------------------------------------------------------------------------*/

#include <chrono>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <queue>
#include <sstream>
#include <string>
#include <thread>
#include <vector>

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
using std::vector;

/*[Global Variables]---------------------------------------------------------*/
queue<state> * q;
int target;
int num_threads;

bool exit_threads = 0;

state::state(vector<int> n, const char * s) {
  while(n.size() != 0) {
    nums.push_back(n.back());
    n.pop_back();
  }
  
  strcpy(sol, s);
}

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
  msg.str("");

  while(1) {

    //if queue is empty, wait for element
    while(q[id].size() == 0) {
      msg << "[" << setw(4) << id << setw(1) << "] Q empty" << endl;
      cerr << msg.str();
      msg.str("");

      if(exit_threads) {
        return 0;
      }

      std::this_thread::sleep_for(std::chrono::seconds(1));
    }
    state s = q[id].front();
    q[id].pop();
  }

  return 0;
}

bool check_join() {
  int i;

  for(i = 0; i < num_threads; i++) {
    if(!q[i].empty())
      return 0;
  }
  return 1;
}

void handle_input() {
  string input;

  cout << "[main] Enter nums: " << endl;
  while(getline(cin, input)) {
    if(input == "q")
      break;

    stringstream ssinput(input);

    vector<int> nums;

    int i = 0;
    int num;
    while(i < MAX_STATE_SIZE && ssinput >> num) {
      nums.push_back(num);
      i++;
    }

    //DEBUG printout
    for(i = 0; i < (int) nums.size(); i++) {
      cout << nums[i] << " ";
    }
    cout << endl;

    state init_state(nums, "");
    q[0].push(init_state);

    //wait until join
    while(!check_join()) {
      //cerr << "[main] Waiting" << endl;

      //TODO maybe find some better way than busywaiting/polling
      std::this_thread::sleep_for(std::chrono::seconds(1));
    }

    cout << "[main] Enter nums: " << endl;
  }

  exit_threads = 1;
}

int main(int argc, char * argv[]) {
  
  int i;
  
  num_threads = 1;

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