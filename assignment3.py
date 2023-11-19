import socket
import threading
import argparse
from threading import Timer

# Node class, used to create a linked list structure for book content.
class Node:
    def __init__(self, data):
        self.data = data  # Store text data
        self.next = None  # Points to the next node
        self.book_next = None  # Points to the next node in the same book

# Book class, used for storing information and content linked list of each book.
class Book:
    def __init__(self, book_number):
        self.head = None  # Points to the head of the book content linked list.
        self.tail = None  # Points to the tail of the book content linked list.
        self.book_number = book_number  
        self.pattern_count = 0  #  Number of occurrences of the search pattern.

# Global variables
shared_list = []  # Shared list storing all nodes.
books = []  # List storing all book objects
lock = threading.Lock()  # Thread lock for synchronization
pattern = ""  # Pattern string to be searched

# Function to handle client connections.
def handle_client(client_socket, book_number, pattern):
    book = Book(book_number)  #  Create a new book object
    books.append(book)  # Add the new book to the global book list
    
    while True:
        data = client_socket.recv(4096)  # Receive data from the client
        if not data:
            print(f"Connection closed by client.")  # Client closed connection
            break
        
        text = data.decode().strip()  # Decode and remove whitespace from both ends
        print(f"Received data: {text}")  # Print received data
        
        node = Node(text)  
        with lock:  # Use lock to ensure thread safety
            if shared_list:
                shared_list[-1].next = node  # Add the new node to the end of the shared list
            shared_list.append(node)

        # Update the book content linked list
        if not book.head:
            book.head = node
        else:
            book.tail.book_next = node
        book.tail = node
        
        # Calculate the number of occurrences of the search pattern in the text.
        book.pattern_count += text.count(pattern)
        
    # When the client disconnects, save the book content to a file
    current_node = book.head
    with open(f"book_{book_number:02}.txt", 'w') as f:
        while current_node:
            f.write(current_node.data + '\n')  # Write node data to file
            current_node = current_node.book_next

    client_socket.close()  # Close client socket connection

# Periodic output function, regularly output books sorted by the frequency of search pattern occurrences
def periodic_output():
    with lock:
        sorted_books = sorted(books, key=lambda b: b.pattern_count, reverse=True)
        print(f"Books sorted by frequency of pattern '{pattern}':")
        for book in sorted_books:
            print(f"Book {book.book_number}: {book.pattern_count} occurrences")

    Timer(5, periodic_output).start()  # Execute every 5 seconds

def main():
    global pattern  
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Multi-threaded network server for pattern analysis")
    parser.add_argument("-l", "--listen", type=int, required=True, help="Listen port number")
    parser.add_argument("-p", "--pattern", type=str, required=True, help="Search pattern")
    args = parser.parse_args()
    
    pattern = args.pattern  # Set the search pattern
    listen_port = args.listen  # Set the listen port number

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create socket object
    server.bind(('0.0.0.0', listen_port))  # Bind address and port number
    server.listen(5)  # Start listening on the port
    print(f"Server listening on port {listen_port}")

    Timer(5, periodic_output).start()  # Start periodic output

    book_number = 1  # book number start from 1
    try:
        while True:
            client_socket, addr = server.accept()  # Accept new client connection
            print(f"Accepted connection from {addr}")  # Print client address
            # Create a new thread for each client connection
            client_thread = threading.Thread(target=handle_client, args=(client_socket, book_number, pattern))
            client_thread.start()  # Start the thread
            book_number += 1  # Increment book number
    except KeyboardInterrupt:
        print("Server is shutting down.")  # Capture keyboard interrupt, shut down server
    finally:
        server.close() 

if __name__ == "__main__":
    main() 

