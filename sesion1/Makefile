CC = gcc
CFLAGS = -Wall -Wextra -pedantic -std=c11

TARGET = 1-multiply_matrices

OBJ = functions.o 1-multiply_matrices.o

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $<

clean:
	rm -f $(TARGET) $(OBJ)

rebuild: clean all