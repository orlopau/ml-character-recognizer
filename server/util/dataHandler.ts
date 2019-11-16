import * as fs from "fs";
import * as path from "path";

type Coordinate = {
    x: number,
    y: number
}

/**
 * Handles saving and transforming training data
 */
class TrainingDataHandler {
    private charactersSaved = new Map<string, number>();
    private readonly alphabet: string = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    private readonly dao: CSVDataDAO;

    /**
     * Creates a new handler
     * @param dir where the data will be saved
     * @param threshold after which a new file is created
     */
    constructor(dir: string, threshold: number) {
        this.dao = new CSVDataDAO(dir, threshold);

        for (let i = 0; i < this.alphabet.length; i++) {
            this.charactersSaved.set(this.alphabet.charAt(i), 0);
        }
    }

    /**
     * Saves data to disk
     * @param char label char
     * @param paths paths
     */
    saveData(char: string, paths: Array<Array<Coordinate>>) {
        if (!char || !paths) throw new Error("Char or path can't be null!");

        paths.forEach(path => path.forEach(coord => {
            if (coord.x > 1 || coord.y > 1 || coord.x < 0 || coord.y < 0) throw new Error("Coordinates have to be in range 0...1")
        }));

        char = char.toUpperCase();
        if (!this.charactersSaved.has(char)) throw new Error("Char is not included in alphabet!");

        this.dao.add(this.transformToCSV(char, paths));
        this.charactersSaved.set(char, this.charactersSaved.get(char)! + 1);
    }

    /**
     * Returns the char which is most needed in the dataset aka the one that appears the least.
     */
    getMostNeededChar(): string {
        let char: string = "A";
        let min: number;
        this.charactersSaved.forEach((value, key) => {
            if (value < min || min == null) {
                min = value;
                char = key;
            }
        });

        return char;
    }

    /**
     * Transforms data into a csv formatted line.
     * @param paths - touch paths
     * @param char - character drawn
     */
    private transformToCSV(char: string, paths: Array<Array<Coordinate>>): string {
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
}

/**
 * Creates a new queue for file writing handling concurrency.
 * Overwrites specified file on creation.
 */
class CSVDataDAO {
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

export {TrainingDataHandler, Coordinate}

