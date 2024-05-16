#include <iostream>
#include <pthread.h>
#include <semaphore.h>
#include <csignal>
#include <string>

const int buffer_size = 10;
const int iterations = 100;
int buffer[buffer_size];

int in = 0, out = 0;

sem_t empty, full, mutex;


void* producer_f(void* arg) {
    int id = *((int *)arg);
    int start_value = (id == 0) ? 1000 : 2000; //start at 1000, or if taken start at 2000

    for (int i = 0; i < iterations; i++) {
        sem_wait(&empty); //wait until there is at least one open slot in the buffer
        sem_wait(&mutex); //wait to enter critical section

        buffer[in] = start_value + i; //in_slot in the buffer is assigned starting value + i
        std::cout << "Producer " << id << " produced " << buffer[in] << " at " << in << ". (Out: " << out << ")" << std::endl;
        in = (in + 1) % buffer_size; //change in_slot to the next in_slot using modulus

        sem_post(&mutex); //release the lock on the critical section
        sem_post(&full); //tell the full_semaphore that it is no longer empty

        usleep(50);
    }
    pthread_exit(nullptr);
}

void* consumer_f(void* arg) {
    int id = *((int *)arg);

    for (int i = 0; i < iterations; i++) {
        sem_wait(&full); //wait until there is one item in the buffer
        sem_wait(&mutex); //wait until the mutex lock is available

        std::cout << "Consumer " << id << " consumed " << buffer[out] << " at " << out << ". (In: " << in << ")" << std::endl;
        out = (out + 1) % buffer_size; //advance the out value by 1 using modulus 10

        sem_post(&mutex); //release mutex lock
        sem_post(&empty); //tell the empty_semaphore that it is no longer full

        usleep(50);
    }

    pthread_exit(nullptr);
}

int main() {

    pthread_t producer1, producer2, consumer1, consumer2;

    int id_producer1 = 0;
    int id_consumer1 = 0;
    int id_producer2 = 1;
    int id_consumer2 = 1;

    sem_init(&empty, 0, buffer_size); //create empty semaphore with initial value buffer_size, saying there are buffer_size empty slots in the buffer
    sem_init(&full, 0, 0); //create full semaphore with initial value 0, meaning there are initially 0 filled slots in the buffer
    sem_init(&mutex, 0, 1); //create mutex semaphore with initial value 1, meaning that one critical section is initially unlocked

    //create threads, from assignment 4
    pthread_create(&producer1, nullptr, &producer_f, (void*)&id_producer1);
    pthread_create(&consumer1, nullptr,&consumer_f,(void*)&id_consumer1);
    pthread_create(&producer2,nullptr,&producer_f,(void*)&id_producer2);
    pthread_create(&consumer2,nullptr,&consumer_f,(void*)&id_consumer2);

    //wait for threads to die
    pthread_join(producer1,nullptr);
    pthread_join(consumer1,nullptr);
    pthread_join(producer2,nullptr);
    pthread_join(consumer2,nullptr);

    //output buffer contents
    std::string output_string;
    for (int i : buffer) {
        output_string+= " " + std::to_string(i);
    }

    std::cout << "Final Buffer Elements: " << output_string << std::endl;

    sem_destroy(&empty);
    sem_destroy(&full);
    sem_destroy(&mutex);

    return 0;
}
