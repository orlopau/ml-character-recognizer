import fastify from "fastify";
import fs from "fs";
import {transformToCSV, WritingQueue} from "./dataHandler";

let fast = fastify({
    logger: true,
    ignoreTrailingSlash: true
});

/*
 * Data is written as modified csv, using the following format:
 * The drawn Character is represented by a Char at the beginning of the entry.
 * Coords are written after each other: x1,y1,x2,y2,x3,y3,...
 * Each path is separated by a x: A,x1,y1,x2,y2,x,x1,y1,x2,y2,...
 */

/* Checks if directory exists, if not creates it. */
const dataDir = "../data/";
if (!fs.existsSync(dataDir)) fs.mkdirSync(dataDir);

let dao = new WritingQueue(dataDir, 10000);

fast.post("/data", async (req, res) => {
    let paths = req.body.paths;
    let char = req.body.character;

    if (!char || !paths) {
        res.status(400);
    } else {
        dao.add(transformToCSV(paths, char));
        res.status(200);
    }

    res.send();
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