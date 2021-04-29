import matplotlib
import matplotlib.pyplot as plt

def main():
    dank =      [9, 9, 9, 8, 4, 7, 2, 5, 7, 8, 8, 8, 9, 9, 10]
    dagny =     [6, 8, 7, 7, 9, 8, 7, 5, 4, 3, 6, 7, 7, 8, 9]
    olav =      [8, 8, 9, 9, 6, 8, 6, 5, 8, 6, 4, 9, 8, 9, 9]
    viro =      [7, 8, 8, 7, 7, 6, 6, 5, 8, 5, 7, 8, 9, 9, 9]
    mathias =   [7, 7, 9, 7, 7, 8, 7, 5, 6, 4, 6, 8, 7, 8, 9]

    names = ["Danilas", "Dagny", "Olav", "Viroshaan", "Mathias"]
    arrays = [dank, dagny, olav, viro, mathias]

    mean =      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(len(dank)):
        for a in arrays:
            mean[i] += a[i]

    for i in mean:
        mean[mean.index(i)] /= 5


    for i in arrays:
        plt.ylim(0, 10)
        plt.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], i)
        plt.title(names[arrays.index(i)])
        plt.xlabel("EiT dager")
        plt.ylabel("Motivasjon")
        plt.savefig(str(arrays.index(i)) + ".png")
        plt.show()
    
    plt.ylim(0, 10)
    for i in arrays:
        plt.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], i, label=names[arrays.index(i)], linestyle='None', marker='o', alpha=0.3)
    plt.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], mean, label="Gjennomsnitt")
    plt.xlabel("EiT dager")
    plt.ylabel("Motivasjon")
    plt.legend()
    plt.savefig("all.png")

    return 1

if __name__ == "__main__":
    main()