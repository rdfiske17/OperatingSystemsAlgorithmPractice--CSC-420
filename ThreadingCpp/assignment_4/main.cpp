#include <iostream>
#include <pthread.h>

/*
 * Inspiration taken from https://www.geeksforgeeks.org/thread-functions-in-c-c/
 */

void* func1(void* arg) {
    std::cout << "We're in thread 1 now!" << std::endl;

    for(int i = 0; i < 2000000; i++) {
        if(i>51781 & i % 51781 == 0) {
            std::cout << "Thread 1 printing for i = " << i << "!" << std::endl;
        }
    }

    std::cout << "Thread 1 now exiting..." << std::endl;

    pthread_exit(nullptr);
}

void* func2(void* arg) {
    std::cout << "We're in thread 2 now!" << std::endl;

    for(int j = 0; j < 2000000; j++) {
        if(j>51781 & j % 51781 == 0) {
            std::cout << "Thread 2 printing for j = " << j << "!" << std::endl;
        }
    }

    std::cout << "Thread 2 now exiting..." << std::endl;

    pthread_exit(nullptr);
}

int main() {

    //https://www.unix.com/programming/21041-getting-username-c-program-unix.html
    char * p = getenv("USER");
    std::cout << "Hello, " << p << "!" << std::endl;

    pthread_t ptid1, ptid2;

    pthread_create(&ptid1, nullptr, &func1, nullptr);
    pthread_create(&ptid2, nullptr, &func2, nullptr);

    pthread_join(ptid1, nullptr);
    pthread_join(ptid2, nullptr);

    std::cout << "Threads closed!" << std::endl;

    return 0;

}

/*
 * Observations:
 * The interleaving pattern for this project seems quite random, like the interleaving for project 3. This is due to the
 * nature of scheduling the threads on the CPU. You can more-or-less regulate the order to go every-other if you use
 * usleep(t) to wait t microseconds between executions. However, without this wait factor, the randomness is quite
 * observable at this high of function loop values!
 */