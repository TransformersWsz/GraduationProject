const env = {
    database: "researcher",
    username: "root",
    password: "206209",
    host: "106.15.231.105",
    dialect: "mysql",
    pool: {
        max: 5,
        min: 0,
        acquire: 30000,
        idle: 10000
    }
};

module.exports = env;