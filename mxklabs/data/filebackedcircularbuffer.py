import os
import math

class FileBackedCircularBuffer(object):

    """
    A quickly written class to help store a rolling buffer of 'number_of_records'
    records, each of 'record_size' bytes, in a file-backed store.
    """

    def __init__(self, filename, max_number_of_records, record_size):
        self._filename = filename
        self._record_size = record_size
        self._max_number_of_records = max_number_of_records
        self._index_size = int(math.ceil(math.log10(max_number_of_records))) + 1 # Add one just in case of inaccuracies.
        self._data_size = max_number_of_records * (record_size + 1)
        self._filesize = self._index_size + self._data_size
        
        if os.path.exists(self._filename):
            # File exists, check it's the right size.
            with open(self._filename, 'rb') as file:
                file.seek(0, 2) # seek end of the file
                size = file.tell()
                assert(size == self._filesize)
        else:
            # File doesn't exist. Create it with index 0.
            with open(self._filename, 'wb') as file:
                file.write(self._index_to_bytes(0))
                numbytes = self._max_number_of_records * (self._record_size + 1)
                file.write(bytes([0x00] * numbytes))

    def records(self):
        result = []
        index = self._read_index()
        index = (index + 1) % self._max_number_of_records
        with open(self._filename, 'r+b') as file:
            for record_offset in range(self._max_number_of_records):
                offset = self._index_size + \
                         ((index + record_offset) % self._max_number_of_records) * (self._record_size + 1)
                file.seek(offset, 0)
                bytes = file.read(self._record_size + 1)
                if bytes[0] == 0x01:
                    result.append(bytes[1:])
        return result

    def add_record(self, record):
        index = self._read_index()
        print(self._read_index())
        with open(self._filename, 'r+b') as file:
            offset = self._index_size + \
                     index * (self._record_size + 1)
            file.seek(offset)
            file.write(bytes([0x01]) + record)
        index = (index + 1) % self._max_number_of_records
        self._write_index(index)

    def _index_to_bytes(self, index):
        index_str = str(index)
        index_bytes = index_str.encode('utf-8')
        assert(len(index_bytes) <= self._index_size)
        bytes_missing = (self._index_size - len(index_bytes))
        return bytes([0x30] * bytes_missing) + index_bytes

    def _index_from_bytes(self, bytes):
        return int(bytes)

    def _read_index(self):
        with open(self._filename, 'rb') as file:
            bytes = file.read(self._index_size)
            index = self._index_from_bytes(bytes)
            assert(index < self._max_number_of_records)
            return index
        raise RuntimeError("Unable to read index")

    def _write_index(self, index):
        bytes = self._index_to_bytes(index)
        with open(self._filename, 'r+b') as file:
            file.seek(0, 0) # byte 0 relative to start
            file.write(bytes)


