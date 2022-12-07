from Pyro4 import expose
from heapq import merge

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

    def solve(self):
        processed_arr = self.read_input()
        step = len(processed_arr) / len(self.workers)

        mapped = []
        for i in range(0, len(self.workers)):
            mapped.append(self.workers[i].mymap(processed_arr[i*step:i*step+step]))

        reduced = self.myreduce(mapped)
        self.write_output(reduced)

    @staticmethod
    @expose
    def mymap(array):
        array_len = len(array)
        gap = array_len // 2

        while gap > 0:
            j = gap
            while j < array_len:
                i = j - gap
                while i >= 0:
                    if array[i + gap] > array[i]:
                        break
                    else:
                        array[i + gap], array[i] = array[i], array[i + gap]
                    i = i - gap
                j += 1
            gap = gap // 2
        return array

    @staticmethod
    @expose
    def myreduce(mapped):
        arr_num = len(mapped)
        res = mapped[0].value
        for i in range(1, arr_num):
            res = list(merge(res, list(mapped[i].value)))
        return res

    def read_input(self):
        f = open(self.input_file_name, 'r')
        array = []
        arr_line = f.readline().split(' ')
        for element in arr_line:
            if element != '':
                array.append(int(element))
        f.close()
        return array

    def write_output(self, output):
        f = open(self.output_file_name, 'a')
        f.write(str(output))
        f.write('\n')
        f.close()