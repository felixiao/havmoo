import sys, time

class ProgressBar:
    def __init__(self, count = 0, total = 0, width = 60):
        self.count = count
        self.total = total
        self.width = width
    def move(self):
        self.count += 1
    def log(self, s):
        sys.stdout.write(' ' * 79 + '\r')
        sys.stdout.flush()
        # print(s)
        progress = self.width * self.count / self.total
        sys.stdout.write(s+' '+'#' * int(progress) + '-' * int(self.width - progress) )
        sys.stdout.write('{0:6}/{1:6}'.format(self.count, self.total)+ '\r')
        if progress == self.width:
            sys.stdout.write('\n')
        sys.stdout.flush()
