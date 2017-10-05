import os
import time


def get_difference(a, b):
    s = set(a)
    return [x for x in b if x not in s]


class JournalWatcher:
    def __init__(self, directory, watch_delay=0.1):
        self._directory = directory
        self._watch_delay = watch_delay
        self._journal_files = os.listdir(directory)
        self._current_file_path = None

    def watch_file(self):
        with open(self._current_file_path, 'r') as log_file:
            # Go to the end of the file
            log_file.seek(0, 2)
            while True:
                # stop looping if a new journal has been detected
                new_file_path = self.get_new_journal_file()
                if new_file_path:
                    self._current_file_path = new_file_path
                    break
                line = log_file.readline()
                if line and not line == '\n':
                    yield line
                time.sleep(self._watch_delay)

    def get_new_journal_file(self):
        files = os.listdir(self._directory)
        if not sorted(files) == sorted(self._journal_files):
            new_files = get_difference(self._journal_files, files)
            # Update the files seen by the class
            self._journal_files = files
            # Checking the length takes deletions into consideration
            if len(new_files):
                new_file = new_files[0]
                print('New journal file detected: {}'.format(new_file))
                return new_file
        return None


if __name__ == '__main__':
    watcher = JournalWatcher(directory='C:\\test')
    while True:
        watcher.get_new_journal_file()
        time.sleep(1)