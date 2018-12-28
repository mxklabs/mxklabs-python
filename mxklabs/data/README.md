## <a name="mxklabs.data">Module mxklabs.data
A work-in-progress python 3 module for data classes we find 
useful. Currently the only data class in this module is a 
file-backed circular buffer, used in IoT monitoring applications.

### Installation
```sh
pip install mxklabs
```

### Example
Create a circular buffer for 10-byte objects with 1000 records
and populate it with some strings. 

```python
import mxklabs.data     

if __name__ == "__main__":
  
  # Create non-volatile (backed by file) circular buffer.
  buffer = mxklabs.data.FileBackedCircularBuffer('filename.data', max_number_of_records=1000, record_size=10)
  
  # Add some silly records.
  buffer.add_record(bytes("foobar    ", 'utf-8'))
  buffer.add_record(bytes("superman  ", 'utf-8'))
  buffer.add_record(bytes("christmas ", 'utf-8'))
  
  # Print all records from oldest to newest.
  for record in buffer.records():
    print(str(record))
```

### API Summary

| Object | Type |
|---|---|
| [`mxklabs.data.FileBackedCircularBuffer`](#mxklabs.data.FileBackedCircularBuffer) [[`link`](#mxklabs.data.FileBackedCircularBuffer)] | `object` |
| [`mxklabs.data.FileBackedCircularBuffer`](#mxklabs.data.FileBackedCircularBuffer.add_record) [[`link`](#mxklabs.data.FileBackedCircularBuffer.add_record)] | `function` |
| [`mxklabs.data.FileBackedCircularBuffer`](#mxklabs.data.FileBackedCircularBuffer.records) [[`link`](#mxklabs.data.FileBackedCircularBuffer.records)] | `function` |
 
#### <a name="mxklabs.data.FileBackedCircularBuffer"></a> `mxklabs.data.FileBackedCircularBuffer(filename, max_number_of_records, record_size)`
Creates a circular buffer object which uses `filename` as a backend to store data. The buffer
can store at most `max_number_of_records` records of `record_size` bytes each.

#### <a name="mxklabs.data.FileBackedCircularBuffer.add_record"></a> `mxklabs.data.FileBackedCircularBuffer.add_record(self, record)`
Adds a record to the circular buffer. If the buffer is full it will discard the oldest entry.
The record must be a `bytes` object of length `record_size`.

#### <a name="mxklabs.data.FileBackedCircularBuffer.records"></a> `mxklabs.data.FileBackedCircularBuffer.records(self)`
Returns a list of all records currently in the buffer.