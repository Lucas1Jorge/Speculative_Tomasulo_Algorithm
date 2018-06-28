#include <stdio.h>
#include <stdlib.h>


void swap(int* a, int* b) {
	int temp = *a;
	*a = *b;
	*b = temp;
}


int mdc(int a, int b) {
	if (a == 0 || b == 0) return 0;

	int temp;

	while (b != 0) {
		if (b > a) swap(&a, &b);
		temp = b;
		b = a - b;
		a = temp;
	}

	return a;
}


int main() {
	printf("%d\n", mdc(24, 32));
	printf("%d\n", mdc(5, 15));
	printf("%d\n", mdc(25, 30));
	printf("%d\n", mdc(49, 56));
	printf("%d\n", mdc(1, 56));
	printf("%d\n", mdc(0, 1));

	return 0;
}

/*
	ADDI R1, R0, 49
	ADDI R2, R0, 56

	BLE R2, R1, 24	; start swap
	ADD R2, R1, R2
	SUB R1, R2, R1
	SUB R2, R2, R1	; end swap

	ADD R3, R2, R0
	SUB R2, R1, R2
	ADD R1, R3, R0
	BEQ R2, R0, 28
	BLE R0, R2, 8
*/