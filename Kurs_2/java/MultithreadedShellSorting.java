public class MultithreadedShellSorting implements Runnable {

    private int[] part1;
    private int[] part2;
    private int[] array;
    private Thread thr;

    public MultithreadedShellSorting(int[] part1, int[] part2) {
        super();
        this.part1 = part1;
        this.part2 = part2;
        this.thr = new Thread(this);
        thr.start();
    }

    @Override
    public void run() {
        try {
            Threads one = new Threads(part1);
            Threads two = new Threads(part2);
            one.getThr().join();
            two.getThr().join();
        } catch (InterruptedException e) {
        }
        array = merge(part1, part2);
    }

    private int[] merge(int[] part1, int[] part2) {
        int length = part1.length + part2.length;
        int[] merged = new int[length];
        int i1 = 0;
        int i2 = 0;
        for (int i = 0; i < length; i++) {
            if (i1 == part1.length) {
                merged[i] = part2[i2++];
            } else if (i2 == part2.length) {
                merged[i] = part1[i1++];
            } else {
                if (part1[i1] < part2[i2]) {
                    merged[i] = part1[i1++];
                } else {
                    merged[i] = part2[i2++];
                }
            }
        }
        return merged;
    }

    public Thread getThr() {
        return thr;
    }

    public int[] getArray() {
        return array;
    }
}