# Week 2 Notes

# Shared var error: Concurrency Issue
# Mutex/Lock/Semaphore

import time
from threading import Lock, Thread

class BankAccount(object):
    def __init__(self):
        self.lock = Lock()
        self.amount = 1000000 
    # Could also put lock in some method(s) for BankAccount

class Person(Thread):
    def __init__(self, action, account):
        super().__init__()
        self.iterations = 1000000
        self.account = account
        self.action = action

    def take_money(self):
        self.account.lock.acquire()
        self.account.amount -= 1
        self.account.lock.release()

    def put_money(self):
        self.account.lock.acquire()
        # Critical Section
        self.account.amount += 1
        self.account.lock.release()

    def run(self):
        while self.iterations > 0:
            getattr(self, "{}_money".format(self.action))()
            self.iterations -= 1


def take_money(account):
    t = 1000000
    while t > 0:
        t -= 1
        account.lock.acquire()
        account.amount -= 1
        account.lock.release()

def put_money(account):
    t = 1000000
    while t > 0:
        t -= 1
        account.lock.acquire()
        account.amount += 1
        account.lock.release()


if __name__ == "__main__":
    # Locks make sure account balance is 1000000
    Account = BankAccount()
    Seb = Person("put", Account)
    Seb_cousin = Person("take", Account)

    Seb.start() 
    Seb_cousin.start() 

    Seb.join()
    Seb_cousin.join()
    print(Account.amount)

    # Functions as threads
    s = Thread(target=put_money, args=(Account,))
    n = Thread(target=take_money, args=(Account,))
    s.start()
    n.start()
    s.join()
    n.join()
    print(Account.amount)
