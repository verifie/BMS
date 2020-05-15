#!/usr/bin/python3
#

# Selfish code test...
# 2020/05/15 0642 PME.


class Restaurant(object):
    bankrupt = True

    def open_branch(self):
        if not self.bankrupt:
            print("branch opened")

x = Restaurant()

print ("Bankruptcy state: ", x.bankrupt)



