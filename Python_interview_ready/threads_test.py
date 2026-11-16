import threading ;
from time import sleep;

class Hello(threading.Thread):
    def run(self):
        for i in range(5):
            print("Hello", i+1)
            sleep(0.1)

class Hi(threading.Thread):
    def run(self):
        for i in range(5):
            print("Hi", i+1)
            sleep(0.1)

t1 = Hello()
t2 = Hi()

t1.start();
t2.start()

#---------------------functions------------

import threading;
from time import sleep;

def hello():
        for i in range(5):
            print("Hello", i+1)
            sleep(0.1)

def hi():
        for i in range(5):
            print("Hi", i+1)
            sleep(0.1)

t1 = threading.Thread(target=hello)
t2 = threading.Thread(target=hi)

t1.start();
t2.start();

# main thread until 2 threads finishes
t1.join();
t2.join();


#---------------------threads save time------------

import threading;
from time import sleep, time;

def download(filename):
    print("Downloading file....", filename)
    sleep(0.5)
    print("Download complete")

files = ['video.mp4', 'file.txt', 'image.png']

start = time()
threads = []
for file in files:
  t = threading.Thread(target=download, args = (file,))
  threads.append(t)
  t.start()
  t.join()

end = time()

print(f'---->{end-start}')

print('Bye')
