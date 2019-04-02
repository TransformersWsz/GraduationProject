const env = require("./env")

const Sequelize = require("sequelize");

const sequelize = new Sequelize(env.database, env.username, env.password, {
    host: env.host,
    dialect: env.dialect,
    pool: env.pool
});

const db = {};

db.Sequelize = Sequelize;
db.sequelize = sequelize;

module.exports = db;