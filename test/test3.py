import multiprocessing
import time
import requests
# Your foo function
def foo(n):
    while True:
        print "running.."
        requests.get('https://parakana.herokuapp.com/get_parking_data')

if __name__ == '__main__':
    # Start foo as a process
    p = multiprocessing.Process(target=foo, name="Foo", args=(10,))
    p.start()

    p.join(10)

    # If thread is active
    if p.is_alive():
        print "foo is running... let's kill it..."

        # Terminate foo
        p.terminate()
        p.join()
