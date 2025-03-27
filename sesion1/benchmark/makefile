CC = gcc
CFLAGS = -Wall -Wextra -pedantic -std=c11

TARGET = mul_benchmark

OBJ = mul_functions.o mul_benchmark.o

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^

mul_functions.o: mul_functions.c mul_functions.h
	$(CC) $(CFLAGS) -c $<

mul_benchmark.o: mul_benchmark.c mul_functions.h
	$(CC) $(CFLAGS) -c $<

clean:
	rm -f $(TARGET) $(OBJ)

rebuild: clean all
