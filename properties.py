


class propValues():
    def __init__(self):

        self.cycle_file        = 10000
        self.cycle_write_image = 2000
        self.cycle_log         = 100
        
        self.time_sleep        = 60 * 0.3
        self.cycle_sleep       = 1000



class dtoDirectories():
    def __init__(self):
        self.directories = []
        self.directories.append("C:\\Users\\istor\\Desktop\\train\\test1")
        self.directories.append("C:\\Users\\istor\\Desktop\\train\\test2")

    def get_list(self):
        return self.directories

