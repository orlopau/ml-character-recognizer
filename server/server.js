const polka = require("polka");

const app = polka();

app.post("/data", (req, res) => {

});

app.listen(8080, err => {
   if (err) throw err;
   console.log(`> Running on localhost:8080`);
});