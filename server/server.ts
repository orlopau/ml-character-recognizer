import fastify from "fastify";
import fs from "fs";

let fast = fastify({
    logger: true,
    ignoreTrailingSlash: true
});

/*
 * Data is written as modified csv, using the following format:
 * Coords are written after each other: x1,y1,x2,y2,x3,y3,...
 * Each path is separated by a x: x1,y1,x2,y2,x,x1,y1,x2,y2,...
 */

const path = "../data.csv";

if (!fs.existsSync(path)){
    fs.openSync(path, "w");
}

let writeStream = fs.createWriteStream(path);

type Coord = {
    x: number,
    y: number
}

function writeDataToStream(paths: Array<Array<Coord>>): void {
    let line = "";

    paths.forEach(path => {
        path.forEach(coord => {
            line += coord.x + "," + coord.y + ",";
        });
        line += "x,";
    });

    if (line.length > 0) line = line.substr(0, line.length - 1);

    line += "\n";

    writeStream.write(line, "utf8");
}

fast.post("/data", async (req, res) => {
    let paths = req.body;
    writeDataToStream(paths);
    return;
});

const start = async () => {
    try {
        await fast.listen(3000, "0.0.0.0");
        console.log(`server listening on ${3000}`);
    } catch (e) {
        console.log(e);
    }
};
start();