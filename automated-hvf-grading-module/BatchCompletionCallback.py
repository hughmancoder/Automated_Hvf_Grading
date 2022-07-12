import math
import time

class BatchCompletionCallBack(object):
    # Added code - start
    global total_n_jobs
    # Added code - end
    def __init__(self, dispatch_timestamp, batch_size, parallel):
        self.dispatch_timestamp = dispatch_timestamp
        self.batch_size = batch_size
        self.parallel = parallel

    def __call__(self, out):
        self.parallel.n_completed_tasks += self.batch_size
        this_batch_duration = time.time() - self.dispatch_timestamp

        self.parallel._backend.batch_completed(self.batch_size,
                                           this_batch_duration)
        self.parallel.print_progress()
        # Added code - start
        progress = math.trunc((self.parallel.n_completed_tasks / total_n_jobs) * 100)
        print("Progress: {}".format(progress))

        time_remaining = math.trunc((this_batch_duration / self.batch_size) * (total_n_jobs - self.parallel.n_completed_tasks))
        print( "ETA: {}s".format(time_remaining/60))
        # Added code - end
        if self.parallel._original_iterator is not None:
            self.parallel.dispatch_next()