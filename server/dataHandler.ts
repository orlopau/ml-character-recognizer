import * as fs from "fs";
import * as path from "path";

type Coordinate = {
    x: number,
    y: number
}

/**
 * Creates a new queue for file writing handling concurrency.
 * Overwrites specified file on creation.
 */
class WritingQueue {
    private readonly dir: string;
    private writingQueue: Array<string> = [];
    private writeStream: fs.WriteStream;
    private readonly threshold: number;
    private active: boolean = false;
    private writtenLines: number = 0;

    /**
     * Creates a new writing queue for csv files.
     * Creates a new file when the line threshold is reached.
     * @param dir - directory to write files to
     * @param threshold - number of lines triggering creation of a new file
     */
    constructor(dir: string, threshold: number) {
        this.dir = dir;
        this.threshold = threshold;
        this.writeStream = this.createNewFileStream();
    }

    private consume(): void {
        if (this.writingQueue.length == 0) {
            this.active = false;
            return;
        }
        this.active = true;
        this.writeStream.write(this.writingQueue.pop());

        this.writtenLines++;
        if (this.writtenLines >= this.threshold) {
            this.createNewFileStream();
        }

        this.consume();
    }

    add(s: string) {
        this.writingQueue.push(s);
        if (!this.active) this.consume();
    }

    /**
     * Creates new file and stream in dir.
     */
    private createNewFileStream(): fs.WriteStream {
        let files = fs.readdirSync(this.dir);
        return fs.createWriteStream(path.join(this.dir, `data${files.length}.csv`));
    }
}

/**
 * Writes coord data to a specified file stream.
 * @param paths - touch paths
 * @param char - character drawn
 */
function transformToCSV(paths: Array<Array<Coordinate>>, char: string): string {
    if (char.length > 1) throw new Error("Char can only be 1 character long!");

    let line = char.toUpperCase();

    paths.forEach(path => {
        path.forEach(coord => {
            line += "," + coord.x + "," + coord.y;
        });
        line += ",x";
    });

    line += "\n";

    return line;
}

export {transformToCSV, WritingQueue, Coordinate}

