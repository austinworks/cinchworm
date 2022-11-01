# Cinchworm

## Getting Started

- Create a Python virtual environment, if not already created.

    ```
    python3 -m venv env
    ```

- Upgrade packaging tools, if necessary.

    ```
    env/bin/pip install --upgrade pip setuptools
    ```

- Install the project in editable mode with its testing requirements.

    ```
    env/bin/pip install -e ".[testing]"
    ```

- Run your project's tests.

    ```
    env/bin/pytest
    ```

- Run your project.

    ```
    env/bin/pserve development.ini
    ```

## Compression 

The compression algorithm is dependent on the data being a set of relatively contiguous ranges, with few "outlier" values.

In raw form, the data is represented as 24-bit integers. To compress it, we create a "header" describing the minimum value for a given range and the number of values
contained in the range, followed by a "segment" of the data, represented as 16-bit integers.  With additional iteration, we might add another field to the header describing the size of the data in the range, enabling the algorithm to dynamically select 8, 10, or 16-bit as the size of the values within the segment.

This algorithm will fail against a dataset composed primarily of outliers.  Values that are not contiguous within a range of 65535 will be represented as singleton segments, turning a 24-bit integer into a 40-bit header followed by a 16-bit value.

```
Header
| initial value (3 bytes) | number of values in segment (2 bytes) |

Values
| 2 bytes | 2 bytes | 2 bytes |
```

## Web Flow

To ease setup, I have elected to work without a relational database, as it wasn't material to the requirements of the project.

The metadata about file uploads is stored in json files in the /uploads/meta folder.  A UUID is generated and passed to the "show" view,
this can be used to pull the metadata information and access the resulting binary data.  In this case, the UUID acts as both identifier and password,
giving reasonably good security against exploratory searches of the datastore.

The application uses 4 views

- home: GET presents the initial upload form
- compress: POST route initiating the compression event
- complete: GET shows the outcome of the compression
- download: GET allows the user to download the compressed binary


## Notes

This is my first time using Pyramid, I found it to be pretty reasonable.

Most of the work on the compression algorithm happened in a Jupyter notebook, it's ugly as heck but I'm including it for completeness.

Please do check out the included tests.
