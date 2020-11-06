CC := g++
DEPS := class_CFAPGG.h
obj := class_CFAPGG.o All_FAPGG.o bimodal.o exponential.o powerlaw.o uniform.o


all: $(obj)
	$(CC) -o Deterministic.out class_CFAPGG.o All_FAPGG.o
	$(CC) -o Bimodal.out class_CFAPGG.o bimodal.o
	$(CC) -o Exponential.out class_CFAPGG.o exponential.o
	$(CC) -o Power_Law.out class_CFAPGG.o powerlaw.o
	$(CC) -o Uniform.out class_CFAPGG.o uniform.o

Deterministic: class_CFAPGG.o All_FAPGG.o
	$(CC) -o Deterministic.out class_CFAPGG.o All_FAPGG.o

Bimodal: class_CFAPGG.o bimodal.o
	$(CC) -o Bimodal.out class_CFAPGG.o bimodal.o

Exponential: class_CFAPGG.o exponential.o
	$(CC) -o Exponential.out class_CFAPGG.o exponential.o

Power_Law: class_CFAPGG.o powerlaw.o
	$(CC) -o Power_Law.out class_CFAPGG.o powerlaw.o

Uniform: class_CFAPGG.o uniform.o
	$(CC) -o Uniform.out class_CFAPGG.o uniform.o

%.o: %.c
	$(CC) -c $^ -o $@




clean:
	@echo "Cleaning up..."
	rm *.o *.out