


int main() {
	char buff[100] = {0};
	gets(buff);


	if (buff[1] == 0x45) {
		gets(buff);
		printf(buff);
	}

	if (buff[3] == 0x11) {
		printf(buff);
	}


	printf(buff);
	return 0;

}

