# Multi-Threaded Network Server for Pattern Analysis

## Overview

This project implements a multi-threaded network server designed to perform pattern analysis on incoming data from multiple clients. It processes the data, counts the occurrences of a specified pattern, and periodically outputs the results.

## Features

- **Multi-threaded server**: Handles multiple clients concurrently.
- **Pattern analysis**: Counts occurrences of a specified pattern in incoming data.
- **Data storage**: Saves received data into individual book files.
- **Periodic reporting**: Outputs sorted books by pattern frequency every 5 seconds.

## Getting Started

### Prerequisites

- Python 3.x
- Required libraries 

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Smin7005/Multi-Threaded-Network-Server-for-Pattern-Analysis.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Multi-Threaded-Network-Server-for-Pattern-Analysis
    ```

### Usage

1. Start the server with the desired port and pattern:
    ```bash
    python server.py -l <PORT> -p <PATTERN>
    ```
    Replace `<PORT>` with the port number and `<PATTERN>` with the search pattern.

2. Connect clients to the server and send data for analysis.

### Example

To start the server on port 8080 and search for the pattern "example":
```bash
python server.py -l 8080 -p example
```

## Code Explanation

### Node Class

Defines a linked list node used to store text data and pointers to the next nodes.

### Book Class

Stores information and content of each book, including a linked list of nodes and the pattern count.

### Global Variables

- `shared_list`: Stores all nodes.
- `books`: Stores all book objects.
- `lock`: Ensures thread safety.
- `pattern`: The pattern to search for in the data.

### Functions

- `handle_client(client_socket, book_number, pattern)`: Manages client connections, processes incoming data, and updates the book content.
- `periodic_output()`: Periodically outputs books sorted by pattern frequency.
- `main()`: Sets up the server, accepts client connections, and starts the periodic output.

## Contributing

Shangmin Chi (Shaun)

## License

This project is licensed under the MIT License. See the LICENSE file for details.


---
